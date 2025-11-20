# 🚀 Deployment Guide

This guide covers deploying the Resume ATS Analyzer to production.

## Architecture

- **Frontend**: Vercel (React/TypeScript)
- **Backend**: Railway or Render (Python/FastAPI)

## Prerequisites

- [Vercel Account](https://vercel.com/signup)
- [Railway Account](https://railway.app/) or [Render Account](https://render.com/)
- GitHub repository with your code

---

## Option 1: Deploy Backend to Railway (Recommended)

Railway is great for Python backends with dependencies like spaCy.

### Step 1: Deploy Backend to Railway

1. **Go to [Railway](https://railway.app/)**
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `Resume-Analyser` repository
5. Railway will auto-detect the Python app

### Step 2: Configure Railway

1. **Set Root Directory** (if needed):
   - Go to Settings → Root Directory
   - Set to `backend`

2. **Add Environment Variables**:
   ```
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

3. **Install Build Command**:
   Railway should auto-detect, but verify:
   ```bash
   pip install -r requirements.txt && python -m spacy download en_core_web_sm
   ```

4. **Set Start Command**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy**: Railway will build and deploy automatically

6. **Get Your Backend URL**: Copy the Railway app URL (e.g., `https://your-app.railway.app`)

---

## Option 2: Deploy Backend to Render

### Step 1: Create a New Web Service

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `resume-analyzer-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command**:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

5. **Add Environment Variables**:
   ```
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   PYTHON_VERSION=3.9.18
   ```

6. Click "Create Web Service"

7. **Get Your Backend URL**: Copy the Render app URL

---

## Deploy Frontend to Vercel

### Step 1: Prepare Frontend

1. **Update Frontend Environment Variable**:

   Create `.env.production` in `frontend/`:
   ```
   VITE_API_URL=https://your-railway-or-render-app.com/api
   ```

2. **Update `vercel.json`**:

   Already created! Just update the backend URL in the file:
   ```json
   {
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "https://your-backend-url.railway.app/api/:path*"
       }
     ]
   }
   ```

### Step 2: Deploy to Vercel

**Method 1: Vercel CLI (Recommended)**

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: resume-ats-analyzer
# - Directory: ./
# - Override settings? No

# Deploy to production
vercel --prod
```

**Method 2: Vercel Dashboard**

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Add Environment Variable**:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-url.railway.app/api`

6. Click "Deploy"

---

## Post-Deployment Steps

### 1. Update CORS Settings

In your backend `.env` or Railway/Render environment variables:

```
CORS_ORIGINS=https://your-app.vercel.app,https://resume-ats-analyzer.vercel.app
```

### 2. Test the Deployment

1. Visit your Vercel URL
2. Upload a test resume
3. Verify analysis works
4. Check browser console for errors

### 3. Custom Domain (Optional)

**Vercel:**
- Go to Project Settings → Domains
- Add your custom domain
- Follow DNS configuration steps

**Railway/Render:**
- Similar process in their dashboard
- Update CORS_ORIGINS with new domain

---

## Environment Variables Reference

### Backend (Railway/Render)

```bash
# Required
CORS_ORIGINS=https://your-frontend.vercel.app

# Optional
DEBUG=False
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=pdf,docx,doc
```

### Frontend (Vercel)

```bash
# Required
VITE_API_URL=https://your-backend.railway.app/api
```

---

## Troubleshooting

### Backend Issues

**spaCy model not found:**
- Ensure build command includes: `python -m spacy download en_core_web_sm`
- Check Railway/Render logs

**Memory issues:**
- Upgrade to a paid plan (free tier may be limited)
- Railway: 512MB RAM minimum recommended
- Render: Use at least Starter plan

**CORS errors:**
- Verify CORS_ORIGINS includes your Vercel URL
- Check both http:// and https://

### Frontend Issues

**API connection failed:**
- Verify VITE_API_URL is correct
- Check Railway/Render app is running
- Test backend URL directly in browser

**Build failures:**
- Check Node.js version (18+ required)
- Clear cache: `vercel --force`

---

## Quick Deployment Checklist

- [ ] Backend deployed to Railway/Render
- [ ] spaCy model downloaded during build
- [ ] Backend URL copied
- [ ] Frontend `vercel.json` updated with backend URL
- [ ] Environment variable `VITE_API_URL` set in Vercel
- [ ] CORS_ORIGINS updated in backend
- [ ] Frontend deployed to Vercel
- [ ] Test upload and analysis
- [ ] Custom domain configured (optional)

---

## Costs

**Free Tier:**
- Vercel: Free for personal projects
- Railway: $5 credit/month (may need paid plan)
- Render: Free tier available (limited)

**Recommended for Production:**
- Railway: ~$5-10/month
- Render: ~$7/month (Starter plan)
- Vercel: Free (hobby) or $20/month (Pro)

---

## Support

If you encounter issues:
1. Check Railway/Render/Vercel logs
2. Open a GitHub issue
3. Check CORS configuration
4. Verify environment variables

---

**Your app will be live at:**
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-app.railway.app` or `https://your-app.onrender.com`

🎉 **Congratulations! Your Resume ATS Analyzer is now live!**
