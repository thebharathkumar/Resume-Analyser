"""API routes"""
from fastapi import APIRouter

from .upload import router as upload_router
from .analyze import router as analyze_router

router = APIRouter()

# Include sub-routers
router.include_router(upload_router, prefix="/upload", tags=["upload"])
router.include_router(analyze_router, prefix="/analyze", tags=["analyze"])
