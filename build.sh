#!/bin/bash
# Vercel build script

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Moving built files to root for Vercel..."
cp -r frontend/dist/* .

echo "Build complete!"
