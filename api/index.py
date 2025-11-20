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

# Ensure /tmp directory exists for uploads
os.makedirs("/tmp/resume-uploads", exist_ok=True)

try:
    from mangum import Mangum
    from main import app

    # Create handler for Vercel - must be named 'handler'
    handler = Mangum(app, lifespan="off")

except Exception as e:
    print(f"Error loading app: {e}")
    import traceback
    traceback.print_exc()

    # Create a fallback handler that returns the error
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Failed to load application: {str(e)}"
        }
