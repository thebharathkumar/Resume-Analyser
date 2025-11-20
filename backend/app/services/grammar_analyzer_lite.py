"""
Simplified grammar analyzer for Vercel
Uses basic pattern matching instead of LanguageTool
"""
import re
from typing import List, Dict
from collections import defaultdict


class GrammarAnalyzer:
    """Lightweight grammar and text strength analysis"""

    def __init__(self):
        """Initialize analyzer"""

        self.strong_verbs = {
            'achieved', 'accomplished', 'advanced', 'analyzed', 'built',
            'created', 'decreased', 'delivered', 'demonstrated', 'designed',
            'developed', 'directed', 'eliminated', 'enhanced', 'established',
            'exceeded', 'executed', 'expanded', 'generated', 'implemented',
            'improved', 'increased', 'initiated', 'launched', 'led',
            'managed', 'optimized', 'orchestrated', 'organized', 'pioneered'
        }

        self.weak_verbs = {
            'was', 'were', 'did', 'made', 'got', 'had', 'worked',
            'helped', 'responsible', 'duties'
        }

        self.power_words = {
            'strategic', 'innovative', 'collaborative', 'results-driven',
            'data-driven', 'cross-functional', 'scalable', 'robust'
        }

        self.filler_words = {
            'very', 'really', 'quite', 'just', 'actually', 'basically'
        }

    def analyze_grammar(self, text: str) -> Dict:
        """Basic grammar analysis"""

        issues = []

        # Check for common issues
        # Double spaces
        if '  ' in text:
            issues.append({
                'message': 'Extra spaces found',
                'context': 'Multiple consecutive spaces',
                'severity': 'info',
                'suggestions': ['Remove extra spaces']
            })

        # Check sentences end with punctuation
        sentences = text.split('\n')
        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if sent and len(sent) > 10:
                if not sent[-1] in '.!?;:':
                    issues.append({
                        'message': 'Sentence may be missing punctuation',
                        'context': sent[:50],
                        'severity': 'warning',
                        'suggestions': ['Add period at end']
                    })

        # Calculate basic grammar score
        total_issues = len(issues)
        word_count = len(text.split())

        if word_count > 0:
            error_rate = (total_issues / word_count) * 100
            grammar_score = max(0, 100 - (error_rate * 10))
        else:
            grammar_score = 0

        return {
            'total_issues': total_issues,
            'grammar_score': round(grammar_score, 2),
            'all_issues': issues[:20]  # Limit to 20
        }

    def analyze_text_strength(self, text: str) -> Dict:
        """Analyze text strength"""

        lines = text.split('\n')
        text_strengths = []
        overall_stats = {
            'strong_verbs_count': 0,
            'weak_verbs_count': 0,
            'power_words_count': 0,
            'filler_words_count': 0,
            'quantified_achievements': 0,
        }

        position = 0

        for line in lines:
            if not line.strip():
                position += len(line) + 1
                continue

            line_lower = line.lower()
            strength_score = 50
            issues = []
            suggestions = []

            # Check for strong verbs
            strong_count = sum(1 for v in self.strong_verbs if v in line_lower)
            if strong_count > 0:
                strength_score += 20
                overall_stats['strong_verbs_count'] += strong_count

            # Check for weak verbs
            weak_count = sum(1 for v in self.weak_verbs if v in line_lower)
            if weak_count > 0:
                strength_score -= 15
                overall_stats['weak_verbs_count'] += weak_count
                issues.append("Contains weak verbs")

            # Check for numbers/metrics
            has_numbers = bool(re.search(r'\d+%|\$\d+|\d+\+', line))
            if has_numbers:
                strength_score += 15
                overall_stats['quantified_achievements'] += 1

            # Check for power words
            power_count = sum(1 for w in self.power_words if w in line_lower)
            if power_count > 0:
                strength_score += 10
                overall_stats['power_words_count'] += power_count

            # Check for filler words
            filler_count = sum(1 for w in self.filler_words if w in line_lower)
            if filler_count > 0:
                strength_score -= 10
                overall_stats['filler_words_count'] += filler_count
                issues.append("Contains filler words")

            # Determine category
            if strength_score >= 70:
                category = 'strong'
            elif strength_score <= 40:
                category = 'weak'
            else:
                category = 'medium'

            strength_score = max(0, min(100, strength_score))

            text_strengths.append({
                'text': line.strip(),
                'start_pos': position,
                'end_pos': position + len(line),
                'strength_score': round(strength_score, 2),
                'category': category,
                'issues': issues,
                'suggestions': suggestions
            })

            position += len(line) + 1

        overall_strength = sum(ts['strength_score'] for ts in text_strengths) / len(text_strengths) if text_strengths else 0

        return {
            'text_strengths': text_strengths,
            'overall_strength_score': round(overall_strength, 2),
            'statistics': overall_stats
        }

    def create_heatmap_data(self, text: str) -> Dict:
        """Create heatmap data"""

        grammar_result = self.analyze_grammar(text)
        strength_result = self.analyze_text_strength(text)

        sections = []
        lines = text.split('\n')

        for i, line in enumerate(lines):
            if line.strip():
                strength_data = next(
                    (ts for ts in strength_result['text_strengths'] if ts['text'] == line.strip()),
                    None
                )

                sections.append({
                    'line_number': i + 1,
                    'text': line.strip(),
                    'strength_score': strength_data['strength_score'] if strength_data else 50,
                    'grammar_issues_count': 0,
                    'category': strength_data['category'] if strength_data else 'medium'
                })

        return {
            'sections': sections,
            'text_strengths': strength_result['text_strengths'],
            'grammar_issues': grammar_result['all_issues'],
            'overall_grammar_score': grammar_result['grammar_score']
        }
