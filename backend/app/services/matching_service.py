import logging
import re
from typing import List, Set, Tuple, Optional, Dict
from ..schemas.resume import ParsedResumeProfile
from ..schemas.role_match import (
    RoleArchetype, 
    RoleMatchResult, 
    SkillMatchBreakdown, 
    MatchRolesResponse
)
from ..data.roles_taxonomy import TECH_ROLES_DATASET
from .vector_store_service import VectorStoreService

logger = logging.getLogger(__name__)

# Common skill equivalence aliases
SKILL_ALIASES: Dict[str, List[str]] = {
    "machine learning": ["ml", "deep learning", "ai", "artificial intelligence", "scikit-learn", "pytorch", "tensorflow"],
    "deep learning": ["neural networks", "pytorch", "tensorflow", "keras", "transformers"],
    "mathematics & statistics": ["statistics", "math", "probability", "mathematical modeling", "linear algebra"],
    "rest apis": ["rest", "api", "fastapi", "flask", "express", "graphql"],
    "responsive design": ["css", "html", "tailwind", "styled-components", "frontend"],
    "ci/cd": ["github actions", "jenkins", "gitlab ci", "ci/cd", "deployment"],
    "cloud (aws/gcp)": ["aws", "gcp", "azure", "cloud"],
    "vector databases": ["chromadb", "faiss", "qdrant", "pinecone", "milvus"],
    "llms": ["large language models", "transformers", "huggingface", "rag", "langchain", "gemini", "gpt"]
}

