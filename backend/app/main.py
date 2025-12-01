"""
FastAPI application for RAG Chatbot backend.
"""
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.core.config import settings
from app.models.database import get_session_maker, init_db, ChatHistory
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    SelectedTextRequest,
    HealthResponse,
    IngestionRequest,
    IngestionResponse
)
from app.services.rag_service import RAGService
from app.services.ingestion_service import IngestionService


# Database setup
SessionMaker = get_session_maker(settings.database_url)


def get_db():
    """Dependency to get database session."""
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for FastAPI app."""
    # Startup
    print("Initializing database...")
    init_db(settings.database_url)
    print("Database initialized!")

    yield

    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics Chatbot API",
    description="RAG-based chatbot for the coursebook",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    rag_service = RAGService()
    qdrant_stats = rag_service.get_collection_stats()

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        services={
            "api": "running",
            "database": "connected",
            "qdrant": "connected" if "error" not in qdrant_stats else "error",
            "openai": "configured"
        }
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return await root()


@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint for asking questions about the book.

    Supports:
    - General questions about book content
    - Chapter-specific queries (with chapter filter)
    - Selected text queries (with selected_text parameter)
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Initialize RAG service
        rag_service = RAGService()

        # Get answer using RAG pipeline
        answer, retrieved_chunks = rag_service.answer_query(
            query=request.query,
            selected_text=request.selected_text,
            chapter_filter=request.chapter
        )

        # Store in chat history
        chat_history = ChatHistory(
            session_id=session_id,
            user_query=request.query,
            bot_response=answer,
            selected_text=request.selected_text,
            retrieved_chunks=[
                {
                    "chunk_id": chunk.chunk_id,
                    "score": chunk.score,
                    "metadata": chunk.metadata
                }
                for chunk in retrieved_chunks
            ],
            context_used="\n\n".join([chunk.content for chunk in retrieved_chunks]),
            model_used=settings.llm_model
        )
        db.add(chat_history)
        db.commit()

        # Return response
        return ChatResponse(
            answer=answer,
            session_id=session_id,
            retrieved_chunks=retrieved_chunks,
            model_used=settings.llm_model,
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/api/chat/selected", response_model=ChatResponse)
async def chat_selected_text(
    request: SelectedTextRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint for questions about user-selected text.

    This endpoint prioritizes the selected text as context while still
    retrieving some relevant chunks from the book for additional context.
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Initialize RAG service
        rag_service = RAGService()

        # Get answer with selected text as primary context
        answer, retrieved_chunks = rag_service.answer_query(
            query=request.query,
            selected_text=request.selected_text,
            top_k=3  # Fewer chunks when we have selected text
        )

        # Store in chat history
        chat_history = ChatHistory(
            session_id=session_id,
            user_query=request.query,
            bot_response=answer,
            selected_text=request.selected_text,
            retrieved_chunks=[
                {
                    "chunk_id": chunk.chunk_id,
                    "score": chunk.score,
                    "metadata": chunk.metadata
                }
                for chunk in retrieved_chunks
            ],
            context_used=request.selected_text,
            model_used=settings.llm_model
        )
        db.add(chat_history)
        db.commit()

        # Return response
        return ChatResponse(
            answer=answer,
            session_id=session_id,
            retrieved_chunks=retrieved_chunks,
            model_used=settings.llm_model,
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing selected text query: {str(e)}")


@app.post("/api/ingest", response_model=IngestionResponse)
async def ingest_documents(
    request: IngestionRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint to ingest or re-ingest all book documents.

    Use force_refresh=true to delete and re-ingest all documents.
    """
    try:
        # Path to docs directory (relative to backend)
        import os
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(backend_dir)
        docs_dir = os.path.join(project_root, "docs")

        if not os.path.exists(docs_dir):
            raise HTTPException(status_code=404, detail=f"Docs directory not found: {docs_dir}")

        # Run ingestion
        ingestion_service = IngestionService(db)
        stats = ingestion_service.ingest_documents(
            docs_directory=docs_dir,
            force_refresh=request.force_refresh
        )

        return IngestionResponse(
            status="completed" if not stats.get("errors") else "completed_with_errors",
            documents_processed=stats["documents_processed"],
            chunks_created=stats["chunks_created"],
            vectors_stored=stats["vectors_stored"],
            duration_seconds=stats["duration_seconds"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during ingestion: {str(e)}")


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about the RAG system."""
    try:
        from app.models.database import Document, DocumentChunk as DBDocumentChunk

        # Database stats
        doc_count = db.query(Document).count()
        chunk_count = db.query(DBDocumentChunk).count()
        chat_count = db.query(ChatHistory).count()

        # Qdrant stats
        rag_service = RAGService()
        qdrant_stats = rag_service.get_collection_stats()

        return {
            "database": {
                "documents": doc_count,
                "chunks": chunk_count,
                "chat_history_entries": chat_count
            },
            "qdrant": qdrant_stats,
            "models": {
                "embedding": settings.embedding_model,
                "llm": settings.llm_model
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
