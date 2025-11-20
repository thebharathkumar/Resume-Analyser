"""
File upload API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path

from ..core.config import settings
from ..models.analysis import UploadResponse

router = APIRouter()


@router.post("/", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume file for analysis

    Accepts PDF and DOCX files up to 10MB
    """

    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    content = await file.read()
    file_size = len(content)

    # Validate file size
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    # Generate unique file ID
    file_id = str(uuid.uuid4())

    # Create uploads directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(exist_ok=True)

    # Save file with unique name
    file_path = upload_dir / f"{file_id}.{file_extension}"

    with open(file_path, "wb") as f:
        f.write(content)

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_type=file_extension,
        size=file_size,
        message="File uploaded successfully"
    )


@router.delete("/{file_id}")
async def delete_uploaded_file(file_id: str):
    """Delete an uploaded file"""

    # Find and delete the file
    upload_dir = Path(settings.UPLOAD_DIR)

    deleted = False
    for ext in settings.ALLOWED_EXTENSIONS:
        file_path = upload_dir / f"{file_id}.{ext}"
        if file_path.exists():
            os.remove(file_path)
            deleted = True
            break

    if not deleted:
        raise HTTPException(status_code=404, detail="File not found")

    return {"message": "File deleted successfully", "file_id": file_id}
