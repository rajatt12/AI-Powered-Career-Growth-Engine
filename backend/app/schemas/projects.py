from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .resume import ParsedResumeProfile

class ProjectTemplate(BaseModel):
    id: str = Field(description="Unique slug identifier (e.g. 'distributed-task-queue')")
    title: str = Field(description="Display title of the project")
    tagline: str = Field(description="One-sentence elevator pitch of what the project does")
    difficulty: str = Field(description="Beginner, Intermediate, Advanced")
    estimated_hours: int = Field(description="Estimated hours to build and deploy")
    target_roles: List[str] = Field(description="Role IDs this project is best suited for")
    skills_covered: List[str] = Field(description="Tech stack and tools mastered by building this project")
    architecture_overview: str = Field(description="High-level architectural summary")
    system_architecture_mermaid: str = Field(description="Mermaid.js diagram string of the system flow")
    core_features: List[str] = Field(description="Key functional modules to implement")
    database_models: List[str] = Field(description="Key database entities and schemas")
    resume_bullet_points: List[str] = Field(
        description="Google XYZ formula bullet points candidate can add to their resume"
    )
    github_starter_topics: List[str] = Field(default_factory=list)

class ProjectRecommendation(BaseModel):
    project: ProjectTemplate
    relevance_score: float = Field(description="Match score based on skill gap coverage (0 - 100%)")
    skills_bridged: List[str] = Field(description="Missing skills from the target role that this project eliminates")
    skills_already_known: List[str] = Field(description="Skills the candidate already has that apply to this project")
    why_recommended: str = Field(description="Actionable explanation of why this project boosts the candidate's hiring odds")

class RecommendProjectsRequest(BaseModel):
    profile: ParsedResumeProfile
    target_role_id: str = Field(description="Role ID from Phase 2 (e.g. 'backend-engineer', 'ai-ml-engineer')")
    max_recommendations: int = Field(default=3, ge=1, le=6)

class RecommendProjectsResponse(BaseModel):
    success: bool
    target_role_id: str
    target_role_title: str
    total_missing_skills_targeted: List[str]
    recommendations: List[ProjectRecommendation]
