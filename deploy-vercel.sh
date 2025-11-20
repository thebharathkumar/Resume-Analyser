#!/bin/bash

# Vercel Deployment Script for Resume ATS Analyzer

echo "🚀 Deploying Resume ATS Analyzer to Vercel..."

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm i -g vercel
fi

# Navigate to frontend
cd frontend

# Check for .env file
if [ ! -f .env.production ]; then
    echo "⚠️  Warning: .env.production not found"
    echo "Creating template .env.production file..."
    cat > .env.production << EOF
# Backend API URL - UPDATE THIS AFTER DEPLOYING BACKEND
VITE_API_URL=https://your-backend-url.railway.app/api
EOF
    echo "❗ Please update .env.production with your backend URL before deploying"
    echo "   Edit frontend/.env.production and replace 'your-backend-url.railway.app'"
    read -p "Press Enter after updating the file..."
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build locally to test
echo "🔨 Building frontend..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"

    # Deploy to Vercel
    echo ""
    echo "🚀 Deploying to Vercel..."
    echo "   Follow the prompts to configure your project"
    echo ""

    vercel --prod

    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "Next steps:"
    echo "1. Copy your Vercel URL"
    echo "2. Update backend CORS_ORIGINS with your Vercel URL"
    echo "3. Deploy backend to Railway or Render (see DEPLOYMENT.md)"
    echo ""
else
    echo "❌ Build failed. Please fix errors and try again."
    exit 1
fi

cd ..
