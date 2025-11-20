"""
Main resume analyzer orchestrator
Coordinates all analysis services to generate comprehensive resume analysis
"""
from typing import Dict, Optional
import uuid
from datetime import datetime

from .document_parser import DocumentParser
from .keyword_analyzer import KeywordAnalyzer
from .ats_analyzer import ATSAnalyzer
from .grammar_analyzer import GrammarAnalyzer
from .readability_scorer import ReadabilityScorer
from .role_matcher import RoleMatcher
from .job_comparator import JobComparator

from ..models.analysis import (
    ResumeAnalysisResult,
    KeywordAnalysis,
    KeywordMatch,
    RoleMatch,
    HeatmapData,
    ReadabilityScore,
    ATSCompatibility,
    JobDescriptionComparison,
)


class MainAnalyzer:
    """Main analyzer that orchestrates all analysis services"""

    def __init__(self):
        """Initialize all analysis services"""
        self.parser = DocumentParser()
        self.keyword_analyzer = KeywordAnalyzer()
        self.ats_analyzer = ATSAnalyzer()
        self.grammar_analyzer = GrammarAnalyzer()
        self.readability_scorer = ReadabilityScorer()
        self.role_matcher = RoleMatcher()
        self.job_comparator = JobComparator()

    def analyze_resume(
        self,
        file_path: str,
        file_type: str,
        target_role: Optional[str] = None,
        job_description: Optional[str] = None,
        industry: Optional[str] = None
    ) -> ResumeAnalysisResult:
        """
        Perform comprehensive resume analysis

        Args:
            file_path: Path to resume file
            file_type: Type of file (pdf, docx)
            target_role: Optional target job role
            job_description: Optional job description for comparison
            industry: Optional industry specification

        Returns:
            Complete resume analysis result
        """

        # Parse document
        parsed_doc = self.parser.parse_document(file_path, file_type)
        text = parsed_doc['text']
        metadata = parsed_doc['metadata']

        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())

        # Word count
        word_count = self.parser.count_words(text)

        # Page count
        page_count = metadata.get('page_count', 1)

        # 1. ATS Compatibility Analysis
        ats_result = self.ats_analyzer.analyze_ats_compatibility(
            text, file_type, metadata
        )

        ats_compatibility = ATSCompatibility(
            overall_score=ats_result['overall_score'],
            formatting_score=ats_result['formatting_score'],
            structure_score=ats_result['structure_score'],
            keyword_density=ats_result['keyword_density'],
            file_format_compatible=ats_result['file_format_compatible'],
            issues=ats_result['issues'],
            recommendations=ats_result['recommendations']
        )

        # 2. Keyword Analysis
        if job_description:
            keyword_result = self.keyword_analyzer.analyze_keywords_with_job(
                text, job_description
            )
            matched_keywords = [
                KeywordMatch(
                    keyword=kw['keyword'],
                    count=kw['count'],
                    relevance_score=min(100, kw['count'] * 10),
                    category=kw['category']
                )
                for kw in keyword_result['matched_keywords']
            ]
            missing_keywords = keyword_result['missing_keywords']
            keyword_score = keyword_result['match_score']
        else:
            keywords = self.keyword_analyzer.extract_keywords(text)
            matched_keywords = [
                KeywordMatch(
                    keyword=kw['keyword'],
                    count=kw['count'],
                    relevance_score=min(100, kw['count'] * 10),
                    category=kw['category']
                )
                for kw in keywords
            ]
            missing_keywords = []
            keyword_score = 75  # Base score without job description

        keyword_recommendations = self.keyword_analyzer.get_keyword_recommendations(
            text, job_description
        )

        keyword_analysis = KeywordAnalysis(
            total_keywords=len(matched_keywords),
            matched_keywords=matched_keywords[:30],
            missing_keywords=missing_keywords[:20],
            overall_score=keyword_score,
            recommendations=keyword_recommendations
        )

        # 3. Role Matching (if target role provided)
        role_matching = None
        if target_role:
            role_result = self.role_matcher.match_role(
                text, target_role, job_description
            )

            role_matching = RoleMatch(
                target_role=target_role,
                match_percentage=role_result['match_percentage'],
                matched_skills=role_result['matched_skills'],
                missing_skills=role_result['missing_skills'],
                experience_match=role_result['experience_match'],
                education_match=role_result['education_match'],
                recommendations=role_result['recommendations']
            )

        # 4. Grammar and Strength Analysis (Heatmap)
        heatmap_result = self.grammar_analyzer.create_heatmap_data(text)

        heatmap_data = HeatmapData(
            sections=heatmap_result['sections'],
            text_strengths=heatmap_result['text_strengths'],
            grammar_issues=heatmap_result['grammar_issues'],
            overall_grammar_score=heatmap_result['overall_grammar_score']
        )

        # 5. Readability Analysis
        readability_result = self.readability_scorer.calculate_readability(text)
        hiring_manager_result = self.readability_scorer.assess_hiring_manager_readability(text)

        readability = ReadabilityScore(
            flesch_reading_ease=readability_result['flesch_reading_ease'],
            flesch_kincaid_grade=readability_result['flesch_kincaid_grade'],
            gunning_fog=readability_result['gunning_fog'],
            smog_index=readability_result['smog_index'],
            automated_readability_index=readability_result['automated_readability_index'],
            coleman_liau_index=readability_result['coleman_liau_index'],
            overall_score=hiring_manager_result['hiring_manager_score'],
            interpretation=readability_result['interpretation'],
            recommendations=readability_result['recommendations']
        )

        # 6. Job Description Comparison (if provided)
        job_comparison = None
        if job_description:
            comparison_result = self.job_comparator.compare_with_job_description(
                text, job_description
            )

            job_comparison = JobDescriptionComparison(
                match_score=comparison_result['match_score'],
                matched_requirements=comparison_result['matched_requirements'],
                missing_requirements=comparison_result['missing_requirements'],
                keyword_overlap=comparison_result['keyword_overlap'],
                skills_gap=comparison_result['skills_gap'],
                recommendations=comparison_result['recommendations']
            )

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            ats_compatibility.overall_score,
            keyword_analysis.overall_score,
            heatmap_data.overall_grammar_score,
            readability.overall_score,
            role_matching.match_percentage if role_matching else None,
            job_comparison.match_score if job_comparison else None
        )

        # Generate strengths and weaknesses
        strengths, weaknesses = self._analyze_strengths_weaknesses(
            ats_compatibility,
            keyword_analysis,
            heatmap_data,
            readability,
            role_matching,
            job_comparison
        )

        # Generate priority improvements
        priority_improvements = self._generate_priority_improvements(
            ats_compatibility,
            keyword_analysis,
            heatmap_data,
            readability,
            role_matching,
            job_comparison
        )

        # Create final result
        result = ResumeAnalysisResult(
            analysis_id=analysis_id,
            timestamp=datetime.utcnow(),
            filename=file_path.split('/')[-1],
            file_type=file_type,
            word_count=word_count,
            page_count=page_count,
            ats_compatibility=ats_compatibility,
            keyword_analysis=keyword_analysis,
            role_matching=role_matching,
            heatmap_data=heatmap_data,
            readability=readability,
            job_comparison=job_comparison,
            overall_score=overall_score,
            strengths=strengths,
            weaknesses=weaknesses,
            priority_improvements=priority_improvements
        )

        return result

    def _calculate_overall_score(
        self,
        ats_score: float,
        keyword_score: float,
        grammar_score: float,
        readability_score: float,
        role_match_score: Optional[float] = None,
        job_match_score: Optional[float] = None
    ) -> float:
        """Calculate overall resume score"""

        # Base weights
        weights = {
            'ats': 0.25,
            'keywords': 0.20,
            'grammar': 0.20,
            'readability': 0.15,
        }

        total_score = (
            ats_score * weights['ats'] +
            keyword_score * weights['keywords'] +
            grammar_score * weights['grammar'] +
            readability_score * weights['readability']
        )

        # Add role match if provided
        if role_match_score is not None:
            total_score += role_match_score * 0.10
            weights['role'] = 0.10

        # Add job comparison if provided
        if job_match_score is not None:
            total_score += job_match_score * 0.10
            weights['job'] = 0.10

        # Normalize if we added extra scores
        total_weight = sum(weights.values())
        if total_weight > 0:
            total_score = (total_score / total_weight) * 100

        return round(total_score, 2)

    def _analyze_strengths_weaknesses(
        self,
        ats: ATSCompatibility,
        keywords: KeywordAnalysis,
        heatmap: HeatmapData,
        readability: ReadabilityScore,
        role: Optional[RoleMatch],
        job: Optional[JobDescriptionComparison]
    ) -> tuple:
        """Analyze strengths and weaknesses"""

        strengths = []
        weaknesses = []

        # ATS
        if ats.overall_score >= 80:
            strengths.append(f"Excellent ATS compatibility ({ats.overall_score}%)")
        elif ats.overall_score < 60:
            weaknesses.append(f"Low ATS compatibility ({ats.overall_score}%)")

        # Keywords
        if keywords.overall_score >= 75:
            strengths.append(f"Strong keyword optimization ({keywords.overall_score}%)")
        elif keywords.overall_score < 50:
            weaknesses.append(f"Insufficient keyword coverage ({keywords.overall_score}%)")

        # Grammar
        if heatmap.overall_grammar_score >= 85:
            strengths.append(f"Excellent grammar and writing quality ({heatmap.overall_grammar_score}%)")
        elif heatmap.overall_grammar_score < 70:
            weaknesses.append(f"Grammar needs improvement ({heatmap.overall_grammar_score}%)")

        # Readability
        if readability.overall_score >= 75:
            strengths.append("Highly readable for hiring managers")
        elif readability.overall_score < 60:
            weaknesses.append("Readability could be improved")

        # Role match
        if role and role.match_percentage >= 70:
            strengths.append(f"Strong match for {role.target_role} ({role.match_percentage}%)")
        elif role and role.match_percentage < 50:
            weaknesses.append(f"Low match for {role.target_role} ({role.match_percentage}%)")

        # Job comparison
        if job and job.match_score >= 70:
            strengths.append(f"Well-aligned with job description ({job.match_score}%)")
        elif job and job.match_score < 50:
            weaknesses.append(f"Significant gaps vs. job description ({job.match_score}%)")

        return strengths, weaknesses

    def _generate_priority_improvements(
        self,
        ats: ATSCompatibility,
        keywords: KeywordAnalysis,
        heatmap: HeatmapData,
        readability: ReadabilityScore,
        role: Optional[RoleMatch],
        job: Optional[JobDescriptionComparison]
    ) -> list:
        """Generate priority improvements"""

        improvements = []

        # Collect all scores
        scores = [
            ('ATS Compatibility', ats.overall_score, ats.recommendations),
            ('Keywords', keywords.overall_score, keywords.recommendations),
            ('Grammar', heatmap.overall_grammar_score, []),
            ('Readability', readability.overall_score, readability.recommendations),
        ]

        if role:
            scores.append(('Role Match', role.match_percentage, role.recommendations))

        if job:
            scores.append(('Job Match', job.match_score, job.recommendations))

        # Sort by score (lowest first)
        scores.sort(key=lambda x: x[1])

        # Get top 3 areas needing improvement
        for area, score, recs in scores[:3]:
            if score < 70 and recs:
                improvements.append(f"{area}: {recs[0]}")

        # Add specific high-priority improvements
        if len(heatmap.grammar_issues) > 5:
            improvements.insert(0, f"Fix {len(heatmap.grammar_issues)} grammar issues")

        if keywords.missing_keywords and len(keywords.missing_keywords) > 5:
            improvements.insert(0, f"Add missing keywords: {', '.join(keywords.missing_keywords[:3])}")

        return improvements[:5]  # Top 5 improvements
