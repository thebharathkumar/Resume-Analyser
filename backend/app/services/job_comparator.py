"""
Job description comparison service
"""
from typing import Dict, List, Set
import re
from collections import Counter
import spacy


class JobComparator:
    """Compare resume against job descriptions"""

    def __init__(self):
        """Initialize job comparator"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise Exception(
                "spaCy model not found. Please run: python -m spacy download en_core_web_sm"
            )

    def compare_with_job_description(
        self, resume_text: str, job_description: str
    ) -> Dict:
        """Perform comprehensive comparison between resume and job description"""

        # Extract requirements from job description
        jd_requirements = self._extract_job_requirements(job_description)

        # Extract skills and keywords from resume
        resume_skills = self._extract_skills(resume_text)

        # Find matches and gaps
        matched_requirements = self._find_requirement_matches(
            resume_text, jd_requirements['all_requirements']
        )

        missing_requirements = [
            req for req in jd_requirements['all_requirements']
            if req.lower() not in resume_text.lower()
        ]

        # Calculate match score
        total_requirements = len(jd_requirements['all_requirements'])
        matched_count = len(matched_requirements)

        if total_requirements > 0:
            match_score = (matched_count / total_requirements) * 100
        else:
            match_score = 0

        # Calculate keyword overlap
        resume_keywords = set(resume_text.lower().split())
        jd_keywords = set(job_description.lower().split())

        # Filter out common words
        common_words = self._get_common_words()
        resume_keywords = resume_keywords - common_words
        jd_keywords = jd_keywords - common_words

        keyword_overlap_count = len(resume_keywords.intersection(jd_keywords))
        keyword_overlap_percentage = (
            (keyword_overlap_count / len(jd_keywords) * 100)
            if jd_keywords else 0
        )

        # Identify skills gap
        skills_gap = self._identify_skills_gap(
            resume_text, jd_requirements
        )

        # Generate recommendations
        recommendations = self._generate_comparison_recommendations(
            match_score,
            missing_requirements,
            skills_gap
        )

        return {
            'match_score': round(match_score, 2),
            'matched_requirements': matched_requirements[:20],
            'missing_requirements': missing_requirements[:15],
            'keyword_overlap': round(keyword_overlap_percentage, 2),
            'skills_gap': skills_gap,
            'recommendations': recommendations,
            'requirement_categories': jd_requirements['categories']
        }

    def _extract_job_requirements(self, job_description: str) -> Dict:
        """Extract requirements from job description"""

        doc = self.nlp(job_description.lower())

        # Initialize categories
        requirements = {
            'technical_skills': [],
            'soft_skills': [],
            'experience': [],
            'education': [],
            'certifications': [],
            'all_requirements': []
        }

        # Patterns for different requirement types
        patterns = {
            'technical_skills': r'(?:proficient|experience|knowledge|skilled)\s+(?:in|with)\s+([^.,;]+)',
            'years_experience': r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience',
            'education': r'(bachelor|master|phd|b\.s\.|m\.s\.|b\.a\.|m\.a\.|degree)',
            'certifications': r'(certified|certification|certificate)\s+([^.,;]+)',
        }

        # Extract using patterns
        for category, pattern in patterns.items():
            matches = re.findall(pattern, job_description.lower())
            requirements[category].extend(matches)

        # Extract noun chunks as potential requirements
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()
            if len(chunk_text) > 3 and chunk_text not in requirements['all_requirements']:
                requirements['all_requirements'].append(chunk_text)

        # Categorize soft skills
        soft_skill_keywords = [
            'communication', 'leadership', 'teamwork', 'problem solving',
            'analytical', 'creative', 'collaborative', 'organized',
            'attention to detail', 'time management'
        ]

        for skill in soft_skill_keywords:
            if skill in job_description.lower():
                requirements['soft_skills'].append(skill)

        # Remove duplicates
        for key in requirements:
            requirements[key] = list(set(requirements[key]))

        # Compile categories
        categories = {
            'technical': len(requirements['technical_skills']),
            'soft_skills': len(requirements['soft_skills']),
            'experience': len(requirements['experience']),
            'education': len(requirements['education'])
        }

        return {
            'all_requirements': requirements['all_requirements'][:30],
            'categories': categories,
            **requirements
        }

    def _extract_skills(self, text: str) -> Set[str]:
        """Extract skills from text"""
        doc = self.nlp(text.lower())

        skills = set()

        # Extract noun chunks
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()
            if len(chunk_text) > 2:
                skills.add(chunk_text)

        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
                skills.add(ent.text)

        return skills

    def _find_requirement_matches(
        self, resume_text: str, requirements: List[str]
    ) -> List[str]:
        """Find which requirements are met in the resume"""
        resume_lower = resume_text.lower()
        matched = []

        for req in requirements:
            req_lower = req.lower()

            # Check for exact match or partial match
            if req_lower in resume_lower:
                matched.append(req)
            else:
                # Check for partial word matches
                req_words = set(req_lower.split())
                resume_words = set(resume_lower.split())

                # If at least 70% of requirement words are in resume
                overlap = len(req_words.intersection(resume_words))
                if len(req_words) > 0 and overlap / len(req_words) >= 0.7:
                    matched.append(req)

        return matched

    def _identify_skills_gap(
        self, resume_text: str, jd_requirements: Dict
    ) -> List[str]:
        """Identify critical skills gap"""

        resume_lower = resume_text.lower()
        gaps = []

        # Check technical skills gap
        for skill in jd_requirements.get('technical_skills', []):
            if isinstance(skill, str) and skill.lower() not in resume_lower:
                gaps.append(skill)

        # Check soft skills gap
        for skill in jd_requirements.get('soft_skills', []):
            if skill.lower() not in resume_lower:
                gaps.append(skill)

        return gaps[:10]  # Top 10 gaps

    def _get_common_words(self) -> Set[str]:
        """Get set of common words to exclude from keyword analysis"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is',
            'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how'
        }

    def _generate_comparison_recommendations(
        self,
        match_score: float,
        missing_requirements: List[str],
        skills_gap: List[str]
    ) -> List[str]:
        """Generate recommendations based on comparison"""
        recommendations = []

        if match_score < 50:
            recommendations.append(
                f"Low match score ({match_score:.0f}%). Consider tailoring your resume "
                "to better align with the job description."
            )
        elif match_score < 70:
            recommendations.append(
                f"Moderate match ({match_score:.0f}%). Add more keywords and requirements "
                "from the job description."
            )
        else:
            recommendations.append(
                f"Strong match ({match_score:.0f}%)! Your resume aligns well with the job description."
            )

        if missing_requirements:
            top_missing = missing_requirements[:5]
            recommendations.append(
                f"Add these key requirements to your resume: {', '.join(top_missing)}"
            )

        if skills_gap:
            top_gaps = skills_gap[:5]
            recommendations.append(
                f"Address these skill gaps: {', '.join(top_gaps)}"
            )

        if match_score >= 70:
            recommendations.append(
                "Ensure your achievements use similar language and metrics as the job description."
            )

        recommendations.append(
            "Use exact keywords from the job description where truthful and applicable."
        )

        return recommendations

    def extract_key_phrases(self, text: str, top_n: int = 20) -> List[Dict]:
        """Extract key phrases from text"""
        doc = self.nlp(text.lower())

        # Extract noun chunks
        phrases = [chunk.text for chunk in doc.noun_chunks]

        # Count frequency
        phrase_counts = Counter(phrases)

        # Get top phrases
        top_phrases = phrase_counts.most_common(top_n)

        return [
            {'phrase': phrase, 'count': count}
            for phrase, count in top_phrases
        ]

    def calculate_semantic_similarity(
        self, resume_text: str, job_description: str
    ) -> float:
        """Calculate semantic similarity between resume and job description"""

        # Process both texts
        resume_doc = self.nlp(resume_text.lower())
        jd_doc = self.nlp(job_description.lower())

        # Calculate similarity using spaCy's built-in similarity
        # Note: This requires word vectors which are not in sm model
        # For production, use en_core_web_md or en_core_web_lg

        try:
            similarity = resume_doc.similarity(jd_doc)
            return round(similarity * 100, 2)
        except:
            # Fallback to simple keyword overlap if vectors not available
            resume_words = set(resume_text.lower().split())
            jd_words = set(job_description.lower().split())

            common_words = self._get_common_words()
            resume_words -= common_words
            jd_words -= common_words

            if len(jd_words) > 0:
                overlap = len(resume_words.intersection(jd_words))
                similarity = (overlap / len(jd_words)) * 100
            else:
                similarity = 0

            return round(similarity, 2)
