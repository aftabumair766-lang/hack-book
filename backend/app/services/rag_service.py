"""
RAG (Retrieval-Augmented Generation) service for chatbot.
"""
import os
import uuid
from typing import List, Dict, Optional, Tuple
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.core.config import settings
from app.models.schemas import RetrievedChunk


class RAGService:
    """Service for RAG operations: embedding, retrieval, and generation."""

    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=settings.openai_api_key)

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )

        self.collection_name = settings.qdrant_collection_name
        self.embedding_model = settings.embedding_model
        self.llm_model = settings.llm_model

    def create_collection(self, vector_size: int = 1536):
        """Create Qdrant collection if it doesn't exist."""
        try:
            collections = self.qdrant_client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                print(f"Created collection: {self.collection_name}")
            else:
                print(f"Collection already exists: {self.collection_name}")
        except Exception as e:
            print(f"Error creating collection: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text using OpenAI."""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    def store_chunk(
        self,
        chunk_id: str,
        text: str,
        metadata: Dict,
        vector: Optional[List[float]] = None
    ) -> str:
        """Store a document chunk with its vector in Qdrant."""
        try:
            # Generate embedding if not provided
            if vector is None:
                vector = self.generate_embedding(text)

            # Create point
            point = PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "text": text,
                    "chunk_id": chunk_id,
                    **metadata
                }
            )

            # Upsert to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            return chunk_id
        except Exception as e:
            print(f"Error storing chunk {chunk_id}: {e}")
            raise

    def retrieve_relevant_chunks(
        self,
        query: str,
        top_k: int = 5,
        chapter_filter: Optional[str] = None
    ) -> List[RetrievedChunk]:
        """Retrieve most relevant chunks for a query."""
        try:
            # Generate query embedding
            query_vector = self.generate_embedding(query)

            # Build filter if chapter specified
            query_filter = None
            if chapter_filter:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="chapter",
                            match=MatchValue(value=chapter_filter)
                        )
                    ]
                )

            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=query_filter
            )

            # Convert to RetrievedChunk objects
            chunks = []
            for result in search_results:
                chunk = RetrievedChunk(
                    chunk_id=result.payload.get("chunk_id", ""),
                    content=result.payload.get("text", ""),
                    score=result.score,
                    metadata={
                        k: v for k, v in result.payload.items()
                        if k not in ["text", "chunk_id"]
                    }
                )
                chunks.append(chunk)

            return chunks
        except Exception as e:
            print(f"Error retrieving chunks: {e}")
            raise

    def generate_response(
        self,
        query: str,
        context_chunks: List[RetrievedChunk],
        selected_text: Optional[str] = None
    ) -> str:
        """Generate response using OpenAI with retrieved context."""
        try:
            # Build context from chunks
            context = "\n\n".join([
                f"[Source {i+1} - {chunk.metadata.get('title', 'Unknown')}]\n{chunk.content}"
                for i, chunk in enumerate(context_chunks)
            ])

            # Build system message
            system_message = """You are an AI assistant for the "Physical AI & Humanoid Robotics" coursebook.
Your role is to help students understand concepts from the book by answering questions based on the provided context.

Guidelines:
- Answer questions accurately using ONLY the provided context
- If the context doesn't contain enough information, say so clearly
- Cite specific sections or chapters when referencing information
- Be concise but thorough
- Use technical language appropriate for university-level robotics students
- If asked about selected text, focus your answer on that specific passage"""

            # Build user message
            user_message = f"Context from the coursebook:\n\n{context}\n\n"

            if selected_text:
                user_message += f"\nSelected text:\n{selected_text}\n\n"

            user_message += f"Question: {query}\n\nPlease provide a detailed answer based on the context above."

            # Generate response
            response = self.openai_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=settings.llm_temperature,
                max_tokens=settings.max_tokens
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            raise

    def answer_query(
        self,
        query: str,
        selected_text: Optional[str] = None,
        chapter_filter: Optional[str] = None,
        top_k: int = 5
    ) -> Tuple[str, List[RetrievedChunk]]:
        """
        Complete RAG pipeline: retrieve and generate.

        Returns:
            Tuple of (answer, retrieved_chunks)
        """
        # If selected text is provided, use it as primary context
        if selected_text:
            # Still retrieve some relevant chunks for additional context
            retrieved_chunks = self.retrieve_relevant_chunks(
                query=query,
                top_k=2,  # Fewer chunks when we have selected text
                chapter_filter=chapter_filter
            )
        else:
            # Retrieve relevant chunks
            retrieved_chunks = self.retrieve_relevant_chunks(
                query=query,
                top_k=top_k,
                chapter_filter=chapter_filter
            )

        # Generate response
        answer = self.generate_response(
            query=query,
            context_chunks=retrieved_chunks,
            selected_text=selected_text
        )

        return answer, retrieved_chunks

    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector collection."""
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "vectors_count": collection_info.vectors_count,
                "points_count": collection_info.points_count,
                "status": collection_info.status
            }
        except Exception as e:
            return {"error": str(e)}
