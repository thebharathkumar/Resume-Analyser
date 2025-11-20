"""
ATS (Applicant Tracking System) Analyzer Service
Simulates how ATS systems parse and score resumes
"""
import re
from typing import Dict, List
import string


class ATSAnalyzer:
    """Simulate ATS parsing and compatibility checking"""

    def __init__(self):
        """Initialize ATS analyzer"""
        # Common formatting issues that ATS systems struggle with
        self.problematic_elements = {
            'tables': r'(\t.*\t)',
            'headers_footers': r'(page \d+|header|footer)',
            'columns': r'(.{50,}\s{10,}.{50,})',  # Wide spacing suggests columns
            'text_boxes': r'(\[.*\])',
            'special_chars': r'([^\w\s\-.,@:()/&])',
        }

        # ATS-friendly section headers
        self.standard_sections = {
            'work experience', 'experience', 'employment history',
            'education', 'skills', 'certifications', 'projects',
            'summary', 'objective', 'professional summary'
        }

    def analyze_ats_compatibility(
        self, text: str, file_type: str, metadata: Dict
    ) -> Dict:
        """Analyze resume's ATS compatibility"""

        # Initialize scores
        formatting_score = 100
        structure_score = 100
        issues = []
        recommendations = []

        # Check file format
        file_format_compatible = file_type.lower() in ['pdf', 'docx']
        if not file_format_compatible:
            formatting_score -= 30
            issues.append(f"File format '{file_type}' may not be ATS-compatible")
            recommendations.append("Use PDF or DOCX format for best ATS compatibility")

        # Check for tables (ATS systems often struggle with tables)
        if re.search(self.problematic_elements['tables'], text):
            formatting_score -= 15
            issues.append("Document contains tables which may confuse ATS")
            recommendations.append("Consider using simple text formatting instead of tables")

        # Check for complex formatting
        if re.search(self.problematic_elements['columns'], text):
            formatting_score -= 10
            issues.append("Multi-column layout detected")
            recommendations.append("Use single-column layout for better ATS parsing")

        # Check for standard section headers
        text_lower = text.lower()
        found_sections = [
            section for section in self.standard_sections
            if section in text_lower
        ]

        if len(found_sections) < 3:
            structure_score -= 20
            issues.append("Missing standard section headers")
            recommendations.append(
                "Include clear sections: Summary, Experience, Education, Skills"
            )

        # Check for excessive special characters
        special_char_count = len(re.findall(
            self.problematic_elements['special_chars'], text
        ))
        special_char_ratio = special_char_count / len(text) if text else 0

        if special_char_ratio > 0.02:  # More than 2% special characters
            formatting_score -= 10
            issues.append("High use of special characters")
            recommendations.append("Minimize use of special characters and symbols")

        # Check for bullet points (good for ATS)
        bullet_patterns = [r'•', r'▪', r'·', r'-\s', r'\*\s']
        has_bullets = any(re.search(pattern, text) for pattern in bullet_patterns)

        if not has_bullets:
            structure_score -= 10
            recommendations.append("Use bullet points to list achievements and responsibilities")

        # Check length (ATS preference)
        word_count = len(text.split())
        if word_count < 300:
            structure_score -= 15
            issues.append("Resume is too short")
            recommendations.append("Expand your resume to 400-800 words for optimal content")
        elif word_count > 1000:
            structure_score -= 10
            issues.append("Resume is very long")
            recommendations.append("Consider condensing to 1-2 pages (400-800 words)")

        # Check for contact information
        has_email = bool(re.search(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text
        ))
        has_phone = bool(re.search(
            r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text
        ))

        if not has_email:
            structure_score -= 15
            issues.append("No email address found")
            recommendations.append("Include a professional email address")

        if not has_phone:
            structure_score -= 10
            issues.append("No phone number found")
            recommendations.append("Include a contact phone number")

        # Check for dates in experience section
        date_pattern = r'\b(19|20)\d{2}\b|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}'
        date_count = len(re.findall(date_pattern, text))

        if date_count < 2:
            structure_score -= 10
            recommendations.append("Include dates for your experience and education")

        # Calculate overall ATS score
        overall_score = (formatting_score + structure_score) / 2

        # Keyword density check
        words = text.split()
        unique_words = set(word.lower().strip(string.punctuation) for word in words)
        keyword_density = (len(unique_words) / len(words) * 100) if words else 0

        if keyword_density < 30:
            recommendations.append("Increase variety of keywords and technical terms")

        return {
            'overall_score': round(max(0, overall_score), 2),
            'formatting_score': round(max(0, formatting_score), 2),
            'structure_score': round(max(0, structure_score), 2),
            'keyword_density': round(keyword_density, 2),
            'file_format_compatible': file_format_compatible,
            'issues': issues,
            'recommendations': recommendations,
            'found_sections': found_sections,
            'word_count': word_count
        }

    def simulate_ats_parsing(self, text: str) -> Dict:
        """Simulate how an ATS would parse the resume"""

        # Extract sections that ATS would identify
        sections = {}

        # Common section patterns
        section_headers = {
            'contact': r'(?:contact|personal\s+information)',
            'summary': r'(?:summary|objective|profile)',
            'experience': r'(?:experience|work\s+history|employment)',
            'education': r'(?:education|academic|qualifications?)',
            'skills': r'(?:skills|technical\s+skills|competencies)',
            'certifications': r'(?:certifications?|certificates?)',
        }

        lines = text.split('\n')
        current_section = None
        section_content = {key: [] for key in section_headers.keys()}

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Check if line is a section header
            for section, pattern in section_headers.items():
                if re.search(pattern, line_stripped, re.IGNORECASE):
                    if len(line_stripped.split()) <= 4:  # Short line, likely a header
                        current_section = section
                        break

            # Add content to current section
            if current_section and line_stripped:
                section_content[current_section].append(line_stripped)

        # Extract structured data
        parsed_data = {
            'sections_found': [k for k, v in section_content.items() if v],
            'contact_info': self._extract_contact_info(text),
            'dates_found': self._extract_dates(text),
            'education_degrees': self._extract_degrees(text),
            'company_names': self._extract_companies(text),
        }

        return parsed_data

    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        github_pattern = r'github\.com/[\w-]+'

        return {
            'emails': re.findall(email_pattern, text),
            'phones': re.findall(phone_pattern, text),
            'linkedin': re.findall(linkedin_pattern, text, re.IGNORECASE),
            'github': re.findall(github_pattern, text, re.IGNORECASE),
        }

    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        date_patterns = [
            r'\b(19|20)\d{2}\b',  # Years
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',  # Month Year
            r'\d{1,2}/\d{4}',  # MM/YYYY
        ]

        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text))

        return list(set(dates))

    def _extract_degrees(self, text: str) -> List[str]:
        """Extract education degrees"""
        degree_patterns = [
            r'\b(?:B\.?S\.?|Bachelor|B\.?A\.?|B\.?Tech|B\.?E\.?)\b',
            r'\b(?:M\.?S\.?|Master|M\.?A\.?|M\.?Tech|M\.?B\.?A\.?|M\.?E\.?)\b',
            r'\b(?:Ph\.?D\.?|Doctorate)\b',
        ]

        degrees = []
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            degrees.extend(matches)

        return list(set(degrees))

    def _extract_companies(self, text: str) -> List[str]:
        """Extract potential company names (simplified)"""
        # This is a simplified version - in production, you'd use NER
        lines = text.split('\n')
        companies = []

        # Look for lines with common company indicators
        company_indicators = ['Inc', 'LLC', 'Ltd', 'Corp', 'Corporation', 'Company']

        for line in lines:
            if any(indicator in line for indicator in company_indicators):
                # Extract the company name (simplified)
                companies.append(line.strip())

        return companies[:10]  # Limit to 10
