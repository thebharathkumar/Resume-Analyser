"""
Document parsing service for extracting text from resumes
"""
import PyPDF2
import docx
import pdfplumber
from typing import Dict, Any
import re


class DocumentParser:
    """Parse resume documents and extract text and metadata"""

    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        """Parse PDF file and extract text"""
        text = ""
        metadata = {
            "page_count": 0,
            "method": "pdfplumber"
        }

        try:
            # Try pdfplumber first (better for formatted PDFs)
            with pdfplumber.open(file_path) as pdf:
                metadata["page_count"] = len(pdf.pages)
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # Fallback to PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    metadata["page_count"] = len(pdf_reader.pages)
                    metadata["method"] = "PyPDF2"
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                raise Exception(f"Failed to parse PDF: {str(e)}, {str(e2)}")

        return {
            "text": text.strip(),
            "metadata": metadata
        }

    @staticmethod
    def parse_docx(file_path: str) -> Dict[str, Any]:
        """Parse DOCX file and extract text"""
        try:
            doc = docx.Document(file_path)

            # Extract text from paragraphs
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += "\n" + cell.text

            metadata = {
                "page_count": len(doc.sections),
                "paragraphs": len(doc.paragraphs),
                "tables": len(doc.tables)
            }

            return {
                "text": text.strip(),
                "metadata": metadata
            }
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")

    @staticmethod
    def parse_document(file_path: str, file_type: str) -> Dict[str, Any]:
        """Parse document based on file type"""
        if file_type.lower() in ['pdf']:
            return DocumentParser.parse_pdf(file_path)
        elif file_type.lower() in ['docx', 'doc']:
            return DocumentParser.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Extract common resume sections"""
        sections = {}

        # Common section headers
        section_patterns = {
            'contact': r'(contact|personal information)',
            'summary': r'(summary|objective|profile|about)',
            'experience': r'(experience|work history|employment)',
            'education': r'(education|academic|qualification)',
            'skills': r'(skills|technical skills|competencies)',
            'projects': r'(projects|portfolio)',
            'certifications': r'(certifications|certificates|licenses)',
            'awards': r'(awards|achievements|honors)',
        }

        lines = text.split('\n')
        current_section = 'other'
        section_content = {key: [] for key in section_patterns.keys()}
        section_content['other'] = []

        for line in lines:
            line_lower = line.lower().strip()

            # Check if line is a section header
            matched = False
            for section, pattern in section_patterns.items():
                if re.search(pattern, line_lower) and len(line.split()) <= 5:
                    current_section = section
                    matched = True
                    break

            if not matched and line.strip():
                section_content[current_section].append(line)

        # Convert lists to strings
        sections = {k: '\n'.join(v).strip() for k, v in section_content.items() if v}

        return sections

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    @staticmethod
    def extract_emails(text: str) -> list:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)

    @staticmethod
    def extract_phone_numbers(text: str) -> list:
        """Extract phone numbers from text"""
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        return re.findall(phone_pattern, text)

    @staticmethod
    def extract_urls(text: str) -> list:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
