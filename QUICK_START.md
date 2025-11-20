# ⚡ Quick Start Guide

Choose your path:

## 🏠 Local Development (5 minutes)

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Terminal 1 - Start Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Start Frontend
cd frontend
npm run dev

# Open http://localhost:3000
```

## ☁️ Deploy to Production (10 minutes)

**See [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md) for the quickest path!**

### TL;DR:

1. **Backend to Railway** (3 min):
   - Go to railway.app
   - Deploy from GitHub
   - Set Root Directory: `backend`
   - Copy Railway URL

2. **Frontend to Vercel** (3 min):
   - Go to vercel.com/new
   - Import GitHub repo
   - Set Root Directory: `frontend`
   - Add env var: `VITE_API_URL=https://your-railway-url/api`
   - Deploy!

3. **Update CORS** (1 min):
   - In Railway: Set `CORS_ORIGINS=https://your-vercel-url`

**Done!** 🎉

---

## 📚 Documentation

- [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md) - Quick Vercel deployment (10 min)
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Comprehensive deployment guide
- [README.md](./README.md) - Full project documentation
- [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute

## 🐛 Troubleshooting

**Backend won't start:**
```bash
# Make sure spaCy model is installed
python -m spacy download en_core_web_sm

# Check Python version
python --version  # Should be 3.9+
```

**Frontend build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Check backend is running at http://localhost:8000
- Visit http://localhost:8000/health to verify
- Check CORS settings if deployed

## 💡 Tips

- Use Chrome DevTools to debug API calls
- Check browser console for errors
- Backend logs show detailed analysis progress
- Test with a real resume PDF for best results

## 🎯 Next Steps

After deploying:
1. Test with multiple resume formats
2. Share on LinkedIn with your URL
3. Customize the UI colors/branding
4. Add more role templates in `role_matcher.py`
5. Star the repo ⭐

**Need help?** Open a GitHub issue!
