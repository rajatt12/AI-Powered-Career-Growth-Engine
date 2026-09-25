from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .resume import ParsedResumeProfile

class RoleArchetype(BaseModel):
    id: str = Field(description="Unique slug identifier (e.g. 'backend-engineer')")
    title: str = Field(description="Display title of the role")
    category: str = Field(description="Broad category (e.g. 'Software Engineering', 'AI & Data')")
    description: str = Field(description="Comprehensive role summary and core responsibilities")
    required_skills: List[str] = Field(description="Mandatory / Core technical skills")
    preferred_skills: List[str] = Field(description="Nice-to-have / Advanced skills")
    typical_tools: List[str] = Field(description="Frameworks, databases, and DevOps tools used")
    experience_levels: List[str] = Field(default=["Junior", "Mid-Level", "Senior"])
    market_demand: str = Field(default="High", description="High, Very High, Steady")
    average_salary_range: str = Field(default="$90,000 - $160,000")

class SkillMatchBreakdown(BaseModel):
    matched_core_skills: List[str] = Field(default_factory=list, description="Core required skills the candidate has")
    missing_core_skills: List[str] = Field(default_factory=list, description="Core required skills the candidate is missing")
    matched_preferred_skills: List[str] = Field(default_factory=list, description="Bonus/preferred skills the candidate has")
    missing_preferred_skills: List[str] = Field(default_factory=list, description="Bonus/preferred skills the candidate is missing")
    overlap_ratio: float = Field(default=0.0, description="Fraction of required skills covered (0.0 - 1.0)")

class RoleMatchResult(BaseModel):
    role_id: str
    title: str
    category: str
    match_score_percentage: float = Field(description="Final hybrid match score (0 - 100%)")
    vector_similarity_score: float = Field(description="Semantic macro fit (0 - 100%)")
    skill_overlap_score: float = Field(description="Hard skill micro fit (0 - 100%)")
    fit_verdict: str = Field(description="'Strong Match' (>80%), 'Good Match' (65-80%), 'Potential Match' (50-65%), or 'Pivot Candidate' (<50%)")
    key_strengths: List[str] = Field(default_factory=list, description="Standout skills candidate already possesses for this role")
    critical_gaps: List[str] = Field(default_factory=list, description="Top skills needed to be job-ready")
    skill_breakdown: SkillMatchBreakdown
    salary_range: str
    market_demand: str

class MatchRolesRequest(BaseModel):
    profile: ParsedResumeProfile
    top_k: int = Field(default=5, ge=1, le=15, description="Number of top matching roles to return")

class MatchRolesResponse(BaseModel):
    success: bool
    candidate_name: Optional[str] = None
    detected_seniority: str
    top_matches: List[RoleMatchResult]
    total_roles_evaluated: int
