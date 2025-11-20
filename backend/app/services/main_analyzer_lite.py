"""
Lightweight main analyzer for Vercel deployment
Uses pattern matching instead of heavy NLP libraries
"""
from typing import Dict, Optional
import uuid
from datetime import datetime

from .document_parser import DocumentParser
from .keyword_analyzer_lite import KeywordAnalyzer
from .ats_analyzer import ATSAnalyzer
from .grammar_analyzer_lite import GrammarAnalyzer
from .readability_scorer import ReadabilityScorer
from .role_matcher_lite import RoleMatcher
from .job_comparator_lite import JobComparator

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
    """Lightweight analyzer optimized for Vercel deployment"""

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
        """Perform comprehensive resume analysis"""

        # Parse document
        parsed_doc = self.parser.parse_document(file_path, file_type)
        text = parsed_doc['text']
        metadata = parsed_doc['metadata']

        analysis_id = str(uuid.uuid4())
        word_count = self.parser.count_words(text)
        page_count = metadata.get('page_count', 1)

        # 1. ATS Compatibility
        ats_result = self.ats_analyzer.analyze_ats_compatibility(text, file_type, metadata)
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
            keyword_result = self.keyword_analyzer.analyze_keywords_with_job(text, job_description)
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
            keyword_score = 75

        keyword_recommendations = self.keyword_analyzer.get_keyword_recommendations(text, job_description)

        keyword_analysis = KeywordAnalysis(
            total_keywords=len(matched_keywords),
            matched_keywords=matched_keywords[:30],
            missing_keywords=missing_keywords[:20],
            overall_score=keyword_score,
            recommendations=keyword_recommendations
        )

        # 3. Role Matching
        role_matching = None
        if target_role:
            role_result = self.role_matcher.match_role(text, target_role, job_description)
            role_matching = RoleMatch(
                target_role=target_role,
                match_percentage=role_result['match_percentage'],
                matched_skills=role_result['matched_skills'],
                missing_skills=role_result['missing_skills'],
                experience_match=role_result['experience_match'],
                education_match=role_result['education_match'],
                recommendations=role_result['recommendations']
            )

        # 4. Grammar and Heatmap
        heatmap_result = self.grammar_analyzer.create_heatmap_data(text)
        heatmap_data = HeatmapData(
            sections=heatmap_result['sections'],
            text_strengths=heatmap_result['text_strengths'],
            grammar_issues=heatmap_result['grammar_issues'],
            overall_grammar_score=heatmap_result['overall_grammar_score']
        )

        # 5. Readability
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

        # 6. Job Description Comparison
        job_comparison = None
        if job_description:
            comparison_result = self.job_comparator.compare_with_job_description(text, job_description)
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
            ats_compatibility, keyword_analysis, heatmap_data,
            readability, role_matching, job_comparison
        )

        # Priority improvements
        priority_improvements = self._generate_priority_improvements(
            ats_compatibility, keyword_analysis, heatmap_data,
            readability, role_matching, job_comparison
        )

        return ResumeAnalysisResult(
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

    def _calculate_overall_score(self, ats_score: float, keyword_score: float,
                                 grammar_score: float, readability_score: float,
                                 role_match_score: Optional[float] = None,
                                 job_match_score: Optional[float] = None) -> float:
        """Calculate overall score"""
        weights = {'ats': 0.25, 'keywords': 0.20, 'grammar': 0.20, 'readability': 0.15}

        total_score = (ats_score * weights['ats'] + keyword_score * weights['keywords'] +
                      grammar_score * weights['grammar'] + readability_score * weights['readability'])

        if role_match_score is not None:
            total_score += role_match_score * 0.10
            weights['role'] = 0.10

        if job_match_score is not None:
            total_score += job_match_score * 0.10
            weights['job'] = 0.10

        total_weight = sum(weights.values())
        return round((total_score / total_weight) * 100, 2) if total_weight > 0 else 0

    def _analyze_strengths_weaknesses(self, ats, keywords, heatmap, readability,
                                     role, job) -> tuple:
        """Analyze strengths and weaknesses"""
        strengths = []
        weaknesses = []

        if ats.overall_score >= 80:
            strengths.append(f"Excellent ATS compatibility ({ats.overall_score}%)")
        elif ats.overall_score < 60:
            weaknesses.append(f"Low ATS compatibility ({ats.overall_score}%)")

        if keywords.overall_score >= 75:
            strengths.append(f"Strong keyword optimization ({keywords.overall_score}%)")
        elif keywords.overall_score < 50:
            weaknesses.append(f"Insufficient keywords ({keywords.overall_score}%)")

        if heatmap.overall_grammar_score >= 85:
            strengths.append(f"Excellent writing quality ({heatmap.overall_grammar_score}%)")
        elif heatmap.overall_grammar_score < 70:
            weaknesses.append(f"Writing needs improvement ({heatmap.overall_grammar_score}%)")

        if role and role.match_percentage >= 70:
            strengths.append(f"Strong match for {role.target_role}")
        elif role and role.match_percentage < 50:
            weaknesses.append(f"Low match for {role.target_role}")

        return strengths, weaknesses

    def _generate_priority_improvements(self, ats, keywords, heatmap, readability,
                                       role, job) -> list:
        """Generate priority improvements"""
        improvements = []

        scores = [
            ('ATS', ats.overall_score, ats.recommendations),
            ('Keywords', keywords.overall_score, keywords.recommendations),
            ('Grammar', heatmap.overall_grammar_score, []),
            ('Readability', readability.overall_score, readability.recommendations),
        ]

        if role:
            scores.append(('Role Match', role.match_percentage, role.recommendations))

        scores.sort(key=lambda x: x[1])

        for area, score, recs in scores[:3]:
            if score < 70 and recs:
                improvements.append(f"{area}: {recs[0]}")

        if len(heatmap.grammar_issues) > 5:
            improvements.insert(0, f"Fix {len(heatmap.grammar_issues)} writing issues")

        return improvements[:5]
