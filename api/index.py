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

    # Create handler for Vercel
    handler = Mangum(app, lifespan="off")

    # Export handler as default
    def main(request, context):
        """Main handler function for Vercel"""
        try:
            return handler(request, context)
        except Exception as e:
            print(f"Handler error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "statusCode": 500,
                "body": f"Internal server error: {str(e)}"
            }

except Exception as e:
    print(f"Error loading app: {e}")
    import traceback
    traceback.print_exc()
    raise
