"""
Vercel serverless function - Minimal working version
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os
from pathlib import Path
import uuid

# Initialize FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
ALLOWED_EXTENSIONS = ["pdf", "docx", "doc"]
MAX_SIZE = 10 * 1024 * 1024  # 10MB

@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.post("/api/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        # Check extension
        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(400, f"Invalid file type. Use: {', '.join(ALLOWED_EXTENSIONS)}")

        # Read content
        content = await file.read()
        if len(content) > MAX_SIZE:
            raise HTTPException(400, "File too large (max 10MB)")

        # Generate ID
        file_id = str(uuid.uuid4())

        # Save to /tmp
        upload_dir = Path("/tmp/resume-uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / f"{file_id}.{ext}"
        file_path.write_bytes(content)

        return {
            "file_id": file_id,
            "filename": file.filename,
            "file_type": ext,
            "size": len(content),
            "message": "Upload successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/analyze/")
async def analyze(request: dict):
    file_id = request.get("file_id")
    if not file_id:
        raise HTTPException(400, "file_id required")

    # Check if file exists
    upload_dir = Path("/tmp/resume-uploads")
    found = False
    for ext in ALLOWED_EXTENSIONS:
        if (upload_dir / f"{file_id}.{ext}").exists():
            found = True
            break

    if not found:
        raise HTTPException(404, "File not found")

    # Return mock analysis
    return {
        "analysis_id": str(uuid.uuid4()),
        "file_id": file_id,
        "ats_score": 85,
        "overall_score": 82,
        "keyword_score": 78,
        "formatting_score": 90,
        "readability_score": 80,
        "sections_found": ["Summary", "Experience", "Education", "Skills"],
        "key_findings": [
            "Strong technical skills section",
            "Clear work experience descriptions",
            "Good use of action verbs"
        ],
        "recommendations": [
            "Add more quantifiable achievements",
            "Include relevant keywords",
            "Consider adding a skills summary"
        ],
        "keywords_found": ["Python", "JavaScript", "ML", "Data Analysis"],
        "missing_keywords": ["Cloud", "DevOps", "Agile"],
        "status": "completed"
    }

# Vercel handler
handler = Mangum(app, lifespan="off")
