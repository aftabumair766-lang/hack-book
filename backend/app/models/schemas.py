"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chatbot queries."""
    query: str = Field(..., min_length=1, max_length=2000, description="User's question")
    session_id: Optional[str] = Field(None, description="Session ID for chat history")
    selected_text: Optional[str] = Field(None, description="Text selected by user for context")
    chapter: Optional[str] = Field(None, description="Current chapter for context filtering")


class RetrievedChunk(BaseModel):
    """Retrieved document chunk with score."""
    chunk_id: str
    content: str
    score: float
    metadata: Dict[str, Any]


class ChatResponse(BaseModel):
    """Response model for chatbot queries."""
    answer: str = Field(..., description="Bot's answer to the query")
    session_id: str = Field(..., description="Session ID")
    retrieved_chunks: List[RetrievedChunk] = Field(default_factory=list, description="Retrieved context chunks")
    model_used: str = Field(..., description="LLM model used for generation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SelectedTextRequest(BaseModel):
    """Request model for selected text queries."""
    selected_text: str = Field(..., min_length=1, description="Text selected by user")
    query: str = Field(..., min_length=1, max_length=500, description="Question about selected text")
    session_id: Optional[str] = Field(None, description="Session ID")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]


class IngestionRequest(BaseModel):
    """Request to ingest documents."""
    force_refresh: bool = Field(False, description="Force re-ingestion of all documents")


class IngestionResponse(BaseModel):
    """Response from document ingestion."""
    status: str
    documents_processed: int
    chunks_created: int
    vectors_stored: int
    duration_seconds: float
