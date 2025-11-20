"""
Vercel serverless function entry point
"""
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_path = str(Path(__file__).parent.parent / "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Ensure /tmp directory exists for uploads
os.makedirs("/tmp/resume-uploads", exist_ok=True)

# Import and create the FastAPI app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router
from app.core.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered ATS Resume Analyzer",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Create Mangum handler for Vercel
from mangum import Mangum
handler = Mangum(app, lifespan="off")
