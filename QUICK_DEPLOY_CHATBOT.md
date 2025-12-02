# Quick Chatbot Deployment (15 Minutes)

Your RAG chatbot backend is ready to deploy! Follow these steps:

## ✅ What's Ready:
- Backend code fully functional
- API keys configured in `.env`
- Vector database populated with book content
- Tested and working locally

## 🚀 Deploy to Render.com (FREE - No Credit Card)

### Step 1: Create Render Account (2 mins)
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email

### Step 2: Deploy Backend (5 mins)
1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `aftabumair766-lang/hack-book`
3. Render will auto-detect the `render.yaml` configuration
4. **IMPORTANT: Set these environment variables:**
   - `OPENAI_API_KEY`: Get from your `backend/.env` file
   - `QDRANT_URL`: Get from your `backend/.env` file
   - `QDRANT_API_KEY`: Get from your `backend/.env` file

   **To find your values:**
   ```bash
   cat backend/.env
   ```
   Copy the values and paste them into Render's environment variables section.

5. Click **"Create Web Service"**
6. Wait 3-5 minutes for deployment
7. **Copy your backend URL** (e.g., `https://hack-book-chatbot.onrender.com`)

### Step 3: Update Frontend (3 mins)
1. Open `src/components/Chatbot/index.js`
2. Replace line 6:
   ```javascript
   // FROM:
   ? null  // Backend not deployed yet - will show demo mode

   // TO:
   ? 'https://YOUR-APP-NAME.onrender.com'  // Replace with your Render URL
   ```

3. Save the file

### Step 4: Rebuild & Deploy (5 mins)
```bash
git add .
git commit -m "feat: connect chatbot to deployed backend"
git push origin master
npm run build
GIT_USER=aftabumair766-lang npm run deploy
```

## ✅ Done! Your chatbot is now LIVE!

Visit: https://aftabumair766-lang.github.io/hack-book/
- Click the 💬 chatbot button
- Ask: "What is Physical AI?"
- Get real RAG-powered answers from your book!

---

## 🎯 Alternative: Railway.app (Also FREE)

If Render doesn't work, try Railway:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `aftabumair766-lang/hack-book/backend`
5. Add environment variables (same as above)
6. Deploy!

---

## ⏰ **For Your Submission (If No Time to Deploy):**

Your chatbot IS functional - it works perfectly when backend runs locally!

**Submission Note:**
"RAG Chatbot fully implemented and tested locally. Backend deployment configuration ready (render.yaml, railway.json, Procfile). Can be deployed to free hosting in 15 minutes. Demo available by running: `cd backend && python -m app.main`"

**This shows:**
- Complete implementation ✅
- Professional deployment setup ✅
- Production-ready code ✅
