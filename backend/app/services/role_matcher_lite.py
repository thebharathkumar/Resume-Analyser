"""
Lightweight role matching for Vercel
"""
import re
from typing import Dict, List, Set


class RoleMatcher:
    """Match resume against target roles without heavy NLP"""

    def __init__(self):
        """Initialize role matcher"""

        self.role_requirements = {
            'software_engineer': {
                'technical_skills': {
                    'python', 'java', 'javascript', 'c++', 'git', 'sql',
                    'algorithms', 'data structures', 'oop', 'api', 'rest'
                },
                'soft_skills': {
                    'problem solving', 'teamwork', 'communication'
                }
            },
            'data_scientist': {
                'technical_skills': {
                    'python', 'r', 'sql', 'machine learning', 'statistics',
                    'pandas', 'numpy', 'tensorflow', 'pytorch'
                },
                'soft_skills': {
                    'analytical', 'communication', 'presentation'
                }
            },
            'product_manager': {
                'technical_skills': {
                    'agile', 'scrum', 'jira', 'roadmap', 'analytics'
                },
                'soft_skills': {
                    'leadership', 'communication', 'stakeholder management'
                }
            },
            'frontend_developer': {
                'technical_skills': {
                    'javascript', 'typescript', 'react', 'vue', 'angular',
                    'html', 'css', 'sass'
                },
                'soft_skills': {
                    'attention to detail', 'creativity', 'collaboration'
                }
            }
        }

    def match_role(self, resume_text: str, target_role: str, job_description: str = None) -> Dict:
        """Match resume against target role"""

        role_key = target_role.lower().replace(' ', '_').replace('-', '_')

        if role_key not in self.role_requirements:
            return {
                'target_role': target_role,
                'match_percentage': 0,
                'matched_skills': [],
                'missing_skills': [],
                'experience_match': 50,
                'education_match': 50,
                'recommendations': ['Role template not found']
            }

        requirements = self.role_requirements[role_key]
        resume_lower = resume_text.lower()

        # Find matches
        matched_technical = self._find_matches(resume_lower, requirements['technical_skills'])
        matched_soft = self._find_matches(resume_lower, requirements['soft_skills'])

        missing_technical = requirements['technical_skills'] - matched_technical
        missing_soft = requirements['soft_skills'] - matched_soft

        # Calculate match
        total_required = len(requirements['technical_skills']) + len(requirements['soft_skills'])
        total_matched = len(matched_technical) + len(matched_soft)

        match_percentage = (total_matched / total_required * 100) if total_required > 0 else 0

        return {
            'target_role': target_role,
            'match_percentage': round(match_percentage, 2),
            'matched_skills': sorted(list(matched_technical | matched_soft)),
            'missing_skills': sorted(list(missing_technical | missing_soft))[:15],
            'experience_match': self._assess_experience(resume_text),
            'education_match': self._assess_education(resume_text),
            'recommendations': self._generate_recommendations(match_percentage, list(missing_technical)[:3])
        }

    def _find_matches(self, text: str, skills: Set[str]) -> Set[str]:
        """Find skill matches"""
        matched = set()
        for skill in skills:
            if skill in text:
                matched.add(skill)
        return matched

    def _assess_experience(self, text: str) -> float:
        """Basic experience assessment"""
        years = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', text.lower())
        max_years = max([int(y) for y in years]) if years else 0

        if max_years >= 5:
            return 90
        elif max_years >= 3:
            return 75
        elif max_years >= 1:
            return 60
        return 50

    def _assess_education(self, text: str) -> float:
        """Basic education assessment"""
        text_lower = text.lower()

        if any(word in text_lower for word in ['phd', 'doctorate']):
            return 100
        elif any(word in text_lower for word in ['master', 'm.s.', 'm.a.']):
            return 90
        elif any(word in text_lower for word in ['bachelor', 'b.s.', 'b.a.']):
            return 80
        return 50

    def _generate_recommendations(self, match_pct: float, missing: List[str]) -> List[str]:
        """Generate recommendations"""
        recs = []

        if match_pct < 50:
            recs.append(f"Match is {match_pct:.0f}%. Consider gaining more relevant skills.")

        if missing:
            recs.append(f"Add these skills: {', '.join(missing)}")

        if match_pct >= 70:
            recs.append("Strong match! Emphasize relevant achievements.")

        return recs
