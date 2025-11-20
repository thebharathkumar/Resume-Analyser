"""
Vercel serverless function entry point
"""
import sys
import os
from pathlib import Path

# Get the directory containing this file
current_dir = Path(__file__).parent
backend_dir = current_dir.parent / "backend"

# Add backend to path
sys.path.insert(0, str(backend_dir))

try:
    from mangum import Mangum
    from main import app

    # Create handler for Vercel
    handler = Mangum(app, lifespan="off")

except Exception as e:
    print(f"Error loading app: {e}")
    import traceback
    traceback.print_exc()
    raise