class MatchingService:
    """
    Hybrid Role Matching Engine:
    Combines Macro Vector Semantic Similarity (Dense Search) with
    Micro Skill-to-Requirement Exact & Fuzzy Overlap across all taxonomy roles.
    """

    def __init__(self, vector_store: Optional[VectorStoreService] = None):
        self.vector_store = vector_store or VectorStoreService()

    @staticmethod
    def _normalize_skill(skill: str) -> str:
        """Normalizes skill string for robust comparison."""
        s = skill.lower().strip()
        s = re.sub(r'[\.\-_/]', '', s)
        if s.endswith("js") and len(s) > 4:
            s = s[:-2]
        return s

    def _extract_all_candidate_skills(self, profile: ParsedResumeProfile) -> Set[str]:
        """Collects and flattens all skills extracted from the candidate profile."""
        skills = set()
        for s in profile.skills.languages:
            skills.add(s)
        for s in profile.skills.frameworks:
            skills.add(s)
        for s in profile.skills.databases_and_storage:
            skills.add(s)
        for s in profile.skills.cloud_and_devops:
            skills.add(s)
        for s in profile.skills.ai_and_ml:
            skills.add(s)
        for s in profile.skills.tools_and_platforms:
            skills.add(s)
        for s in profile.skills.soft_skills:
            skills.add(s)
            
        for exp in profile.work_experience:
            for tech in exp.tech_stack:
                skills.add(tech)

        for proj in profile.projects:
            for tech in proj.tech_stack:
                skills.add(tech)

        return skills

    def _is_skill_matched(self, required_skill: str, candidate_skills: Set[str]) -> bool:
        """Checks if a required skill is matched by candidate skills directly or via aliases."""
        norm_req = self._normalize_skill(required_skill)
        norm_candidate = {self._normalize_skill(s) for s in candidate_skills}

        # 1. Direct or substring match
        if norm_req in norm_candidate:
            return True
        for cand in norm_candidate:
            if (len(norm_req) >= 3 and norm_req in cand) or (len(cand) >= 3 and cand in norm_req):
                return True

        # 2. Alias match
        req_lower = required_skill.lower()
        if req_lower in SKILL_ALIASES:
            for alias in SKILL_ALIASES[req_lower]:
                norm_alias = self._normalize_skill(alias)
                if norm_alias in norm_candidate or any(norm_alias in c for c in norm_candidate):
                    return True

        return False

    def _synthesize_candidate_query(self, profile: ParsedResumeProfile) -> str:
        """
        Creates an enriched dense query representation from the candidate's resume.
        """
        all_skills = self._extract_all_candidate_skills(profile)
        
        exp_summaries = []
        for exp in profile.work_experience[:3]:
            bullets = " ".join(exp.quantified_impacts or exp.bullet_points[:2])
            exp_summaries.append(f"{exp.role} at {exp.company}: {bullets}")

        query_text = (
            f"Candidate Title: {profile.summary}. "
            f"Seniority: {profile.detected_seniority} with {profile.total_experience_years} years. "
            f"Skills: {' '.join(all_skills)}. "
            f"Experience: {' '.join(exp_summaries)}"
        )
        return query_text

    def _compute_skill_breakdown(self, candidate_skills: Set[str], role: RoleArchetype) -> SkillMatchBreakdown:
        """
        Computes exact and alias overlap between candidate skills and role requirements.
        """
        matched_core = []
        missing_core = []
        for req in role.required_skills:
            if self._is_skill_matched(req, candidate_skills):
                matched_core.append(req)
            else:
                missing_core.append(req)

        matched_pref = []
        missing_pref = []
        for pref in role.preferred_skills:
            if self._is_skill_matched(pref, candidate_skills):
                matched_pref.append(pref)
            else:
                missing_pref.append(pref)

        total_required = max(1, len(role.required_skills))
        overlap_ratio = len(matched_core) / total_required

        return SkillMatchBreakdown(
            matched_core_skills=matched_core,
            missing_core_skills=missing_core,
            matched_preferred_skills=matched_pref,
            missing_preferred_skills=missing_pref,
            overlap_ratio=round(overlap_ratio, 2)
        )

    def match_roles(self, profile: ParsedResumeProfile, top_k: int = 5) -> MatchRolesResponse:
        """
        Evaluates candidate profile across all roles in taxonomy:
        1. Dense Vector Search on ChromaDB (Macro Similarity)
        2. Granular Skill Gap Overlap (Micro Overlap)
        3. Calibrated Hybrid Scoring & Ranking
        """
        candidate_query = self._synthesize_candidate_query(profile)
        candidate_skills = self._extract_all_candidate_skills(profile)

        # Vector search for all roles
        vector_matches = self.vector_store.search_matching_roles(
            query_text=candidate_query, 
            top_k=len(TECH_ROLES_DATASET)
        )
        vector_score_map = {m["role"].id: m["similarity_score"] for m in vector_matches}

        results: List[RoleMatchResult] = []
        for role in TECH_ROLES_DATASET:
            vector_sim = vector_score_map.get(role.id, 50.0)

            # Compute granular skill breakdown
            breakdown = self._compute_skill_breakdown(candidate_skills, role)
            
            # Skill Score: Core coverage (80%) + Preferred bonus (20%)
            core_ratio = len(breakdown.matched_core_skills) / max(1, len(role.required_skills))
            pref_ratio = len(breakdown.matched_preferred_skills) / max(1, len(role.preferred_skills))
            
            skill_score = min(100.0, (core_ratio * 80.0) + (pref_ratio * 20.0))

            # Hybrid Score: 35% Vector Semantic + 65% Skill Requirements Fit
            hybrid_score = round((0.35 * vector_sim) + (0.65 * skill_score), 1)

            # Verdict
            if hybrid_score >= 75.0:
                verdict = "Strong Match"
            elif hybrid_score >= 60.0:
                verdict = "Good Match"
            elif hybrid_score >= 45.0:
                verdict = "Potential Match"
            else:
                verdict = "Pivot Candidate"

            results.append(RoleMatchResult(
                role_id=role.id,
                title=role.title,
                category=role.category,
                match_score_percentage=hybrid_score,
                vector_similarity_score=round(vector_sim, 1),
                skill_overlap_score=round(skill_score, 1),
                fit_verdict=verdict,
                key_strengths=breakdown.matched_core_skills + breakdown.matched_preferred_skills[:2],
                critical_gaps=breakdown.missing_core_skills,
                skill_breakdown=breakdown,
                salary_range=role.average_salary_range,
                market_demand=role.market_demand
            ))

        # Sort descending by hybrid match score
        results.sort(key=lambda x: x.match_score_percentage, reverse=True)

        return MatchRolesResponse(
            success=True,
            candidate_name=profile.contact.name,
            detected_seniority=profile.detected_seniority,
            top_matches=results[:top_k],
            total_roles_evaluated=len(TECH_ROLES_DATASET)
        )
