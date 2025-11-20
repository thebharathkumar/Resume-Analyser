"""
Keyword analysis service for resume content
"""
import spacy
from collections import Counter
from typing import List, Dict, Set
import re
from sklearn.feature_extraction.text import TfidfVectorizer


class KeywordAnalyzer:
    """Analyze keywords and their relevance in resumes"""

    def __init__(self):
        """Initialize with spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model not found, provide helpful error
            raise Exception(
                "spaCy model not found. Please run: python -m spacy download en_core_web_sm"
            )

        # Common technical skills and keywords by category
        self.skill_categories = {
            'programming': {
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby',
                'go', 'rust', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab'
            },
            'web': {
                'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
                'spring', 'asp.net', 'html', 'css', 'sass', 'webpack', 'next.js'
            },
            'database': {
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'dynamodb', 'cassandra', 'sqlite'
            },
            'cloud': {
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
                'jenkins', 'ci/cd', 'devops', 'cloud'
            },
            'data_science': {
                'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                'scikit-learn', 'pandas', 'numpy', 'data analysis', 'statistics',
                'nlp', 'computer vision', 'ai', 'artificial intelligence'
            },
            'soft_skills': {
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical', 'creative', 'management', 'agile', 'scrum'
            },
            'tools': {
                'git', 'github', 'gitlab', 'jira', 'confluence', 'slack',
                'visual studio', 'vscode', 'intellij', 'postman'
            }
        }

        # Action verbs for impact assessment
        self.strong_action_verbs = {
            'achieved', 'improved', 'increased', 'decreased', 'developed',
            'created', 'implemented', 'designed', 'launched', 'led', 'managed',
            'optimized', 'streamlined', 'delivered', 'built', 'engineered',
            'architected', 'spearheaded', 'pioneered', 'transformed', 'accelerated'
        }

    def extract_keywords(self, text: str, max_keywords: int = 50) -> List[Dict]:
        """Extract important keywords from text"""
        doc = self.nlp(text.lower())

        # Extract noun phrases and named entities
        keywords = []

        # Get noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]

        # Get named entities
        entities = [ent.text for ent in doc.ents]

        # Combine and count
        all_keywords = noun_phrases + entities

        # Filter out short keywords and common words
        filtered_keywords = [
            kw.strip() for kw in all_keywords
            if len(kw.strip()) >= 3 and not self._is_common_word(kw)
        ]

        # Count frequencies
        keyword_counts = Counter(filtered_keywords)

        # Get top keywords
        top_keywords = keyword_counts.most_common(max_keywords)

        return [
            {
                'keyword': kw,
                'count': count,
                'category': self._categorize_keyword(kw)
            }
            for kw, count in top_keywords
        ]

    def _is_common_word(self, word: str) -> bool:
        """Check if word is too common to be meaningful"""
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can'
        }
        return word.lower() in common_words

    def _categorize_keyword(self, keyword: str) -> str:
        """Categorize a keyword into skill category"""
        keyword_lower = keyword.lower()

        for category, skills in self.skill_categories.items():
            if any(skill in keyword_lower for skill in skills):
                return category

        return 'general'

    def analyze_keywords_with_job(
        self, resume_text: str, job_description: str
    ) -> Dict:
        """Analyze resume keywords against job description"""

        # Extract keywords from both
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_description)

        # Create sets for comparison
        resume_kw_set = {kw['keyword'].lower() for kw in resume_keywords}
        job_kw_set = {kw['keyword'].lower() for kw in job_keywords}

        # Find matches and gaps
        matched = resume_kw_set.intersection(job_kw_set)
        missing = job_kw_set - resume_kw_set

        # Calculate match score
        if len(job_kw_set) > 0:
            match_score = (len(matched) / len(job_kw_set)) * 100
        else:
            match_score = 0

        # Find matching keywords with details
        matched_keywords = [
            kw for kw in resume_keywords
            if kw['keyword'].lower() in matched
        ]

        return {
            'matched_keywords': matched_keywords,
            'missing_keywords': list(missing)[:20],  # Top 20 missing
            'match_score': round(match_score, 2),
            'total_resume_keywords': len(resume_keywords),
            'total_job_keywords': len(job_keywords)
        }

    def calculate_keyword_density(self, text: str, keywords: List[str]) -> float:
        """Calculate keyword density in text"""
        text_lower = text.lower()
        total_words = len(text_lower.split())

        if total_words == 0:
            return 0

        keyword_count = sum(
            text_lower.count(keyword.lower()) for keyword in keywords
        )

        density = (keyword_count / total_words) * 100
        return round(density, 2)

    def extract_action_verbs(self, text: str) -> Dict:
        """Extract and analyze action verbs"""
        doc = self.nlp(text.lower())

        # Extract verbs
        verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']

        # Count verbs
        verb_counts = Counter(verbs)

        # Categorize as strong or weak
        strong_verbs = {
            verb: count for verb, count in verb_counts.items()
            if verb in self.strong_action_verbs
        }

        weak_verbs = {
            verb: count for verb, count in verb_counts.items()
            if verb not in self.strong_action_verbs
        }

        return {
            'total_verbs': len(verbs),
            'unique_verbs': len(verb_counts),
            'strong_verbs': strong_verbs,
            'weak_verbs': weak_verbs,
            'strong_verb_ratio': len(strong_verbs) / len(verb_counts) if verb_counts else 0
        }

    def get_keyword_recommendations(
        self, resume_text: str, job_description: str = None
    ) -> List[str]:
        """Generate keyword recommendations"""
        recommendations = []

        # Analyze current keywords
        keywords = self.extract_keywords(resume_text)

        # Check if job description is provided
        if job_description:
            analysis = self.analyze_keywords_with_job(resume_text, job_description)

            if analysis['match_score'] < 60:
                recommendations.append(
                    f"Your keyword match score is {analysis['match_score']}%. "
                    "Consider adding more relevant keywords from the job description."
                )

            if analysis['missing_keywords']:
                top_missing = analysis['missing_keywords'][:5]
                recommendations.append(
                    f"Consider adding these important keywords: {', '.join(top_missing)}"
                )

        # Check action verbs
        verb_analysis = self.extract_action_verbs(resume_text)
        if verb_analysis['strong_verb_ratio'] < 0.3:
            recommendations.append(
                "Use more strong action verbs like 'achieved', 'implemented', 'led', 'developed'"
            )

        # Check keyword density
        keyword_list = [kw['keyword'] for kw in keywords]
        density = self.calculate_keyword_density(resume_text, keyword_list)

        if density < 2:
            recommendations.append(
                "Keyword density is low. Include more relevant technical and industry-specific terms."
            )
        elif density > 8:
            recommendations.append(
                "Keyword density is too high. Ensure natural flow and avoid keyword stuffing."
            )

        return recommendations
