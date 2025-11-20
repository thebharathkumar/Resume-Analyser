"""
Readability scoring service for resume analysis
"""
import textstat
from typing import Dict, List
import re


class ReadabilityScorer:
    """Calculate various readability metrics for resume text"""

    def __init__(self):
        """Initialize readability scorer"""
        pass

    def calculate_readability(self, text: str) -> Dict:
        """Calculate comprehensive readability scores"""

        # Clean text for analysis
        cleaned_text = self._clean_text(text)

        # Calculate various readability metrics
        flesch_reading_ease = textstat.flesch_reading_ease(cleaned_text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(cleaned_text)
        gunning_fog = textstat.gunning_fog(cleaned_text)
        smog_index = textstat.smog_index(cleaned_text)
        automated_readability_index = textstat.automated_readability_index(cleaned_text)
        coleman_liau_index = textstat.coleman_liau_index(cleaned_text)

        # Calculate overall score (0-100)
        # Flesch Reading Ease is already 0-100, higher is better
        # For resumes, we want moderate difficulty (college level)
        # Target: 50-70 on Flesch Reading Ease

        # Normalize scores
        overall_score = self._calculate_overall_score(
            flesch_reading_ease,
            flesch_kincaid_grade,
            gunning_fog
        )

        # Generate interpretation
        interpretation = self._interpret_scores(flesch_reading_ease, overall_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            flesch_reading_ease,
            flesch_kincaid_grade,
            gunning_fog,
            cleaned_text
        )

        return {
            'flesch_reading_ease': round(flesch_reading_ease, 2),
            'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
            'gunning_fog': round(gunning_fog, 2),
            'smog_index': round(smog_index, 2),
            'automated_readability_index': round(automated_readability_index, 2),
            'coleman_liau_index': round(coleman_liau_index, 2),
            'overall_score': round(overall_score, 2),
            'interpretation': interpretation,
            'recommendations': recommendations,
            'metrics': self._get_text_metrics(text)
        }

    def _clean_text(self, text: str) -> str:
        """Clean text for readability analysis"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters that might interfere with analysis
        # but keep sentence-ending punctuation
        text = re.sub(r'[^\w\s.,!?;:-]', '', text)

        return text.strip()

    def _calculate_overall_score(
        self, flesch_reading_ease: float, fk_grade: float, gunning_fog: float
    ) -> float:
        """Calculate overall readability score (0-100)"""

        # For resumes, ideal Flesch Reading Ease is 50-70 (college level)
        # Penalize if too easy or too hard
        if 50 <= flesch_reading_ease <= 70:
            flesch_score = 100
        elif flesch_reading_ease < 50:
            # Too difficult
            flesch_score = max(0, 100 - (50 - flesch_reading_ease) * 2)
        else:
            # Too easy
            flesch_score = max(0, 100 - (flesch_reading_ease - 70) * 1.5)

        # For FK Grade, ideal is 10-14 (high school to college)
        if 10 <= fk_grade <= 14:
            fk_score = 100
        elif fk_grade < 10:
            fk_score = 80
        else:
            fk_score = max(0, 100 - (fk_grade - 14) * 5)

        # For Gunning Fog, ideal is 12-16
        if 12 <= gunning_fog <= 16:
            fog_score = 100
        elif gunning_fog < 12:
            fog_score = 85
        else:
            fog_score = max(0, 100 - (gunning_fog - 16) * 5)

        # Weight the scores
        overall = (flesch_score * 0.5) + (fk_score * 0.25) + (fog_score * 0.25)

        return overall

    def _interpret_scores(self, flesch_score: float, overall_score: float) -> str:
        """Interpret readability scores"""

        if overall_score >= 80:
            return "Excellent readability for a professional resume. Clear and well-structured."
        elif overall_score >= 60:
            return "Good readability. Your resume is appropriately professional and clear."
        elif overall_score >= 40:
            if flesch_score < 50:
                return "Moderate readability. Text may be too complex. Consider simplifying some sentences."
            else:
                return "Moderate readability. Text may be too simple. Add more professional terminology."
        else:
            if flesch_score < 30:
                return "Low readability. Resume is too complex and may be difficult to scan quickly. Simplify your writing."
            else:
                return "Low readability. Resume may lack professional depth. Add more specific technical content."

    def _generate_recommendations(
        self, flesch: float, fk_grade: float, gunning_fog: float, text: str
    ) -> List[str]:
        """Generate readability improvement recommendations"""
        recommendations = []

        # Check Flesch Reading Ease
        if flesch < 40:
            recommendations.append(
                "Simplify complex sentences. Break long sentences into shorter ones."
            )
            recommendations.append(
                "Reduce use of complex words where possible without sacrificing professionalism."
            )
        elif flesch > 80:
            recommendations.append(
                "Consider using more professional and technical terminology appropriate to your field."
            )

        # Check grade level
        if fk_grade > 14:
            recommendations.append(
                f"Reading grade level is {fk_grade:.1f}. Consider simplifying to 12-14 grade level for better ATS compatibility."
            )

        if gunning_fog > 16:
            recommendations.append(
                "Gunning Fog index is high. Reduce sentence complexity and use of polysyllabic words."
            )

        # Check sentence length
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0

        if avg_sentence_length > 25:
            recommendations.append(
                f"Average sentence length is {avg_sentence_length:.1f} words. Aim for 15-20 words per sentence."
            )
        elif avg_sentence_length < 10:
            recommendations.append(
                "Sentences are very short. Consider combining related ideas for better flow."
            )

        # Check word variety
        words = text.lower().split()
        unique_words = set(words)
        if len(words) > 0:
            variety_ratio = len(unique_words) / len(words)
            if variety_ratio < 0.3:
                recommendations.append(
                    "Low word variety detected. Use more diverse vocabulary to avoid repetition."
                )

        if not recommendations:
            recommendations.append(
                "Your resume has good readability for professional audiences."
            )

        return recommendations

    def _get_text_metrics(self, text: str) -> Dict:
        """Get basic text metrics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]

        # Count syllables (simplified)
        total_syllables = textstat.syllable_count(text)

        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_words_per_sentence': round(len(words) / len(sentences), 2) if sentences else 0,
            'avg_syllables_per_word': round(total_syllables / len(words), 2) if words else 0,
            'character_count': len(text),
            'unique_words': len(set(word.lower() for word in words))
        }

    def assess_hiring_manager_readability(self, text: str) -> Dict:
        """
        Assess how easily a hiring manager can scan and read the resume
        """
        metrics = {}

        # Calculate basic readability
        readability = self.calculate_readability(text)

        # Assess scanability
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]

        # Check for bullet points (easier to scan)
        bullet_count = sum(
            1 for line in lines
            if line.strip().startswith(('•', '-', '*', '▪', '·'))
        )

        # Check for section headers (easier navigation)
        section_headers = [
            'experience', 'education', 'skills', 'summary',
            'objective', 'projects', 'certifications'
        ]
        header_count = sum(
            1 for line in lines
            if any(header in line.lower() for header in section_headers)
            and len(line.split()) <= 4
        )

        # Calculate scanability score
        scanability_score = 50  # Base score

        if bullet_count > 5:
            scanability_score += 20
        elif bullet_count > 0:
            scanability_score += 10

        if header_count >= 4:
            scanability_score += 20
        elif header_count >= 2:
            scanability_score += 10

        # Check average line length (shorter is easier to scan)
        avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0

        if avg_line_length < 80:
            scanability_score += 10

        # White space ratio
        empty_lines = len(lines) - len(non_empty_lines)
        whitespace_ratio = empty_lines / len(lines) if lines else 0

        if 0.1 <= whitespace_ratio <= 0.3:  # Good white space
            scanability_score += 10

        # Combine with readability score
        hiring_manager_score = (
            readability['overall_score'] * 0.6 +
            scanability_score * 0.4
        )

        return {
            'hiring_manager_score': round(hiring_manager_score, 2),
            'scanability_score': round(scanability_score, 2),
            'readability_score': readability['overall_score'],
            'bullet_points': bullet_count,
            'section_headers': header_count,
            'avg_line_length': round(avg_line_length, 2),
            'whitespace_ratio': round(whitespace_ratio * 100, 2),
            'recommendations': self._generate_scanability_recommendations(
                bullet_count, header_count, whitespace_ratio
            )
        }

    def _generate_scanability_recommendations(
        self, bullets: int, headers: int, whitespace: float
    ) -> List[str]:
        """Generate recommendations for better scanability"""
        recommendations = []

        if bullets < 3:
            recommendations.append(
                "Add bullet points to highlight achievements and make content easier to scan."
            )

        if headers < 3:
            recommendations.append(
                "Add clear section headers (Experience, Education, Skills) for better organization."
            )

        if whitespace < 0.1:
            recommendations.append(
                "Add more white space between sections for improved readability."
            )
        elif whitespace > 0.3:
            recommendations.append(
                "Reduce excessive white space to fit more content."
            )

        if not recommendations:
            recommendations.append(
                "Resume is well-formatted for hiring manager review."
            )

        return recommendations
