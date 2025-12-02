"""
Database models for storing document metadata and chat history.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Document(Base):
    """Document metadata stored in PostgreSQL."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    chapter = Column(String(100))
    section = Column(String(200))
    file_path = Column(String(500), nullable=False)
    content_length = Column(Integer)
    chunk_count = Column(Integer)
    doc_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatHistory(Base):
    """Store chat conversations for analytics."""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    user_query = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    retrieved_chunks = Column(JSON)
    context_used = Column(Text)
    model_used = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)


class DocumentChunk(Base):
    """Store document chunks metadata (vectors stored in Qdrant)."""
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(255), unique=True, index=True, nullable=False)
    doc_id = Column(String(255), index=True, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_size = Column(Integer)
    doc_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_engine(database_url: str):
    """Create database engine."""
    return create_engine(database_url)


def get_session_maker(database_url: str):
    """Create session maker."""
    engine = get_engine(database_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(database_url: str):
    """Initialize database tables."""
    engine = get_engine(database_url)
    Base.metadata.create_all(bind=engine)
