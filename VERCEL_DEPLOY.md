# 🚀 Quick Vercel Deployment Guide

This guide will get your Resume ATS Analyzer live in **under 10 minutes**!

## 📋 Prerequisites

- GitHub account (with this repo pushed)
- [Vercel account](https://vercel.com/signup) (free)
- [Railway account](https://railway.app) OR [Render account](https://render.com) (free tier available)

---

## Step 1️⃣: Deploy Backend (5 minutes)

### Option A: Railway (Recommended - Easier)

1. **Go to [Railway](https://railway.app)**
2. Click **"Start a New Project"** → **"Deploy from GitHub repo"**
3. Select your `Resume-Analyser` repository
4. **Configure the service:**
   - Click on the service
   - Go to **Settings** → **Root Directory** → Set to `backend`
   - Go to **Variables** → Add:
     ```
     CORS_ORIGINS=*
     ```
     *(We'll update this with your Vercel URL later)*

5. **Wait for deployment** (3-5 minutes)
6. **Copy your Railway URL** (something like `https://resume-analyzer-production.up.railway.app`)

### Option B: Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. Click **"New +" → "Web Service"**
3. Connect your GitHub repo
4. **Configure:**
   - Name: `resume-analyzer-api`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command:
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - Start Command:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
5. **Environment Variables:**
   ```
   CORS_ORIGINS=*
   ```

6. Click **"Create Web Service"**
7. **Copy your Render URL** (something like `https://resume-analyzer.onrender.com`)

---

## Step 2️⃣: Deploy Frontend to Vercel (3 minutes)

### Method 1: Using Vercel Dashboard (Easiest)

1. **Go to [Vercel Dashboard](https://vercel.com/new)**

2. **Import your GitHub repository**

3. **Configure the project:**
   - Framework Preset: **Vite**
   - Root Directory: **frontend**
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `dist` (auto-detected)

4. **Add Environment Variable:**
   - Click **"Environment Variables"**
   - Add:
     - Name: `VITE_API_URL`
     - Value: `https://your-railway-or-render-url.com/api`

     Example:
     ```
     VITE_API_URL=https://resume-analyzer-production.up.railway.app/api
     ```

5. Click **"Deploy"**

6. **Wait 2-3 minutes** for deployment

7. **Copy your Vercel URL** (e.g., `https://resume-ats-analyzer.vercel.app`)

### Method 2: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Create .env.production in frontend/
cd frontend
echo "VITE_API_URL=https://your-backend-url.railway.app/api" > .env.production

# Deploy
vercel --prod

# Follow the prompts
```

---

## Step 3️⃣: Update CORS (1 minute)

Now that you have your Vercel URL, update the backend CORS settings:

### Railway:
1. Go to your Railway project
2. Click on your service
3. Go to **Variables**
4. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
5. Redeploy (will happen automatically)

### Render:
1. Go to your Render dashboard
2. Click on your web service
3. Go to **Environment**
4. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
5. Save (will redeploy automatically)

---

## ✅ You're Live!

Visit your Vercel URL and test:

1. **Upload a resume**
2. **Click "Analyze Resume"**
3. **See the magic happen!** 🎉

---

## 🎯 URLs You'll Have

- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-app.railway.app` or `https://your-app.onrender.com`
- **API Docs**: `https://your-backend-url/api/docs`

---

## 🐛 Troubleshooting

### "Network Error" or API not responding

**Check:**
1. Is backend deployed and running? Visit `https://your-backend-url/health`
2. Is `VITE_API_URL` set correctly in Vercel?
3. Is CORS configured with your Vercel URL?

**Fix:**
- Vercel: Settings → Environment Variables → Check `VITE_API_URL`
- Backend: Variables → Check `CORS_ORIGINS`

### Backend Build Failed

**Railway/Render:**
- Check logs for errors
- Verify `requirements.txt` is in `backend/` directory
- Ensure Root Directory is set to `backend`

### "Module not found" errors

**Vercel:**
- Check that Root Directory is set to `frontend`
- Verify `package.json` is in `frontend/` directory

---

## 💰 Costs

- **Vercel**: FREE (Hobby plan)
- **Railway**: ~$5/month (after free credits)
- **Render**: FREE (with limitations) or $7/month

---

## 🎨 Optional: Custom Domain

### Vercel:
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS as instructed

### Railway/Render:
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records

Don't forget to update CORS settings with your new domain!

---

## 📞 Need Help?

- Check [Full Deployment Guide](./DEPLOYMENT.md)
- Open a GitHub issue
- Check Railway/Render/Vercel docs

---

**🎉 Congratulations! Your Resume ATS Analyzer is now LIVE and ready to go viral on LinkedIn!**

Share your deployment:
- Twitter/X
- LinkedIn
- Product Hunt
- Reddit r/webdev

Built with ❤️ | [GitHub](https://github.com/thebharathkumar/Resume-Analyser)
