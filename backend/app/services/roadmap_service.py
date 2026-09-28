import logging
from typing import List, Optional, Dict
from ..schemas.resume import ParsedResumeProfile
from ..schemas.roadmap import (
    PersonalizedRoadmap, 
    WeeklyMilestone, 
    CuratedResource, 
    GenerateRoadmapResponse
)
from ..schemas.role_match import RoleArchetype
from ..data.roles_taxonomy import TECH_ROLES_DATASET
from ..data.roadmap_curriculum import ROLE_CURRICULUM_DATABASE
from .matching_service import MatchingService
from .project_recommender import ProjectRecommenderService

logger = logging.getLogger(__name__)

class RoadmapService:
    """
    AI Career Architect & Roadmap Generator:
    Takes candidate's target career role, extracted skills, and available weekly hours,
    prunes mastered prerequisites, and synthesizes a structured, time-boxed week-by-week
    curriculum grounded in vetted resources, practical coding tasks, and capstone projects.
    """

    def __init__(
        self, 
        matching_service: Optional[MatchingService] = None,
        project_recommender: Optional[ProjectRecommenderService] = None
    ):
        self.matching_service = matching_service or MatchingService()
        self.project_recommender = project_recommender or ProjectRecommenderService(self.matching_service)

    def generate_roadmap(
        self, 
        profile: ParsedResumeProfile, 
        target_role_id: str, 
        duration_weeks: int = 6, 
        available_hours_per_week: int = 10
    ) -> GenerateRoadmapResponse:
        """
        Generates a tailored, week-by-week learning roadmap with pruned prerequisites.
        """
        # 1. Fetch Target Role
        role: Optional[RoleArchetype] = next(
            (r for r in TECH_ROLES_DATASET if r.id == target_role_id), 
            TECH_ROLES_DATASET[0]
        )

        # 2. Extract Candidate Skills & Gaps
        candidate_skills = self.matching_service._extract_all_candidate_skills(profile)
        breakdown = self.matching_service._compute_skill_breakdown(candidate_skills, role)

        # 3. Fetch Curriculum Nodes for this Role (or fallback)
        curriculum_nodes = ROLE_CURRICULUM_DATABASE.get(
            role.id, 
            ROLE_CURRICULUM_DATABASE["backend-engineer"]
        )

        # 4. Prune Mastered Prerequisites
        pruned_skills = []
        active_nodes = []
        for node in curriculum_nodes:
            # Check if candidate already knows ALL target skills in this node
            node_skills = node.get("skills_targeted", [])
            is_mastered = False
            if node_skills:
                matching_count = sum(1 for s in node_skills if self.matching_service._is_skill_matched(s, candidate_skills))
                if matching_count == len(node_skills) and len(node_skills) > 0 and node != curriculum_nodes[-1]:
                    is_mastered = True

            if is_mastered:
                pruned_skills.extend(node_skills)
            else:
                active_nodes.append(node)

        if not active_nodes:
            active_nodes = curriculum_nodes

        # 5. Get Top Recommended Capstone Project for the Finale
        project_rec = self.project_recommender.recommend_projects(
            profile=profile,
            target_role_id=role.id,
            max_recommendations=1
        )
        capstone_title = project_rec.recommendations[0].project.title if project_rec.recommendations else "Distributed System Architecture Capstone"

        # 6. Map Active Curriculum Nodes to Weekly Milestones
        milestones: List[WeeklyMilestone] = []
        total_nodes = len(active_nodes)
        
        for week_idx in range(1, duration_weeks + 1):
            # Select appropriate node for this week
            node_idx = min(int(((week_idx - 1) / duration_weeks) * total_nodes), total_nodes - 1)
            node = active_nodes[node_idx]

            # Custom weekly task for the final week: Capstone submission
            if week_idx == duration_weeks:
                task = f"Deploy and publish your Capstone Project: '{capstone_title}' with complete README, live demo, and automated test suite."
                phase = "Capstone Project Deployment & Portfolio Polish"
                title = f"Final Capstone: {capstone_title}"
            else:
                task = node["practical_task"]
                phase = node["phase"]
                title = f"Week {week_idx}: {node['title']}"

            milestones.append(WeeklyMilestone(
                week_number=week_idx,
                phase_name=phase,
                title=title,
                objective=node["objective"],
                estimated_hours=available_hours_per_week,
                key_topics=node["key_topics"],
                curated_resources=node["resources"],
                practical_coding_task=task,
                interview_checkpoint_question=node["interview_question"]
            ))

        # 7. Actionable Study & Interview Tips
        study_tips = [
            f"Commit code daily to GitHub. Recruiters evaluate consistency as much as complexity.",
            f"Write a 3-paragraph LinkedIn / Dev.to technical post summarizing your findings for each weekly milestone.",
            f"Use the interview checkpoint questions to practice answering technical concepts aloud using the STAR method.",
            f"Dedicate {int(available_hours_per_week * 0.7)} hrs to hands-on coding and {int(available_hours_per_week * 0.3)} hrs to reading official docs."
        ]

        roadmap = PersonalizedRoadmap(
            target_role_id=role.id,
            target_role_title=role.title,
            duration_weeks=duration_weeks,
            weekly_hours=available_hours_per_week,
            candidate_seniority=profile.detected_seniority,
            mastered_prerequisites_skipped=list(set(pruned_skills)),
            total_estimated_hours=duration_weeks * available_hours_per_week,
            milestones=milestones,
            capstone_project_title=capstone_title,
            study_tips=study_tips
        )

        return GenerateRoadmapResponse(
            success=True,
            roadmap=roadmap
        )
