"""
Grammar and text strength analysis service
"""
import re
from typing import List, Dict
import language_tool_python
from collections import defaultdict


class GrammarAnalyzer:
    """Analyze grammar and text strength"""

    def __init__(self):
        """Initialize grammar checker"""
        # Initialize LanguageTool for grammar checking
        # Note: First run will download language models
        self.tool = language_tool_python.LanguageTool('en-US')

        # Strong action verbs for resume writing
        self.strong_verbs = {
            'achieved', 'accomplished', 'advanced', 'analyzed', 'built',
            'created', 'decreased', 'delivered', 'demonstrated', 'designed',
            'developed', 'directed', 'eliminated', 'enhanced', 'established',
            'exceeded', 'executed', 'expanded', 'generated', 'implemented',
            'improved', 'increased', 'initiated', 'launched', 'led',
            'managed', 'optimized', 'orchestrated', 'organized', 'pioneered',
            'reduced', 'resolved', 'restructured', 'spearheaded', 'streamlined',
            'strengthened', 'transformed', 'accelerated', 'engineered', 'architected'
        }

        # Weak/overused verbs to avoid
        self.weak_verbs = {
            'was', 'were', 'did', 'made', 'got', 'had', 'worked',
            'helped', 'responsible for', 'duties included', 'handled'
        }

        # Power words that add impact
        self.power_words = {
            'strategic', 'innovative', 'collaborative', 'results-driven',
            'data-driven', 'cross-functional', 'scalable', 'robust',
            'comprehensive', 'cutting-edge', 'award-winning', 'proven'
        }

        # Filler words to avoid
        self.filler_words = {
            'very', 'really', 'quite', 'just', 'actually', 'basically',
            'literally', 'definitely', 'probably', 'maybe'
        }

    def analyze_grammar(self, text: str) -> Dict:
        """Perform comprehensive grammar analysis"""

        # Check grammar using LanguageTool
        matches = self.tool.check(text)

        # Categorize issues
        issues_by_severity = defaultdict(list)
        issues_by_type = defaultdict(list)

        for match in matches:
            issue = {
                'message': match.message,
                'context': match.context,
                'offset': match.offset,
                'length': match.errorLength,
                'rule_id': match.ruleId,
                'suggestions': match.replacements[:3],  # Top 3 suggestions
                'category': match.category
            }

            # Categorize by severity
            if 'TYPOS' in match.ruleId or 'GRAMMAR' in match.ruleId:
                severity = 'error'
            elif 'STYLE' in match.ruleId:
                severity = 'warning'
            else:
                severity = 'info'

            issue['severity'] = severity
            issues_by_severity[severity].append(issue)
            issues_by_type[match.category].append(issue)

        # Calculate grammar score
        total_issues = len(matches)
        word_count = len(text.split())

        # Score based on errors per 100 words
        if word_count > 0:
            error_rate = (total_issues / word_count) * 100
            # Perfect score: 0 errors, Score decreases with more errors
            grammar_score = max(0, 100 - (error_rate * 10))
        else:
            grammar_score = 0

        return {
            'total_issues': total_issues,
            'grammar_score': round(grammar_score, 2),
            'issues_by_severity': {
                'errors': issues_by_severity.get('error', []),
                'warnings': issues_by_severity.get('warning', []),
                'info': issues_by_severity.get('info', [])
            },
            'issues_by_type': dict(issues_by_type),
            'all_issues': [
                {
                    'message': m.message,
                    'context': m.context,
                    'offset': m.offset,
                    'length': m.errorLength,
                    'rule_id': m.ruleId,
                    'suggestions': m.replacements[:3],
                    'severity': self._determine_severity(m)
                }
                for m in matches
            ]
        }

    def _determine_severity(self, match) -> str:
        """Determine severity of grammar issue"""
        if 'TYPOS' in match.ruleId or 'GRAMMAR' in match.ruleId:
            return 'error'
        elif 'STYLE' in match.ruleId:
            return 'warning'
        return 'info'

    def analyze_text_strength(self, text: str) -> Dict:
        """Analyze the strength and impact of resume text"""

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

            # Analyze this line
            strength_score = 50  # Start neutral
            issues = []
            suggestions = []
            category = 'medium'

            # Check for strong action verbs
            strong_verb_count = sum(
                1 for verb in self.strong_verbs if verb in line_lower
            )
            if strong_verb_count > 0:
                strength_score += 20
                overall_stats['strong_verbs_count'] += strong_verb_count

            # Check for weak verbs
            weak_verb_count = sum(
                1 for verb in self.weak_verbs if verb in line_lower
            )
            if weak_verb_count > 0:
                strength_score -= 15
                overall_stats['weak_verbs_count'] += weak_verb_count
                issues.append("Contains weak verbs")
                suggestions.append("Replace weak verbs with strong action verbs")

            # Check for power words
            power_word_count = sum(
                1 for word in self.power_words if word in line_lower
            )
            if power_word_count > 0:
                strength_score += 10
                overall_stats['power_words_count'] += power_word_count

            # Check for filler words
            filler_count = sum(
                1 for word in self.filler_words if word in line_lower
            )
            if filler_count > 0:
                strength_score -= 10
                overall_stats['filler_words_count'] += filler_count
                issues.append("Contains filler words")
                suggestions.append("Remove unnecessary filler words")

            # Check for quantified achievements (numbers/percentages)
            has_numbers = bool(re.search(r'\d+%|\$\d+|\d+\+', line))
            if has_numbers:
                strength_score += 15
                overall_stats['quantified_achievements'] += 1
            elif len(line.split()) > 5 and not has_numbers:
                issues.append("No quantified achievements")
                suggestions.append("Add numbers, percentages, or metrics to show impact")

            # Check for passive voice
            passive_indicators = ['was', 'were', 'been', 'being']
            if any(word in line_lower.split() for word in passive_indicators):
                strength_score -= 10
                issues.append("Possible passive voice")
                suggestions.append("Use active voice for stronger impact")

            # Determine category
            if strength_score >= 70:
                category = 'strong'
            elif strength_score <= 40:
                category = 'weak'

            # Ensure score is in valid range
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

        # Calculate overall strength score
        if text_strengths:
            overall_strength = sum(ts['strength_score'] for ts in text_strengths) / len(text_strengths)
        else:
            overall_strength = 0

        return {
            'text_strengths': text_strengths,
            'overall_strength_score': round(overall_strength, 2),
            'statistics': overall_stats,
            'recommendations': self._generate_strength_recommendations(overall_stats)
        }

    def _generate_strength_recommendations(self, stats: Dict) -> List[str]:
        """Generate recommendations based on text strength analysis"""
        recommendations = []

        if stats['weak_verbs_count'] > stats['strong_verbs_count']:
            recommendations.append(
                "Use more strong action verbs like 'achieved', 'implemented', 'led' instead of weak verbs"
            )

        if stats['quantified_achievements'] < 3:
            recommendations.append(
                "Add more quantified achievements with numbers, percentages, and metrics"
            )

        if stats['filler_words_count'] > 5:
            recommendations.append(
                "Remove filler words like 'very', 'really', 'just' to make your resume more concise"
            )

        if stats['power_words_count'] < 2:
            recommendations.append(
                "Include more power words like 'strategic', 'innovative', 'data-driven' to enhance impact"
            )

        return recommendations

    def create_heatmap_data(self, text: str) -> Dict:
        """Create heatmap data for visualization"""

        # Get grammar analysis
        grammar_result = self.analyze_grammar(text)

        # Get strength analysis
        strength_result = self.analyze_text_strength(text)

        # Split text into sections for heatmap
        sections = []
        lines = text.split('\n')

        for i, line in enumerate(lines):
            if line.strip():
                # Find corresponding strength data
                strength_data = next(
                    (ts for ts in strength_result['text_strengths'] if ts['text'] == line.strip()),
                    None
                )

                # Count grammar issues in this line
                line_issues = [
                    issue for issue in grammar_result['all_issues']
                    if line.strip() in issue['context']
                ]

                sections.append({
                    'line_number': i + 1,
                    'text': line.strip(),
                    'strength_score': strength_data['strength_score'] if strength_data else 50,
                    'grammar_issues_count': len(line_issues),
                    'category': strength_data['category'] if strength_data else 'medium'
                })

        return {
            'sections': sections,
            'text_strengths': strength_result['text_strengths'],
            'grammar_issues': grammar_result['all_issues'],
            'overall_grammar_score': grammar_result['grammar_score']
        }

    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'tool'):
            self.tool.close()
