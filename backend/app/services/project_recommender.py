import logging
import re
from typing import List, Set, Optional, Dict
from ..schemas.resume import ParsedResumeProfile
from ..schemas.projects import (
    ProjectTemplate, 
    ProjectRecommendation, 
    RecommendProjectsResponse
)
from ..schemas.role_match import RoleArchetype
from ..data.roles_taxonomy import TECH_ROLES_DATASET
from ..data.projects_dataset import PROJECTS_DATASET
from .matching_service import MatchingService, SKILL_ALIASES

logger = logging.getLogger(__name__)

class ProjectRecommenderService:
    """
    Content-Based Recommendation Engine:
    Maps a candidate's missing skill gaps for a target career role to
    high-impact, multi-skill production portfolio project blueprints.
    """

    def __init__(self, matching_service: Optional[MatchingService] = None):
        self.matching_service = matching_service or MatchingService()

    @staticmethod
    def _normalize_skill(skill: str) -> str:
        s = skill.lower().strip()
        s = re.sub(r'[\.\-_/]', '', s)
        if s.endswith("js") and len(s) > 4:
            s = s[:-2]
        return s

    def _is_skill_match(self, skill_a: str, skill_b: str) -> bool:
        """Fuzzy and alias match between two skill strings."""
        norm_a = self._normalize_skill(skill_a)
        norm_b = self._normalize_skill(skill_b)
        
        if norm_a == norm_b:
            return True
        if len(norm_a) >= 3 and len(norm_b) >= 3:
            if norm_a in norm_b or norm_b in norm_a:
                return True
                
        # Check alias dictionary
        a_lower = skill_a.lower()
        if a_lower in SKILL_ALIASES:
            for alias in SKILL_ALIASES[a_lower]:
                if self._normalize_skill(alias) == norm_b:
                    return True
                    
        return False

    def recommend_projects(
        self, 
        profile: ParsedResumeProfile, 
        target_role_id: str, 
        max_recommendations: int = 3
    ) -> RecommendProjectsResponse:
        """
        Calculates the candidate's skill gaps for the target role and recommends
        the top matching projects that eliminate those exact gaps.
        """
        # 1. Fetch Target Role
        role: Optional[RoleArchetype] = next(
            (r for r in TECH_ROLES_DATASET if r.id == target_role_id), 
            None
        )
        if not role:
            # Fallback to backend-engineer if ID not found
            role = TECH_ROLES_DATASET[0]

        # 2. Extract Candidate Skills & Skill Breakdown
        candidate_skills = self.matching_service._extract_all_candidate_skills(profile)
        breakdown = self.matching_service._compute_skill_breakdown(candidate_skills, role)
        
        all_missing_gaps = breakdown.missing_core_skills + breakdown.missing_preferred_skills

        recommendations: List[ProjectRecommendation] = []

        # 3. Score Each Project against the Candidate's Skill Gap
        for project in PROJECTS_DATASET:
            # Find which missing skills this project bridges
            bridged = []
            for missing in all_missing_gaps:
                for proj_skill in project.skills_covered:
                    if self._is_skill_match(missing, proj_skill):
                        bridged.append(missing)
                        break

            # Find skills candidate already knows that apply to this project
            known = []
            for cand_s in candidate_skills:
                for proj_skill in project.skills_covered:
                    if self._is_skill_match(cand_s, proj_skill):
                        known.append(cand_s)
                        break
            known = list(set(known))
            bridged = list(set(bridged))

            # Role target alignment bonus
            role_fit_bonus = 25.0 if role.id in project.target_roles else 0.0

            # Gap coverage score (0 - 55)
            gap_coverage_ratio = len(bridged) / max(1, len(all_missing_gaps))
            gap_score = min(55.0, gap_coverage_ratio * 55.0 + (len(bridged) * 10.0))

            # Known skills / Feasibility score (0 - 20)
            feasibility_score = min(20.0, (len(known) / max(1, len(project.skills_covered))) * 20.0)

            total_relevance = round(gap_score + role_fit_bonus + feasibility_score, 1)
            total_relevance = min(99.0, max(30.0, total_relevance))

            # Craft actionable why_recommended narrative
            if bridged:
                bridged_str = ", ".join(bridged[:3])
                why = f"Directly demonstrates {bridged_str} to recruiters for the {role.title} track while building on your existing {known[0] if known else 'software'} foundation."
            else:
                why = f"High-impact production portfolio architecture showcasing advanced full-lifecycle system design for {role.title} roles."

            recommendations.append(ProjectRecommendation(
                project=project,
                relevance_score=total_relevance,
                skills_bridged=bridged,
                skills_already_known=known[:4],
                why_recommended=why
            ))

        # Sort descending by relevance score
        recommendations.sort(key=lambda x: x.relevance_score, reverse=True)

        return RecommendProjectsResponse(
            success=True,
            target_role_id=role.id,
            target_role_title=role.title,
            total_missing_skills_targeted=all_missing_gaps,
            recommendations=recommendations[:max_recommendations]
        )
