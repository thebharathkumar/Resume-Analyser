"""
Lightweight keyword analyzer for Vercel deployment
Uses pattern matching instead of spaCy to reduce bundle size
"""
import re
from collections import Counter
from typing import List, Dict, Set


class KeywordAnalyzer:
    """Analyze keywords without heavy NLP dependencies"""

    def __init__(self):
        """Initialize with predefined skill categories"""

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

        # Strong action verbs
        self.strong_action_verbs = {
            'achieved', 'improved', 'increased', 'decreased', 'developed',
            'created', 'implemented', 'designed', 'launched', 'led', 'managed',
            'optimized', 'streamlined', 'delivered', 'built', 'engineered',
            'architected', 'spearheaded', 'pioneered', 'transformed', 'accelerated'
        }

    def extract_keywords(self, text: str, max_keywords: int = 50) -> List[Dict]:
        """Extract important keywords from text using pattern matching"""
        text_lower = text.lower()
        words = re.findall(r'\b[a-z][a-z.+#]{2,}\b', text_lower)

        # Also extract multi-word phrases
        phrases = []
        for category, skills in self.skill_categories.items():
            for skill in skills:
                if ' ' in skill and skill in text_lower:
                    phrases.append(skill)

        # Count occurrences
        word_counts = Counter(words + phrases)

        # Filter and categorize
        keywords = []
        for word, count in word_counts.most_common(max_keywords * 2):
            if len(word) >= 3 and not self._is_common_word(word):
                category = self._categorize_keyword(word)
                if category or count > 1:  # Include if categorized or mentioned multiple times
                    keywords.append({
                        'keyword': word,
                        'count': count,
                        'category': category if category else 'general'
                    })

        return keywords[:max_keywords]

    def _is_common_word(self, word: str) -> bool:
        """Check if word is too common"""
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'your', 'our', 'their', 'my', 'his', 'her', 'its'
        }
        return word.lower() in common_words

    def _categorize_keyword(self, keyword: str) -> str:
        """Categorize a keyword into skill category"""
        keyword_lower = keyword.lower()

        for category, skills in self.skill_categories.items():
            if keyword_lower in skills or any(skill in keyword_lower for skill in skills):
                return category

        return 'general'

    def analyze_keywords_with_job(self, resume_text: str, job_description: str) -> Dict:
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
            'missing_keywords': list(missing)[:20],
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
        text_lower = text.lower()
        words = re.findall(r'\b[a-z]+\b', text_lower)

        # Count verbs
        verb_counts = Counter(words)

        # Categorize as strong or weak
        strong_verbs = {
            verb: count for verb, count in verb_counts.items()
            if verb in self.strong_action_verbs
        }

        return {
            'total_verbs': len(words),
            'unique_verbs': len(verb_counts),
            'strong_verbs': strong_verbs,
            'strong_verb_ratio': len(strong_verbs) / len(verb_counts) if verb_counts else 0
        }

    def get_keyword_recommendations(
        self, resume_text: str, job_description: str = None
    ) -> List[str]:
        """Generate keyword recommendations"""
        recommendations = []

        keywords = self.extract_keywords(resume_text)

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
                    f"Consider adding these keywords: {', '.join(top_missing)}"
                )

        # Check action verbs
        verb_analysis = self.extract_action_verbs(resume_text)
        if verb_analysis['strong_verb_ratio'] < 0.3:
            recommendations.append(
                "Use more strong action verbs like 'achieved', 'implemented', 'led'"
            )

        # Check keyword density
        keyword_list = [kw['keyword'] for kw in keywords]
        density = self.calculate_keyword_density(resume_text, keyword_list)

        if density < 2:
            recommendations.append(
                "Keyword density is low. Include more relevant technical terms."
            )
        elif density > 8:
            recommendations.append(
                "Keyword density is high. Ensure natural flow, avoid keyword stuffing."
            )

        return recommendations
