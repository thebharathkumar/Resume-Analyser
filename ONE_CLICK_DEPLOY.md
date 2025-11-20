# ⚡ ONE-CLICK VERCEL DEPLOYMENT

Deploy the entire Resume ATS Analyzer to Vercel in **ONE CLICK**!

## 🚀 Deploy Now

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/thebharathkumar/Resume-Analyser)

Or follow these super simple steps:

---

## Option 1: Deploy via Vercel Dashboard (2 minutes)

###  Step 1: Click Deploy

1. Go to **[vercel.com/new](https://vercel.com/new)**
2. Click **"Import Project"**
3. Paste your GitHub repo URL: `https://github.com/thebharathkumar/Resume-Analyser`
4. Click **"Import"**

### Step 2: Configure (automatically detected!)

Vercel will automatically detect:
- ✅ Framework: Vite (Frontend)
- ✅ Python Backend
- ✅ Build commands
- ✅ Output directories

**You don't need to configure anything!**

### Step 3: Deploy

Click **"Deploy"** and wait 2-3 minutes.

### ✅ Done!

Your app will be live at: `https://your-app.vercel.app`

---

## Option 2: Deploy via Vercel CLI (1 command)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy (from project root)
vercel --prod

# Follow the prompts (just press Enter for defaults)
```

**That's it!** Your app is live!

---

## 🎯 What Gets Deployed

### ✅ Full-Stack Application
- **Frontend**: React + TypeScript
- **Backend**: Python FastAPI (serverless)
- **Analysis Engine**: Lightweight NLP optimized for Vercel

### ✅ All Features Working
- ✅ Resume upload (PDF/DOCX)
- ✅ ATS compatibility analysis
- ✅ Keyword extraction
- ✅ Grammar & strength heatmap
- ✅ Readability scoring
- ✅ Role matching
- ✅ Job description comparison
- ✅ Export results (JSON)

### ✅ Optimized for Vercel
- Lightweight dependencies (no heavy spaCy models)
- Serverless-ready Python functions
- Fast cold starts
- Automatic scaling

---

## 🎨 After Deployment

### Your URLs
- **App**: `https://your-app.vercel.app`
- **API**: `https://your-app.vercel.app/api`
- **Health Check**: `https://your-app.vercel.app/health`

### Test It
1. Visit your Vercel URL
2. Upload a resume
3. Click "Analyze Resume"
4. See results instantly!

### Custom Domain (Optional)
1. Go to Vercel Dashboard → Your Project
2. Settings → Domains
3. Add your custom domain
4. Update DNS as instructed

---

## 💰 Cost

**100% FREE** on Vercel's Hobby plan!

- Unlimited deployments
- Automatic HTTPS
- Global CDN
- Serverless functions included

No credit card required!

---

## 🐛 Troubleshooting

### "Build Failed"

Check Vercel build logs:
1. Go to your deployment
2. Click "Building"
3. Check logs for errors

Common fixes:
- Ensure `frontend/package.json` exists
- Ensure `backend/requirements.txt` exists
- Check Python version (should be 3.9)

### "Function Too Large"

This shouldn't happen with our optimized setup, but if it does:
- Check `requirements.txt` has lightweight deps
- Ensure using `*_lite.py` versions of analyzers

### "404 on API calls"

- Check `vercel.json` is in project root
- Verify routes are configured correctly
- Check browser console for CORS errors

---

## 🎉 Success!

Once deployed, share your app:

### LinkedIn Post Template
```
🚀 Just launched my AI-powered Resume ATS Analyzer!

✅ See how ATS systems read YOUR resume
✅ Get instant keyword & grammar analysis
✅ Optimize for job descriptions
✅ 100% FREE to use!

Try it: [your-vercel-url]

Built with React, FastAPI & AI. Fully open source!
#buildinpublic #resumetips #jobsearch #webdev
```

### Tweet Template
```
Built an AI Resume Analyzer that shows exactly how ATS systems read your resume 🤖

✨ Instant analysis
✨ Keyword matching
✨ Grammar heatmap
✨ Free & open source

Try it → [your-url]

Tech: @vercel + React + FastAPI
```

---

## 📚 Resources

- **GitHub**: https://github.com/thebharathkumar/Resume-Analyser
- **Vercel Docs**: https://vercel.com/docs
- **Support**: Open a GitHub issue

---

## 🎯 Next Steps

After deploying:

1. ⭐ **Star the repo** on GitHub
2. 📱 **Share on social media**
3. 🎨 **Customize the design** (edit `frontend/src`)
4. 🚀 **Add features** (PR welcome!)
5. 💬 **Get feedback** from users

---

**Made with ❤️ for job seekers everywhere**

Deploy now and help people land their dream jobs! 🚀
