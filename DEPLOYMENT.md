# Deployment Guide

This guide covers deploying your Physical AI & Humanoid Robotics coursebook to GitHub Pages.

## 🚀 Quick Deploy to GitHub Pages

### Prerequisites

- GitHub account
- Git installed locally
- Your repository pushed to GitHub

### Step 1: Update Configuration

Edit `docusaurus.config.js` and replace `YOUR_USERNAME` with your GitHub username:

```javascript
// Line 16
url: 'https://YOUR_GITHUB_USERNAME.github.io',

// Line 23
organizationName: 'YOUR_GITHUB_USERNAME',

// Lines 46, 56, 89, 116, 130
// Replace all instances of YOUR_USERNAME with your GitHub username
```

**Example:** If your GitHub username is `johndoe`:
```javascript
url: 'https://johndoe.github.io',
organizationName: 'johndoe',
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `hack_book`
3. Make it **Public** (required for free GitHub Pages)
4. Don't initialize with README (we already have content)
5. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hack_book.git

# Push all branches
git push -u origin --all
```

### Step 4: Deploy to GitHub Pages

```bash
# Build and deploy
npm run build
npm run deploy
```

Or use SSH (recommended):
```bash
USE_SSH=true npm run deploy
```

Or with explicit user:
```bash
GIT_USER=YOUR_USERNAME npm run deploy
```

### Step 5: Configure GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Source should already be set to `gh-pages` branch
4. Wait 1-2 minutes for deployment

### Step 6: Access Your Site

Your coursebook will be live at:
```
https://YOUR_USERNAME.github.io/hack_book/
```

## 🔧 Alternative Deployment Options

### Option 1: Netlify

1. Push code to GitHub
2. Go to https://netlify.com
3. "New site from Git" → Select your repo
4. Build command: `npm run build`
5. Publish directory: `build`
6. Click "Deploy"

**Advantages:**
- Automatic deploys on push
- Custom domain easy to set up
- Preview deployments for PRs
- Better performance than GitHub Pages

### Option 2: Vercel

1. Push code to GitHub
2. Go to https://vercel.com
3. Import your repository
4. Vercel auto-detects Docusaurus
5. Click "Deploy"

**Advantages:**
- Fastest global CDN
- Automatic HTTPS
- Preview deployments
- Analytics included

### Option 3: Cloudflare Pages

1. Push code to GitHub
2. Go to https://pages.cloudflare.com
3. Connect repository
4. Build command: `npm run build`
5. Output directory: `build`
6. Deploy

**Advantages:**
- Cloudflare CDN
- Unlimited bandwidth
- Fast build times

## 📝 Build Configuration

### Production Build

```bash
npm run build
```

This creates optimized static files in `build/` directory.

### Serve Locally (Production Build)

```bash
npm run serve
```

Test production build locally before deploying.

### Clear Cache (If Issues)

```bash
npm run clear
npm run build
```

## 🔒 Custom Domain Setup

### GitHub Pages with Custom Domain

1. Buy domain (e.g., from Namecheap, Google Domains)
2. In repository settings → Pages → Custom domain: `yourdomain.com`
3. In domain provider DNS settings, add:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153

   Type: A
   Name: @
   Value: 185.199.109.153

   Type: A
   Name: @
   Value: 185.199.110.153

   Type: A
   Name: @
   Value: 185.199.111.153

   Type: CNAME
   Name: www
   Value: YOUR_USERNAME.github.io
   ```

4. Update `docusaurus.config.js`:
   ```javascript
   url: 'https://yourdomain.com',
   baseUrl: '/',
   ```

### Netlify/Vercel Custom Domain

Much simpler - just add domain in dashboard and update DNS to their nameservers.

## 🌐 Deploy Backend (Optional)

If you've set up the RAG chatbot, deploy the backend separately:

### Railway.app (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
cd backend
railway init
railway up
```

Add all environment variables from `.env` in Railway dashboard.

### Render.com

1. Connect GitHub repo
2. New Web Service
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy

### Update Frontend API URL

After deploying backend, update chatbot API URL:

Create `.env.local`:
```env
REACT_APP_API_URL=https://your-backend.railway.app
```

Or in `docusaurus.config.js`:
```javascript
customFields: {
  API_URL: 'https://your-backend.railway.app'
}
```

Update `src/components/Chatbot/index.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL ||
                     'https://your-backend.railway.app';
```

## 🐛 Troubleshooting

### Build Fails

```bash
# Clear cache and rebuild
npm run clear
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 404 on GitHub Pages

- Ensure `baseUrl: '/hack_book/'` matches repo name
- Check Pages settings in GitHub repo
- Wait 1-2 minutes after deploy

### Assets Not Loading

- Check `baseUrl` in config
- Ensure URLs start with `/hack_book/` (not absolute paths)
- Clear browser cache

### Chatbot Not Working

- Backend must be running and accessible
- Check CORS settings in backend
- Verify API URL in chatbot component
- Check browser console for errors

## 📊 Monitoring

### GitHub Pages

- GitHub repo → Settings → Pages shows deployment status
- Check Actions tab for build logs

### Netlify/Vercel

- Dashboard shows all deployments
- Real-time logs available
- Analytics built-in

## ✅ Post-Deployment Checklist

- [ ] Site loads at GitHub Pages URL
- [ ] All chapters are accessible
- [ ] Book cover displays correctly
- [ ] Navigation works
- [ ] Dark theme applied
- [ ] Responsive on mobile
- [ ] Search works (if enabled)
- [ ] Chatbot UI appears (even if backend not configured)
- [ ] Custom domain configured (if applicable)
- [ ] Analytics added (Google Analytics, Plausible, etc.)

## 🔄 Continuous Deployment

### Automatic Deploys on Push

**GitHub Pages:**
Already automatic with `npm run deploy`

**Netlify/Vercel:**
Automatic on every push to main branch

**Custom GitHub Action:**

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

## 🎯 Performance Optimization

### Enable Compression

GitHub Pages serves with gzip automatically.

For other hosts, ensure:
- Brotli compression enabled
- GZIP fallback
- Cache headers set correctly

### CDN Configuration

- GitHub Pages: Uses Fastly CDN automatically
- Netlify/Vercel: Global CDN included
- Cloudflare: Best CDN performance

### Image Optimization

Already optimized with Docusaurus, but you can:
- Use WebP format for images
- Add lazy loading
- Compress images before upload

## 📈 Analytics

Add analytics by updating `docusaurus.config.js`:

### Google Analytics

```javascript
themeConfig: {
  gtag: {
    trackingID: 'G-XXXXXXXXXX',
  },
}
```

### Plausible Analytics (Privacy-friendly)

```javascript
scripts: [
  {
    src: 'https://plausible.io/js/script.js',
    async: true,
    defer: true,
    'data-domain': 'yourdomain.com'
  }
]
```

## 🎉 You're Live!

Once deployed, share your coursebook:
- Tweet about it
- Post on LinkedIn
- Share in robotics communities
- Add to awesome lists
- Submit to educational directories

---

**Need help?** Check:
- Docusaurus deployment docs: https://docusaurus.io/docs/deployment
- GitHub Pages docs: https://docs.github.com/pages
- Your deployment provider's documentation
