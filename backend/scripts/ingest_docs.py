"""
Standalone script to ingest book documents into RAG system.

Usage:
    python scripts/ingest_docs.py [--force-refresh]
"""
import sys
import os
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.models.database import get_session_maker, init_db
from app.services.ingestion_service import IngestionService


def main():
    """Run document ingestion."""
    parser = argparse.ArgumentParser(description="Ingest book documents into RAG system")
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Delete and re-ingest all documents"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("RAG Document Ingestion")
    print("=" * 60)

    # Initialize database
    print("\nInitializing database...")
    init_db(settings.database_url)
    SessionMaker = get_session_maker(settings.database_url)
    db = SessionMaker()

    try:
        # Get docs directory path
        backend_dir = Path(__file__).parent.parent
        project_root = backend_dir.parent
        docs_dir = project_root / "docs"

        if not docs_dir.exists():
            print(f"Error: Docs directory not found: {docs_dir}")
            sys.exit(1)

        print(f"Docs directory: {docs_dir}")
        print(f"Force refresh: {args.force_refresh}")
        print()

        # Run ingestion
        ingestion_service = IngestionService(db)
        stats = ingestion_service.ingest_documents(
            docs_directory=str(docs_dir),
            force_refresh=args.force_refresh
        )

        # Print results
        print("\n" + "=" * 60)
        print("INGESTION COMPLETE")
        print("=" * 60)
        print(f"Status: {'Success' if not stats.get('errors') else 'Completed with errors'}")
        print(f"Documents processed: {stats['documents_processed']}")
        print(f"Chunks created: {stats['chunks_created']}")
        print(f"Vectors stored: {stats['vectors_stored']}")
        print(f"Duration: {stats['duration_seconds']}s")

        if stats.get("errors"):
            print(f"\nErrors ({len(stats['errors'])}):")
            for error in stats['errors'][:10]:  # Show first 10 errors
                print(f"  - {error}")

    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
