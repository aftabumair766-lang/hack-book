# RAG Chatbot Setup Guide

This guide will help you set up the integrated RAG (Retrieval-Augmented Generation) chatbot for your Physical AI & Humanoid Robotics coursebook.

## 🎯 What You'll Get

- **Interactive Q&A**: Students can ask questions about the book content
- **Selected Text Queries**: Highlight text and ask specific questions about it
- **Contextual Answers**: AI responses based on actual book content (RAG)
- **Cyberpunk UI**: Chatbot styled to match your book's theme
- **Chat History**: All conversations stored for analytics

## 📋 Prerequisites

Before starting, you'll need:

1. **OpenAI API Account** (for embeddings and LLM)
2. **Qdrant Cloud Account** (free tier available)
3. **Neon Serverless Postgres** (free tier available)
4. **Python 3.10+** installed

## 🚀 Quick Start (5 Steps)

### Step 1: Get Your API Keys

#### A. OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Important**: Add payment method (you'll need credits for embeddings and queries)

**Cost Estimate**: ~$0.10 - $1.00 for initial ingestion, ~$0.01 per chat query

#### B. Qdrant Cloud (Vector Database)

1. Go to https://cloud.qdrant.io/
2. Sign up for free account
3. Create a new cluster:
   - Choose **Free tier** (1GB, perfect for this project)
   - Select a region close to you
4. Once created, get your credentials:
   - **Cluster URL**: `https://your-cluster-name.qdrant.io`
   - **API Key**: Click "API Keys" → "Create API Key"

#### C. Neon Serverless Postgres

1. Go to https://neon.tech/
2. Sign up for free account
3. Create a new project
4. Get your connection string:
   - Go to your project dashboard
   - Click "Connection Details"
   - Copy the **connection string**
   - Format: `postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require`

### Step 2: Configure Backend

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Copy environment template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` with your credentials:
   ```env
   # OpenAI
   OPENAI_API_KEY=sk-your-key-here

   # Qdrant Cloud
   QDRANT_URL=https://your-cluster-name.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   QDRANT_COLLECTION_NAME=hack_book_embeddings

   # Neon Postgres
   DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

   # API Configuration
   CORS_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

### Step 3: Install Backend Dependencies

```bash
# Make sure you're in the backend/ directory
cd backend

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Ingest Book Content

This step processes all your markdown files, creates embeddings, and stores them in Qdrant:

```bash
python scripts/ingest_docs.py
```

**Expected output:**
```
==================================================
RAG Document Ingestion
==================================================

Initializing database...
Database initialized!
Docs directory: C:\Users\Lab One\hack_book\docs
Force refresh: False

Creating collection: hack_book_embeddings
Processing documents from: C:\Users\Lab One\hack_book\docs
Processed: Introduction (8 chunks)
Processed: Chapter 1: Foundations (12 chunks)
...

==================================================
INGESTION COMPLETE
==================================================
Status: Success
Documents processed: 15
Chunks created: 342
Vectors stored: 342
Duration: 45.2s
```

**Troubleshooting ingestion:**
- If it fails, try: `python scripts/ingest_docs.py --force-refresh`
- Check your API keys are correct
- Verify internet connection
- Ensure OpenAI API has credits

### Step 5: Start the Backend Server

```bash
# From backend/ directory
python -m app.main
```

or

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Test the backend:**

Open http://localhost:8000/health in your browser. You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "api": "running",
    "database": "connected",
    "qdrant": "connected",
    "openai": "configured"
  }
}
```

## 🎨 Frontend Setup (Already Done!)

The chatbot UI is already integrated into your Docusaurus site:

- **Component**: `src/components/Chatbot/index.js`
- **Styles**: `src/components/Chatbot/styles.module.css`
- **Integration**: `src/theme/Root.js`

Just make sure your Docusaurus dev server is running:

```bash
# From project root
npm start
```

## ✅ Testing the Chatbot

1. **Start both servers:**
   - Backend: `cd backend && python -m app.main` (port 8000)
   - Frontend: `npm start` (port 3000)

2. **Open your book:**
   - Go to http://localhost:3000/hack_book/

