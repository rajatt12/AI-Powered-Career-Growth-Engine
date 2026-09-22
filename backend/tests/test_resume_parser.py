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
- Cloud & DevOps: AWS (ECS, S3), Docker, Kubernetes, CI/CD, Terraform
- AI/ML: PyTorch, HuggingFace, Embeddings
- Tools: Git, Linux, Postman

Work Experience:
Senior Backend Engineer | CloudScale Inc | 2022 - Present
- Architected asynchronous event pipeline using FastAPI and Redis, reducing latency by 45% for 2M daily requests.
- Optimized PostgreSQL database queries, reducing AWS RDS CPU utilization by 30% and saving $18,000 annually.
- Mentored 4 junior engineers on distributed systems and clean architecture principles.

Software Engineer | DevMatrix | 2020 - 2022
- Developed RESTful APIs with Python and Flask, serving 50,000 active users.
- Containerized 12 core services using Docker and orchestrated deployments on AWS ECS.

Education:
Bachelor of Science in Computer Science | University of California, Berkeley | 2020
"""

def test_regex_contact_extraction():
    contacts = RegexParser.extract_contacts(SAMPLE_RESUME_TEXT)
    assert contacts.email == "alex.chen@example.com"
    assert contacts.github_url == "https://github.com/alexchen"
    assert contacts.linkedin_url == "https://linkedin.com/in/alexchen-dev"
    assert "Alex Chen" in contacts.name

def test_resume_service_pipeline():
    service = ResumeService()
    result = service.parse_raw_text(SAMPLE_RESUME_TEXT)
    
    assert result.success is True
    assert isinstance(result.profile, ParsedResumeProfile)
    assert result.profile.contact.email == "alex.chen@example.com"
    
    # Verify categorized skills
    all_extracted_skills = (
        result.profile.skills.languages + 
        result.profile.skills.frameworks + 
        result.profile.skills.databases_and_storage +
        result.profile.skills.cloud_and_devops
    )
    # Check that key skills are captured
    assert any("Python" in s or "python" in s.lower() for s in all_extracted_skills)
    assert any("FastAPI" in s or "fastapi" in s.lower() for s in all_extracted_skills)

def test_quantified_metrics_detection():
    service = ResumeService()
    result = service.parse_raw_text(SAMPLE_RESUME_TEXT)
    
    # In fallback or LLM mode, quantified impact points should be extracted
    assert len(result.profile.work_experience) > 0
    work = result.profile.work_experience[0]
    assert len(work.quantified_impacts) > 0
