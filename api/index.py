"""
Vercel serverless function entry point
"""
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import after path is set
from mangum import Mangum
from main import app

# Create handler
handler = Mangum(app, lifespan="off")