3. **Test the chatbot:**
   - Click the 💬 button in bottom-right corner
   - Ask: "What is embodied intelligence?"
   - Try selecting text and asking about it

## 🔧 Configuration Options

### Change AI Models

Edit `backend/.env`:

```env
# Use cheaper/faster model
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small

# Or use better quality
LLM_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-large
```

### Adjust Chunk Size

```env
# Larger chunks = more context, but slower retrieval
CHUNK_SIZE=1500
CHUNK_OVERLAP=300

# Smaller chunks = faster, but less context
CHUNK_SIZE=800
CHUNK_OVERLAP=150
```

### Change API Settings

```env
# Response creativity (0.0 = deterministic, 1.0 = creative)
LLM_TEMPERATURE=0.7

# Maximum response length
MAX_TOKENS=2000
```

## 📊 Monitoring & Analytics

### View Chat History

```bash
# Connect to Neon database
psql $DATABASE_URL

# View recent chats
SELECT user_query, bot_response, timestamp
FROM chat_history
ORDER BY timestamp DESC
LIMIT 10;
```

### Check System Stats

```bash
curl http://localhost:8000/api/stats
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
    "points_count": 342
  }
}
```

## 🚢 Deployment

### Deploy Backend

#### Option 1: Railway.app (Recommended)

1. Push your code to GitHub
2. Go to https://railway.app/
3. "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Add environment variables (all from `.env`)
6. Deploy!

#### Option 2: Render.com

1. Go to https://render.com/
2. "New" → "Web Service"
3. Connect GitHub repo
4. Select `backend/` as root directory
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables
8. Create service

### Update Frontend API URL

Once backend is deployed, update your Docusaurus config:

```javascript
// docusaurus.config.js
module.exports = {
  customFields: {
    REACT_APP_API_URL: 'https://your-backend-url.railway.app'
  }
};
```

Or set as environment variable:
```bash
REACT_APP_API_URL=https://your-backend-url.railway.app npm start
```

## ❓ Troubleshooting

### Chatbot doesn't appear

- Check browser console for errors
- Verify `src/theme/Root.js` exists
- Ensure Docusaurus dev server is running

### "Failed to get response from chatbot"

- Backend server must be running on port 8000
- Check CORS settings in `backend/.env`
- Test backend health: http://localhost:8000/health

### Slow responses

- Use `gpt-3.5-turbo` instead of `gpt-4`
- Reduce chunk retrieval: modify `top_k` in chatbot code
- Use smaller embedding model

### Ingestion fails

- Check OpenAI API credits
- Verify all API keys are correct
- Try `--force-refresh` flag
- Check markdown files don't have syntax errors

### Database connection errors

- Verify Neon connection string is correct
- Check database exists and is accessible
- Ensure `?sslmode=require` is in connection string

## 💰 Cost Breakdown

### Initial Setup (One-time)
- Document ingestion: ~$0.10 - $1.00 (depends on book size)
- Qdrant: **FREE** (1GB free tier)
- Neon Postgres: **FREE** (512MB free tier)

### Ongoing Costs (Per Month)
- Average chat query: ~$0.01 - $0.03
- 100 queries/day ≈ $30-90/month
- 10 queries/day ≈ $3-9/month

**Cost Optimization:**
- Use `gpt-3.5-turbo`: ~70% cheaper than `gpt-4`
- Use `text-embedding-3-small`: 80% cheaper than large
- Cache frequent queries (future feature)

## 📚 Next Steps

1. **Customize prompts**: Edit `backend/app/services/rag_service.py`
2. **Add authentication**: Protect backend with API keys
3. **Analytics dashboard**: Track most asked questions
4. **Fine-tune retrieval**: Adjust chunk size and overlap
5. **Add more features**: Export chat history, rating system, etc.

## 🆘 Getting Help

- **Backend issues**: Check `backend/README.md`
- **API documentation**: http://localhost:8000/docs (when server is running)
- **Docusaurus issues**: https://docusaurus.io/docs

## 🎉 You're Done!

Your RAG chatbot is now integrated into your coursebook! Students can:

- Ask questions about any topic
- Select text and ask for explanations
- Get contextual answers backed by your book content

Enjoy your intelligent, interactive coursebook! 🤖📚
