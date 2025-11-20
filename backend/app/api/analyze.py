"""
Resume analysis API endpoints - Optimized for Vercel serverless
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path

from ..core.config import settings
from ..models.analysis import ResumeAnalysisResult, AnalysisRequest
from ..services.main_analyzer_lite import MainAnalyzer

router = APIRouter()

# Initialize analyzer
analyzer = MainAnalyzer()


class AnalyzeRequestBody(BaseModel):
    """Request body for analysis"""
    file_id: str
    target_role: Optional[str] = None
    job_description: Optional[str] = None
    industry: Optional[str] = None


@router.post("/", response_model=ResumeAnalysisResult)
async def analyze_resume(request: AnalyzeRequestBody):
    """
    Analyze an uploaded resume

    Performs comprehensive analysis including:
    - ATS compatibility check
    - Keyword analysis
    - Role matching (if target role provided)
    - Grammar and strength heatmap
    - Readability scoring
    - Job description comparison (if JD provided)

    Returns detailed analysis results with scores and recommendations
    """

    # Find the uploaded file in /tmp (Vercel serverless)
    upload_dir = Path("/tmp/resume-uploads")
    file_path = None
    file_type = None

    for ext in settings.ALLOWED_EXTENSIONS:
        potential_path = upload_dir / f"{request.file_id}.{ext}"
        if potential_path.exists():
            file_path = str(potential_path)
            file_type = ext
            break

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="File not found. Please upload the file first or file may have expired."
        )

    try:
        # Perform analysis
        result = analyzer.analyze_resume(
            file_path=file_path,
            file_type=file_type,
            target_role=request.target_role,
            job_description=request.job_description,
            industry=request.industry
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/quick")
async def quick_analyze(request: AnalyzeRequestBody):
    """
    Quick analysis - returns only key metrics
    """

    # Find the uploaded file in /tmp
    upload_dir = Path("/tmp/resume-uploads")
    file_path = None
    file_type = None

    for ext in settings.ALLOWED_EXTENSIONS:
        potential_path = upload_dir / f"{request.file_id}.{ext}"
        if potential_path.exists():
            file_path = str(potential_path)
            file_type = ext
            break

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="File not found. Please upload the file first or file may have expired."
        )

    try:
        # Perform full analysis
        result = analyzer.analyze_resume(
            file_path=file_path,
            file_type=file_type,
            target_role=request.target_role,
            job_description=request.job_description
        )

        # Return quick summary
        return {
            "analysis_id": result.analysis_id,
            "overall_score": result.overall_score,
            "ats_score": result.ats_compatibility.overall_score,
            "keyword_score": result.keyword_analysis.overall_score,
            "grammar_score": result.heatmap_data.overall_grammar_score,
            "readability_score": result.readability.overall_score,
            "top_strength": result.strengths[0] if result.strengths else None,
            "top_weakness": result.weaknesses[0] if result.weaknesses else None,
            "priority_improvement": result.priority_improvements[0] if result.priority_improvements else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick analysis failed: {str(e)}"
        )


@router.get("/health")
async def analyzer_health():
    """Check if analyzer services are healthy"""

    try:
        # Quick check
        test_text = "This is a test."

        services_status = {
            "keyword_analyzer": "ok",
            "ats_analyzer": "ok",
            "grammar_analyzer": "ok",
            "readability_scorer": "ok",
            "role_matcher": "ok",
            "job_comparator": "ok"
        }

        return {
            "status": "healthy",
            "services": services_status,
            "message": "All analysis services operational"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
