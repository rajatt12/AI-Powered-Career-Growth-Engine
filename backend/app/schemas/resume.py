from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class ContactInfo(BaseModel):
    name: Optional[str] = Field(default=None, description="Candidate's full name")
    email: Optional[str] = Field(default=None, description="Primary email address")
    phone: Optional[str] = Field(default=None, description="Phone number with country code if available")
    location: Optional[str] = Field(default=None, description="City, State, Country")
    linkedin_url: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(default=None, description="GitHub profile URL")
    portfolio_url: Optional[str] = Field(default=None, description="Personal website or portfolio URL")

class SkillCategories(BaseModel):
    languages: List[str] = Field(default_factory=list, description="Programming languages (e.g. Python, TypeScript, Go, C++)")
    frameworks: List[str] = Field(default_factory=list, description="Web/Application frameworks (e.g. FastAPI, React, Node.js, Django)")
    databases_and_storage: List[str] = Field(default_factory=list, description="Databases & Caches (e.g. PostgreSQL, Redis, MongoDB, Elasticsearch)")
    cloud_and_devops: List[str] = Field(default_factory=list, description="Cloud, CI/CD, Containerization (e.g. AWS, Docker, Kubernetes, Terraform, GitHub Actions)")
    ai_and_ml: List[str] = Field(default_factory=list, description="Machine Learning, NLP, LLM tools (e.g. PyTorch, HuggingFace, LangChain, Sentence-Transformers)")
    tools_and_platforms: List[str] = Field(default_factory=list, description="Developer tools & OS (e.g. Git, Linux, Postman, Jira)")
    soft_skills: List[str] = Field(default_factory=list, description="Interpersonal & leadership skills (e.g. Agile, Team Mentorship, System Design)")

class WorkExperience(BaseModel):
    company: str = Field(description="Company or Organization name")
    role: str = Field(description="Job title / Designation")
    location: Optional[str] = Field(default=None, description="Location of the job (or Remote)")
    start_date: Optional[str] = Field(default=None, description="Start date (e.g. 'Jan 2022' or '2022')")
    end_date: Optional[str] = Field(default=None, description="End date (e.g. 'Present' or 'Dec 2023')")
    is_current: bool = Field(default=False, description="Whether the candidate currently works here")
    bullet_points: List[str] = Field(default_factory=list, description="Original or cleaned accomplishment bullet points")
    quantified_impacts: List[str] = Field(
        default_factory=list, 
        description="Specific achievements with measurable metrics (e.g. 'Reduced latency by 45%', 'Scaled service to 100k daily users')"
    )
    tech_stack: List[str] = Field(default_factory=list, description="Key technologies used in this specific role")

class ProjectItem(BaseModel):
    name: str = Field(description="Project title")
    description: str = Field(description="Summary of what the project does and its architecture")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies & libraries used in the project")
    github_url: Optional[str] = Field(default=None, description="Repository link")
    live_demo_url: Optional[str] = Field(default=None, description="Live deployment URL")
    quantified_impact: Optional[str] = Field(default=None, description="Measurable outcome or metric achieved by the project")

class EducationItem(BaseModel):
    institution: str = Field(description="University, College, or School name")
    degree: str = Field(description="Degree title (e.g. Bachelor of Technology, Master of Science)")
    field_of_study: Optional[str] = Field(default=None, description="Major / Specialization (e.g. Computer Science)")
    graduation_year: Optional[str] = Field(default=None, description="Year of graduation or expected graduation")
    gpa_or_grade: Optional[str] = Field(default=None, description="GPA or percentage if mentioned")

class ParsedResumeProfile(BaseModel):
    summary: str = Field(description="A concise 2-3 sentence professional executive summary of the candidate's core expertise")
    contact: ContactInfo = Field(default_factory=ContactInfo)
    skills: SkillCategories = Field(default_factory=SkillCategories)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list, description="Licenses, certifications, or major awards")
    total_experience_years: float = Field(default=0.0, description="Calculated or estimated total professional work experience in years")
    detected_seniority: str = Field(
        default="Entry-Level", 
        description="Estimated seniority level: Entry-Level (0-2 yrs), Mid-Level (2-5 yrs), Senior (5-8 yrs), Lead / Staff (8+ yrs)"
    )

# API Request / Response schemas
class ParseTextRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Raw text of the resume to parse")

class ParseResumeResponse(BaseModel):
    success: bool
    filename: Optional[str] = None
    extraction_method: str = "hybrid_layout_llm"
    profile: ParsedResumeProfile
    warnings: List[str] = Field(default_factory=list)
