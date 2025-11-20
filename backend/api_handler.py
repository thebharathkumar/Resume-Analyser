"""
Vercel serverless handler
"""
from mangum import Mangum
from main import app

# Wrap FastAPI app for Vercel
handler = Mangum(app, lifespan="off")
