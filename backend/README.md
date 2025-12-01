# RAG Chatbot Backend

This is the backend service for the Physical AI & Humanoid Robotics coursebook chatbot. It provides a Retrieval-Augmented Generation (RAG) system powered by OpenAI, Qdrant Cloud, and Neon Serverless Postgres.

## Features

- **RAG Pipeline**: Retrieval-augmented generation for accurate answers from book content
- **Vector Search**: Qdrant Cloud for semantic similarity search
- **Database**: Neon Serverless Postgres for metadata and chat history
- **Selected Text Queries**: Answer questions about user-selected text
- **Chapter Filtering**: Filter responses by specific chapters
- **Chat History**: Store and track all conversations

## Architecture

```
┌─────────────────┐
│  Docusaurus UI  │
│  (React App)    │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┬────────────┬──────────┐
    ▼         ▼            ▼          ▼
┌────────┐ ┌──────┐  ┌─────────┐ ┌────────┐
│ OpenAI │ │Qdrant│  │  Neon   │ │  Docs  │
│   API  │ │Cloud │  │Postgres │ │Markdown│
└────────┘ └──────┘  └─────────┘ └────────┘
```

## Prerequisites

- Python 3.10+
- OpenAI API key
- Qdrant Cloud account (free tier)
- Neon Serverless Postgres database (free tier)

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key
QDRANT_COLLECTION_NAME=hack_book_embeddings

# Neon Postgres
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require

# API Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Get Your API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy to `.env` as `OPENAI_API_KEY`

#### Qdrant Cloud (Free Tier)
1. Sign up at https://cloud.qdrant.io/
2. Create a new cluster (choose Free tier)
3. Get your cluster URL and API key
4. Add to `.env`:
   - `QDRANT_URL=https://your-cluster.qdrant.io`
   - `QDRANT_API_KEY=your-api-key`

#### Neon Serverless Postgres (Free Tier)
1. Sign up at https://neon.tech/
2. Create a new project
3. Get connection string from dashboard
4. Add to `.env` as `DATABASE_URL`

### 4. Ingest Documents

Process all markdown files from the `docs/` directory and create embeddings:

```bash
python scripts/ingest_docs.py
```

For force refresh (delete and re-ingest):

```bash
python scripts/ingest_docs.py --force-refresh
```

### 5. Run the Server

```bash
# Development mode (with auto-reload)
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00",
  "services": {
    "api": "running",
    "database": "connected",
    "qdrant": "connected",
    "openai": "configured"
  }
}
```

### Chat (General Questions)

```bash
POST /api/chat
Content-Type: application/json

{
  "query": "What is embodied intelligence?",
  "session_id": "optional-session-id",
  "chapter": "Chapter 1"  // Optional filter
}
```

Response:
```json
{
  "answer": "Embodied intelligence refers to...",
  "session_id": "session-123",
  "retrieved_chunks": [
    {
      "chunk_id": "chapter-01_chunk_0_abc",
      "content": "...",
      "score": 0.89,
      "metadata": {...}
    }
  ],
  "model_used": "gpt-4-turbo-preview",
  "timestamp": "2024-01-01T00:00:00"
}
```

### Chat (Selected Text)

```bash
POST /api/chat/selected
Content-Type: application/json

{
  "query": "Explain this in simpler terms",
  "selected_text": "Inverse kinematics is the process...",
  "session_id": "optional-session-id"
}
```

### Ingest Documents

```bash
POST /api/ingest
Content-Type: application/json

{
  "force_refresh": false
}
```

Response:
```json
{
  "status": "completed",
  "documents_processed": 15,
  "chunks_created": 342,
  "vectors_stored": 342,
  "duration_seconds": 45.2
}
```

### Statistics

```bash
GET /api/stats
```

Response:
```json
{
  "database": {
    "documents": 15,
    "chunks": 342,
    "chat_history_entries": 127
  },
  "qdrant": {
    "vectors_count": 342,
    "points_count": 342,
    "status": "green"
  },
  "models": {
    "embedding": "text-embedding-3-small",
    "llm": "gpt-4-turbo-preview"
  }
}
```

## Testing

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main challenges in humanoid robotics?",
    "chapter": "Chapter 6"
  }'

# Question about selected text
curl -X POST http://localhost:8000/api/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this concept",
    "selected_text": "Reinforcement learning enables robots to..."
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes (future modularization)
│   ├── core/             # Core configuration
│   │   └── config.py     # Settings and environment variables
│   ├── models/           # Data models
│   │   ├── database.py   # SQLAlchemy models
│   │   └── schemas.py    # Pydantic models
│   ├── services/         # Business logic
│   │   ├── document_processor.py  # Document chunking
│   │   ├── rag_service.py         # RAG pipeline
│   │   └── ingestion_service.py   # Document ingestion
│   └── main.py           # FastAPI application
├── scripts/
│   └── ingest_docs.py    # Standalone ingestion script
├── tests/                # Tests (to be added)
├── .env.example          # Example environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

### Embedding Model

Default: `text-embedding-3-small`

Options:
- `text-embedding-3-small` (1536 dimensions, fast, cheap)
- `text-embedding-3-large` (3072 dimensions, slower, better quality)
- `text-embedding-ada-002` (1536 dimensions, legacy)

### LLM Model

Default: `gpt-4-turbo-preview`

Options:
- `gpt-4-turbo-preview` (Best quality, more expensive)
- `gpt-3.5-turbo` (Faster, cheaper)
- `gpt-4` (Stable, reliable)

### Chunking Parameters

- `CHUNK_SIZE=1000` - Number of words per chunk
- `CHUNK_OVERLAP=200` - Overlap between chunks

Adjust in `.env`:
```env
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Deployment

### Railway.app

1. Create a new project on Railway.app
2. Add PostgreSQL plugin (or use Neon)
3. Deploy from GitHub
4. Set environment variables
5. Run ingestion: `python scripts/ingest_docs.py`

### Render.com

1. Create a new Web Service
2. Connect your GitHub repo
3. Set environment variables
4. Deploy

### Docker (Optional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring

### Check Qdrant Collection

```python
from app.services.rag_service import RAGService

rag = RAGService()
stats = rag.get_collection_stats()
print(stats)
```

### Check Database

```bash
# Connect to Neon Postgres
psql $DATABASE_URL

# Check documents
SELECT count(*) FROM documents;

# Check chunks
SELECT count(*) FROM document_chunks;

# Check chat history
SELECT count(*) FROM chat_history;
```

## Troubleshooting

### Connection Errors

- Check API keys in `.env`
- Verify Qdrant cluster is running
- Test Neon database connection
- Check CORS settings

### Ingestion Fails

- Verify `docs/` directory exists
- Check markdown file format
- Ensure API rate limits not exceeded
- Check disk space for embeddings

### Slow Responses

- Use `gpt-3.5-turbo` instead of `gpt-4`
- Reduce `top_k` in retrieval (default: 5)
- Use `text-embedding-3-small` instead of large
- Enable Qdrant query caching

## License

MIT License - See main project LICENSE file
