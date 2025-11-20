"""
Data models for resume analysis
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class KeywordMatch(BaseModel):
    """Individual keyword match"""
    keyword: str
    count: int
    relevance_score: float = Field(ge=0, le=100)
    category: str  # technical, soft_skill, industry, etc.


class KeywordAnalysis(BaseModel):
    """Keyword analysis results"""
    total_keywords: int
    matched_keywords: List[KeywordMatch]
    missing_keywords: List[str]
    overall_score: float = Field(ge=0, le=100)
    recommendations: List[str]


class RoleMatch(BaseModel):
    """Role matching results"""
    target_role: str
    match_percentage: float = Field(ge=0, le=100)
    matched_skills: List[str]
    missing_skills: List[str]
    experience_match: float = Field(ge=0, le=100)
    education_match: float = Field(ge=0, le=100)
    recommendations: List[str]


class TextStrength(BaseModel):
    """Text strength at a specific position"""
    text: str
    start_pos: int
    end_pos: int
    strength_score: float = Field(ge=0, le=100)
    category: str  # strong, medium, weak
    issues: List[str] = []
    suggestions: List[str] = []


class GrammarIssue(BaseModel):
    """Grammar issue details"""
    message: str
    context: str
    offset: int
    length: int
    rule_id: str
    suggestions: List[str]
    severity: str  # error, warning, info


class HeatmapData(BaseModel):
    """Heatmap visualization data"""
    sections: List[Dict[str, Any]]
    text_strengths: List[TextStrength]
    grammar_issues: List[GrammarIssue]
    overall_grammar_score: float = Field(ge=0, le=100)


class ReadabilityScore(BaseModel):
    """Readability scoring metrics"""
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog: float
    smog_index: float
    automated_readability_index: float
    coleman_liau_index: float
    overall_score: float = Field(ge=0, le=100)
    interpretation: str
    recommendations: List[str]


class ATSCompatibility(BaseModel):
    """ATS compatibility assessment"""
    overall_score: float = Field(ge=0, le=100)
    formatting_score: float = Field(ge=0, le=100)
    structure_score: float = Field(ge=0, le=100)
    keyword_density: float
    file_format_compatible: bool
    issues: List[str]
    recommendations: List[str]


class JobDescriptionComparison(BaseModel):
    """Job description comparison results"""
    match_score: float = Field(ge=0, le=100)
    matched_requirements: List[str]
    missing_requirements: List[str]
    keyword_overlap: float = Field(ge=0, le=100)
    skills_gap: List[str]
    recommendations: List[str]


class ResumeAnalysisResult(BaseModel):
    """Complete resume analysis result"""
    analysis_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Resume metadata
    filename: str
    file_type: str
    word_count: int
    page_count: int

    # Analysis results
    ats_compatibility: ATSCompatibility
    keyword_analysis: KeywordAnalysis
    role_matching: Optional[RoleMatch] = None
    heatmap_data: HeatmapData
    readability: ReadabilityScore
    job_comparison: Optional[JobDescriptionComparison] = None

    # Summary
    overall_score: float = Field(ge=0, le=100)
    strengths: List[str]
    weaknesses: List[str]
    priority_improvements: List[str]


class AnalysisRequest(BaseModel):
    """Request model for resume analysis"""
    target_role: Optional[str] = None
    job_description: Optional[str] = None
    industry: Optional[str] = None


class UploadResponse(BaseModel):
    """Response after file upload"""
    file_id: str
    filename: str
    file_type: str
    size: int
    message: str
