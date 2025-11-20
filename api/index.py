"""
Vercel serverless function entry point
"""
import sys
import os

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from mangum import Mangum
from main import app

# Wrap FastAPI for Vercel serverless
handler = Mangum(app, lifespan="off")
