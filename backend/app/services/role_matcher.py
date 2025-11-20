"""
Role matching service for comparing resume to target job roles
"""
import re
from typing import Dict, List, Set
from collections import Counter
import spacy


class RoleMatcher:
    """Match resume content against target job roles"""

    def __init__(self):
        """Initialize role matcher"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise Exception(
                "spaCy model not found. Please run: python -m spacy download en_core_web_sm"
            )

        # Define common skills and requirements by role category
        self.role_requirements = {
            'software_engineer': {
                'technical_skills': {
                    'python', 'java', 'javascript', 'c++', 'git', 'sql',
                    'algorithms', 'data structures', 'oop', 'api', 'rest',
                    'testing', 'debugging', 'version control'
                },
                'soft_skills': {
                    'problem solving', 'teamwork', 'communication',
                    'analytical', 'collaborative'
                },
                'experience_keywords': {
                    'developed', 'implemented', 'designed', 'built',
                    'created', 'optimized', 'software', 'application'
                }
            },
            'data_scientist': {
                'technical_skills': {
                    'python', 'r', 'sql', 'machine learning', 'statistics',
                    'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn',
                    'data analysis', 'visualization', 'tableau', 'power bi'
                },
                'soft_skills': {
                    'analytical', 'communication', 'business acumen',
                    'storytelling', 'presentation'
                },
                'experience_keywords': {
                    'analyzed', 'modeled', 'predicted', 'visualized',
                    'insights', 'data', 'metrics', 'statistical'
                }
            },
            'product_manager': {
                'technical_skills': {
                    'agile', 'scrum', 'jira', 'roadmap', 'analytics',
                    'sql', 'a/b testing', 'metrics', 'kpi'
                },
                'soft_skills': {
                    'leadership', 'communication', 'stakeholder management',
                    'strategic thinking', 'prioritization', 'cross-functional'
                },
                'experience_keywords': {
                    'led', 'managed', 'launched', 'defined', 'prioritized',
                    'product', 'feature', 'stakeholder', 'strategy'
                }
            },
            'frontend_developer': {
                'technical_skills': {
                    'javascript', 'typescript', 'react', 'vue', 'angular',
                    'html', 'css', 'sass', 'webpack', 'responsive design',
                    'ui/ux', 'accessibility'
                },
                'soft_skills': {
                    'attention to detail', 'creativity', 'collaboration',
                    'user-focused'
                },
                'experience_keywords': {
                    'developed', 'implemented', 'designed', 'ui', 'interface',
                    'responsive', 'component', 'web'
                }
            },
            'backend_developer': {
                'technical_skills': {
                    'python', 'java', 'node.js', 'sql', 'nosql', 'api',
                    'rest', 'graphql', 'microservices', 'docker', 'aws',
                    'database design', 'scalability'
                },
                'soft_skills': {
                    'problem solving', 'analytical', 'systematic',
                    'attention to detail'
                },
                'experience_keywords': {
                    'designed', 'implemented', 'api', 'database', 'server',
                    'backend', 'scalable', 'performance'
                }
            },
            'devops_engineer': {
                'technical_skills': {
                    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
                    'jenkins', 'ci/cd', 'linux', 'bash', 'python', 'ansible',
                    'monitoring', 'automation'
                },
                'soft_skills': {
                    'problem solving', 'collaboration', 'reliability',
                    'systematic'
                },
                'experience_keywords': {
                    'automated', 'deployed', 'configured', 'infrastructure',
                    'pipeline', 'monitoring', 'cloud', 'containerization'
                }
            }
        }

    def match_role(
        self, resume_text: str, target_role: str, job_description: str = None
    ) -> Dict:
        """Match resume against a target role"""

        # Normalize role name
        role_key = target_role.lower().replace(' ', '_').replace('-', '_')

        # Get role requirements
        if role_key in self.role_requirements:
            requirements = self.role_requirements[role_key]
        else:
            # If role not in predefined list, extract from job description
            if job_description:
                requirements = self._extract_requirements_from_jd(job_description)
            else:
                return {
                    'target_role': target_role,
                    'match_percentage': 0,
                    'error': 'Unknown role and no job description provided',
                    'matched_skills': [],
                    'missing_skills': [],
                    'recommendations': []
                }

        # Extract skills from resume
        resume_lower = resume_text.lower()
        resume_doc = self.nlp(resume_lower)

        # Find matched skills
        matched_technical = self._find_matches(
            resume_lower,
            requirements.get('technical_skills', set())
        )

        matched_soft = self._find_matches(
            resume_lower,
            requirements.get('soft_skills', set())
        )

        matched_experience = self._find_matches(
            resume_lower,
            requirements.get('experience_keywords', set())
        )

        # Find missing skills
        missing_technical = requirements.get('technical_skills', set()) - matched_technical
        missing_soft = requirements.get('soft_skills', set()) - matched_soft

        # Calculate match percentage
        total_required = (
            len(requirements.get('technical_skills', set())) +
            len(requirements.get('soft_skills', set()))
        )

        total_matched = len(matched_technical) + len(matched_soft)

        if total_required > 0:
            match_percentage = (total_matched / total_required) * 100
        else:
            match_percentage = 0

        # Calculate sub-scores
        tech_total = len(requirements.get('technical_skills', set()))
        tech_matched = len(matched_technical)
        tech_score = (tech_matched / tech_total * 100) if tech_total > 0 else 0

        soft_total = len(requirements.get('soft_skills', set()))
        soft_matched = len(matched_soft)
        soft_score = (soft_matched / soft_total * 100) if soft_total > 0 else 0

        # Analyze experience level
        experience_match = self._assess_experience_match(
            resume_text, matched_experience
        )

        # Analyze education match
        education_match = self._assess_education_match(resume_text, target_role)

        # Generate recommendations
        recommendations = self._generate_role_recommendations(
            target_role,
            list(missing_technical),
            list(missing_soft),
            match_percentage
        )

        return {
            'target_role': target_role,
            'match_percentage': round(match_percentage, 2),
            'matched_skills': sorted(list(matched_technical | matched_soft)),
            'missing_skills': sorted(list(missing_technical | missing_soft))[:15],
            'technical_match': round(tech_score, 2),
            'soft_skills_match': round(soft_score, 2),
            'experience_match': round(experience_match, 2),
            'education_match': round(education_match, 2),
            'experience_keywords_found': sorted(list(matched_experience)),
            'recommendations': recommendations
        }

    def _find_matches(self, text: str, skills: Set[str]) -> Set[str]:
        """Find skill matches in text"""
        matched = set()

        for skill in skills:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text):
                matched.add(skill)

        return matched

    def _extract_requirements_from_jd(self, job_description: str) -> Dict:
        """Extract requirements from job description"""
        jd_lower = job_description.lower()
        doc = self.nlp(jd_lower)

        # Extract noun chunks as potential skills
        technical_skills = set()
        soft_skills = set()

        # Common soft skill indicators
        soft_skill_keywords = {
            'leadership', 'communication', 'teamwork', 'collaborative',
            'analytical', 'problem solving', 'creative', 'organized'
        }

        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()

            # Check if it's a soft skill
            if any(soft in chunk_text for soft in soft_skill_keywords):
                soft_skills.add(chunk_text)
            elif len(chunk_text) > 2:  # Minimum length
                technical_skills.add(chunk_text)

        return {
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'experience_keywords': set()
        }

    def _assess_experience_match(
        self, resume_text: str, matched_keywords: Set[str]
    ) -> float:
        """Assess experience level match"""

        # Extract years of experience
        year_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?',
        ]

        years_found = []
        for pattern in year_patterns:
            matches = re.findall(pattern, resume_text.lower())
            years_found.extend([int(m) for m in matches])

        # Get maximum years mentioned
        max_years = max(years_found) if years_found else 0

        # Score based on experience indicators
        score = 50  # Base score

        if max_years >= 5:
            score += 30
        elif max_years >= 3:
            score += 20
        elif max_years >= 1:
            score += 10

        # Bonus for strong experience keywords
        if len(matched_keywords) > 5:
            score += 20
        elif len(matched_keywords) > 2:
            score += 10

        return min(100, score)

    def _assess_education_match(self, resume_text: str, role: str) -> float:
        """Assess education match for role"""

        resume_lower = resume_text.lower()

        # Define education levels
        has_phd = bool(re.search(r'\bph\.?d\.?\b|\bdoctorate\b', resume_lower))
        has_masters = bool(re.search(
            r'\bm\.?s\.?\b|\bmaster[s\']?\b|\bm\.?tech\b|\bm\.?b\.?a\.?\b',
            resume_lower
        ))
        has_bachelors = bool(re.search(
            r'\bb\.?s\.?\b|\bbachelor[s\']?\b|\bb\.?tech\b|\bb\.?e\.?\b|\bb\.?a\.?\b',
            resume_lower
        ))

        # Score based on role requirements
        role_lower = role.lower()

        # Research/PhD-level roles
        if 'research' in role_lower or 'scientist' in role_lower:
            if has_phd:
                return 100
            elif has_masters:
                return 80
            elif has_bachelors:
                return 60
            else:
                return 40

        # Most professional roles
        else:
            if has_bachelors or has_masters or has_phd:
                return 100
            else:
                return 50  # Experience might compensate

    def _generate_role_recommendations(
        self,
        role: str,
        missing_technical: List[str],
        missing_soft: List[str],
        match_percentage: float
    ) -> List[str]:
        """Generate recommendations for role matching"""
        recommendations = []

        if match_percentage < 50:
            recommendations.append(
                f"Your profile matches {match_percentage:.0f}% with {role}. "
                "Consider gaining more relevant skills or highlighting existing ones better."
            )

        if missing_technical:
            top_missing = missing_technical[:5]
            recommendations.append(
                f"Key technical skills to add: {', '.join(top_missing)}"
            )

        if missing_soft:
            top_soft = missing_soft[:3]
            recommendations.append(
                f"Highlight these soft skills if you have them: {', '.join(top_soft)}"
            )

        if match_percentage >= 70:
            recommendations.append(
                f"Strong match for {role}! Consider tailoring your resume further by "
                "emphasizing relevant projects and achievements."
            )

        return recommendations
