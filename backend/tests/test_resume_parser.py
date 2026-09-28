import pytest
from app.parsers.regex_parser import RegexParser
from app.parsers.file_extractor import FileExtractor
from app.services.resume_service import ResumeService
from app.schemas.resume import ParsedResumeProfile

SAMPLE_RESUME_TEXT = """
Alex Chen
Email: alex.chen@example.com | Phone: (415) 555-0199 | San Francisco, CA
LinkedIn: https://linkedin.com/in/alexchen-dev | GitHub: https://github.com/alexchen

Summary:
Full-Stack Engineer with 4 years of experience building high-throughput microservices and real-time streaming platforms.

Skills:
- Languages: Python, TypeScript, Go, SQL
- Frameworks: FastAPI, React, Node.js, Next.js
- Databases: PostgreSQL, Redis, MongoDB
- Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Terraform
- AI/ML: PyTorch, HuggingFace, Embeddings
- Tools: Git, Linux, Postman

Work Experience:
Senior Backend Engineer | CloudScale Inc | 2022 - Present
- Architected asynchronous event pipeline using FastAPI and Redis, reducing latency by 45% for 2M daily requests.
- Optimized PostgreSQL database queries, reducing AWS RDS CPU utilization by 30% and saving $18,000 annually.

Education:
Bachelor of Science in Computer Science | UC Berkeley | 2020
"""

def test_regex_contact_extraction():
    contacts = RegexParser.extract_contacts(SAMPLE_RESUME_TEXT)
    assert contacts.email == "alex.chen@example.com"
    assert contacts.github_url == "https://github.com/alexchen"
    assert contacts.linkedin_url == "https://linkedin.com/in/alexchen-dev"
    assert "Alex Chen" in contacts.name

def test_company_header_ignored_for_name():
    text_with_company_header = """
    HOSHO DIGITAL PVT. LTD.
    INTERNSHIP TRAINING REPORT
    RAJATVEER SINGH PASRICHA
    rajatveer1234@gmail.com | +91 9425654989
    Summary: Aspiring AI/ML Engineer and Data Analyst with experience in Python and SQL.
    """
    contacts = RegexParser.extract_contacts(text_with_company_header)
    assert contacts.name == "Rajatveer Singh Pasricha"
    assert contacts.email == "rajatveer1234@gmail.com"

def test_resume_service_pipeline():
    service = ResumeService()
    result = service.parse_raw_text(SAMPLE_RESUME_TEXT)
    
    assert result.success is True
    assert isinstance(result.profile, ParsedResumeProfile)
    assert result.profile.contact.email == "alex.chen@example.com"
    assert len(result.profile.summary.split()) <= 60
