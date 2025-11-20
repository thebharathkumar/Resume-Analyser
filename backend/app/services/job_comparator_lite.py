"""
Lightweight job description comparator for Vercel
"""
import re
from typing import Dict, List, Set
from collections import Counter


class JobComparator:
    """Compare resume with job descriptions"""

    def __init__(self):
        """Initialize comparator"""
        pass

    def compare_with_job_description(self, resume_text: str, job_description: str) -> Dict:
        """Compare resume with job description"""

        # Extract keywords from both
        resume_keywords = self._extract_keywords(resume_text)
        jd_keywords = self._extract_keywords(job_description)

        # Calculate overlap
        matched = resume_keywords.intersection(jd_keywords)
        missing = jd_keywords - resume_keywords

        # Match score
        match_score = (len(matched) / len(jd_keywords) * 100) if jd_keywords else 0

        # Calculate keyword overlap
        resume_words = set(resume_text.lower().split())
        jd_words = set(job_description.lower().split())

        common_words = self._get_common_words()
        resume_words -= common_words
        jd_words -= common_words

        keyword_overlap = (len(resume_words.intersection(jd_words)) / len(jd_words) * 100) if jd_words else 0

        # Generate recommendations
        recommendations = self._generate_recommendations(match_score, list(missing)[:5])

        return {
            'match_score': round(match_score, 2),
            'matched_requirements': list(matched)[:20],
            'missing_requirements': list(missing)[:15],
            'keyword_overlap': round(keyword_overlap, 2),
            'skills_gap': list(missing)[:10],
            'recommendations': recommendations
        }

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract important keywords"""
        text_lower = text.lower()

        # Extract words 3+ characters
        words = re.findall(r'\b[a-z][a-z.+#]{2,}\b', text_lower)

        # Filter common words
        common = self._get_common_words()
        keywords = {w for w in words if w not in common and len(w) >= 3}

        return keywords

    def _get_common_words(self) -> Set[str]:
        """Get common words to exclude"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is',
            'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had',
            'will', 'would', 'can', 'could', 'should', 'may', 'might'
        }

    def _generate_recommendations(self, match_score: float, missing: List[str]) -> List[str]:
        """Generate recommendations"""
        recs = []

        if match_score < 50:
            recs.append(f"Low match ({match_score:.0f}%). Tailor resume to job description.")
        elif match_score < 70:
            recs.append(f"Moderate match ({match_score:.0f}%). Add more relevant keywords.")
        else:
            recs.append(f"Strong match ({match_score:.0f}%)!")

        if missing:
            recs.append(f"Add these keywords: {', '.join(missing)}")

        recs.append("Use exact keywords from job description where applicable.")

        return recs
