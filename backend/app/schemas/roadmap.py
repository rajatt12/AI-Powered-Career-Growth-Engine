from pydantic import BaseModel, Field
from typing import List, Optional
from .resume import ParsedResumeProfile

class CuratedResource(BaseModel):
    title: str = Field(description="Name of the resource or tutorial")
    url: str = Field(description="Direct URL to official documentation, tutorial, or course")
    resource_type: str = Field(description="'Documentation', 'Interactive Tutorial', 'Video', or 'GitHub Repo'")
    is_free: bool = Field(default=True)

class WeeklyMilestone(BaseModel):
    week_number: int = Field(description="Week number in the schedule (1, 2, 3...)")
    phase_name: str = Field(description="Phase theme (e.g. 'Foundations & Architecture', 'Caching & Queues', 'Capstone')")
    title: str = Field(description="Milestone title")
    objective: str = Field(description="Core learning objective for the week")
    estimated_hours: int = Field(description="Estimated study & build hours for this week")
    key_topics: List[str] = Field(description="Specific concepts and tools to master")
    curated_resources: List[CuratedResource] = Field(default_factory=list, description="Verified learning links")
    practical_coding_task: str = Field(description="Concrete hands-on mini-project or exercise to complete")
    interview_checkpoint_question: str = Field(
        description="A technical interview question to self-test mastery at the end of the week"
    )

class PersonalizedRoadmap(BaseModel):
    target_role_id: str
    target_role_title: str
    duration_weeks: int
    weekly_hours: int
    candidate_seniority: str
    mastered_prerequisites_skipped: List[str] = Field(
        description="Topics the candidate already knows that were pruned out to save time"
    )
    total_estimated_hours: int
    milestones: List[WeeklyMilestone]
    capstone_project_title: Optional[str] = None
    study_tips: List[str] = Field(default_factory=list)

class GenerateRoadmapRequest(BaseModel):
    profile: ParsedResumeProfile
    target_role_id: str = Field(description="Role ID (e.g. 'backend-engineer', 'ai-ml-engineer')")
    duration_weeks: int = Field(default=6, ge=2, le=16, description="Target timeline in weeks")
    available_hours_per_week: int = Field(default=10, ge=3, le=40, description="Weekly hours dedicated to studying")

class GenerateRoadmapResponse(BaseModel):
    success: bool
    roadmap: PersonalizedRoadmap
