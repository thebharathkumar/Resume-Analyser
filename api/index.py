"""
Vercel serverless function entry point - Self-contained version
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_path)

# Ensure /tmp directory exists
os.makedirs("/tmp/resume-uploads", exist_ok=True)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from mangum import Mangum

# Create FastAPI app
app = FastAPI(
    title="Resume ATS Analyzer",
    version="1.0.0",
    description="AI-powered ATS Resume Analyzer"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UploadResponse(BaseModel):
    file_id: str
    filename: str
    file_type: str
    size: int
    message: str

class AnalysisRequest(BaseModel):
    file_id: str
    target_role: Optional[str] = None
    job_description: Optional[str] = None

# Configuration
ALLOWED_EXTENSIONS = ["pdf", "docx", "doc"]
MAX_UPLOAD_SIZE = 10485760  # 10MB

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/upload/", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload a resume file for analysis"""

    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    content = await file.read()
    file_size = len(content)

    # Validate file size
    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    # Generate unique file ID
    file_id = str(uuid.uuid4())

    # Use /tmp for Vercel serverless
    upload_dir = Path("/tmp/resume-uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = upload_dir / f"{file_id}.{file_extension}"

    try:
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_type=file_extension,
        size=file_size,
        message="File uploaded successfully"
    )

@app.post("/api/analyze/")
async def analyze_resume(request: AnalysisRequest):
    """Analyze a resume"""

    # Find the uploaded file
    upload_dir = Path("/tmp/resume-uploads")

    # Try to find the file with any extension
    file_path = None
    for ext in ALLOWED_EXTENSIONS:
        potential_path = upload_dir / f"{request.file_id}.{ext}"
        if potential_path.exists():
            file_path = potential_path
            break

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="File not found. Please upload the file again."
        )

    # For now, return a simple mock analysis
    # TODO: Implement full analysis logic
    return {
        "analysis_id": str(uuid.uuid4()),
        "file_id": request.file_id,
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
            "Include relevant keywords for target role",
            "Consider adding a skills summary"
        ],
        "keywords_found": ["Python", "JavaScript", "Machine Learning", "Data Analysis"],
        "missing_keywords": ["Cloud Computing", "DevOps", "Agile"],
        "status": "completed"
    }

@app.delete("/api/upload/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file"""
    upload_dir = Path("/tmp/resume-uploads")

    deleted = False
    for ext in ALLOWED_EXTENSIONS:
        file_path = upload_dir / f"{file_id}.{ext}"
        if file_path.exists():
            try:
                os.remove(file_path)
                deleted = True
                break
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to delete file: {str(e)}"
                )

    if not deleted:
        return {"message": "File not found or already deleted", "file_id": file_id}

    return {"message": "File deleted successfully", "file_id": file_id}

# Create Mangum handler for Vercel
handler = Mangum(app, lifespan="off")
