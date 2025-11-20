"""
File upload API endpoints - Optimized for Vercel serverless
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
import tempfile

from ..core.config import settings
from ..models.analysis import UploadResponse

router = APIRouter()


@router.post("/", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume file for analysis
    Uses /tmp directory for Vercel serverless compatibility
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

    # Use /tmp for Vercel serverless (ephemeral storage)
    upload_dir = Path("/tmp/resume-uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file with unique name
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


@router.delete("/{file_id}")
async def delete_uploaded_file(file_id: str):
    """Delete an uploaded file from /tmp"""

    upload_dir = Path("/tmp/resume-uploads")

    deleted = False
    for ext in settings.ALLOWED_EXTENSIONS:
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
        # File might have already been cleaned up by Vercel, that's okay
        return {"message": "File not found or already deleted", "file_id": file_id}

    return {"message": "File deleted successfully", "file_id": file_id}
