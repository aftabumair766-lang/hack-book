"""
Document ingestion service to process and store book content.
"""
import time
from typing import Dict, List
from pathlib import Path
from sqlalchemy.orm import Session
from app.services.document_processor import DocumentProcessor
from app.services.rag_service import RAGService
from app.models.database import Document, DocumentChunk as DBDocumentChunk
from app.core.config import settings


class IngestionService:
    """Service to ingest documents into the RAG system."""

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.doc_processor = DocumentProcessor(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        self.rag_service = RAGService()

    def ingest_documents(
        self,
        docs_directory: str,
        force_refresh: bool = False
    ) -> Dict:
        """
        Ingest all documents from docs directory.

        Args:
            docs_directory: Path to docs folder
            force_refresh: If True, delete and re-ingest all documents

        Returns:
            Dictionary with ingestion statistics
        """
        start_time = time.time()

        stats = {
            "documents_processed": 0,
            "chunks_created": 0,
            "vectors_stored": 0,
            "errors": []
        }

        try:
            # Ensure collection exists
            self.rag_service.create_collection()

            # Clear existing data if force refresh
            if force_refresh:
                print("Force refresh: Clearing existing documents...")
                self.db_session.query(Document).delete()
                self.db_session.query(DBDocumentChunk).delete()
                self.db_session.commit()
                # Note: Qdrant collection recreation handled in create_collection

            # Process all markdown files
            print(f"Processing documents from: {docs_directory}")
            results = self.doc_processor.process_docs_directory(docs_directory)

            # Ingest each document
            for doc_id, title, metadata, chunks in results:
                try:
                    # Check if document already exists
                    existing_doc = self.db_session.query(Document).filter(
                        Document.doc_id == doc_id
                    ).first()

                    if existing_doc and not force_refresh:
                        print(f"Skipping existing document: {title}")
                        continue

                    # Store document metadata
                    doc = Document(
                        doc_id=doc_id,
                        title=title,
                        chapter=metadata.get('chapter', ''),
                        section=metadata.get('section', ''),
                        file_path=metadata.get('file_path', ''),
                        content_length=sum(len(c.text) for c in chunks),
                        chunk_count=len(chunks),
                        metadata=metadata
                    )

                    if existing_doc:
                        # Update existing
                        existing_doc.title = title
                        existing_doc.chapter = metadata.get('chapter', '')
                        existing_doc.section = metadata.get('section', '')
                        existing_doc.chunk_count = len(chunks)
                        existing_doc.metadata = metadata
                    else:
                        self.db_session.add(doc)

                    self.db_session.commit()
                    stats["documents_processed"] += 1

                    # Process and store chunks
                    for chunk in chunks:
                        try:
                            # Generate embedding and store in Qdrant
                            self.rag_service.store_chunk(
                                chunk_id=chunk.chunk_id,
                                text=chunk.text,
                                metadata=chunk.metadata
                            )

                            # Store chunk metadata in database
                            db_chunk = DBDocumentChunk(
                                chunk_id=chunk.chunk_id,
                                doc_id=doc_id,
                                chunk_index=chunk.chunk_index,
                                chunk_text=chunk.text,
                                chunk_size=len(chunk.text),
                                metadata=chunk.metadata
                            )
                            self.db_session.merge(db_chunk)
                            stats["chunks_created"] += 1
                            stats["vectors_stored"] += 1

                        except Exception as e:
                            error_msg = f"Error processing chunk {chunk.chunk_id}: {e}"
                            print(error_msg)
                            stats["errors"].append(error_msg)

                    self.db_session.commit()
                    print(f"✓ Ingested: {title} ({len(chunks)} chunks)")

                except Exception as e:
                    error_msg = f"Error ingesting document {doc_id}: {e}"
                    print(error_msg)
                    stats["errors"].append(error_msg)
                    self.db_session.rollback()

            duration = time.time() - start_time
            stats["duration_seconds"] = round(duration, 2)

            print(f"\nIngestion complete!")
            print(f"Documents processed: {stats['documents_processed']}")
            print(f"Chunks created: {stats['chunks_created']}")
            print(f"Vectors stored: {stats['vectors_stored']}")
            print(f"Duration: {stats['duration_seconds']}s")

            if stats["errors"]:
                print(f"Errors encountered: {len(stats['errors'])}")

            return stats

        except Exception as e:
            error_msg = f"Fatal error during ingestion: {e}"
            print(error_msg)
            stats["errors"].append(error_msg)
            return stats
