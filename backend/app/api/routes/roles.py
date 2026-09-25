from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ...schemas.role_match import MatchRolesRequest, MatchRolesResponse, RoleArchetype
from ...services.matching_service import MatchingService
from ...data.roles_taxonomy import TECH_ROLES_DATASET

router = APIRouter(prefix="/api/roles", tags=["Role Matching & Career Discovery"])

matching_service = MatchingService()

@router.get("/taxonomy", response_model=List[RoleArchetype])
def get_role_taxonomy(category: Optional[str] = Query(None, description="Filter roles by category")):
    """
    Returns the curated knowledge base of tech career tracks and requirements.
    """
    if category:
        return [r for r in TECH_ROLES_DATASET if r.category.lower() == category.lower()]
    return TECH_ROLES_DATASET

@router.get("/{role_id}", response_model=RoleArchetype)
def get_role_details(role_id: str):
    """
    Retrieves details, core skills, and market metrics for a specific role archetype.
    """
    role = next((r for r in TECH_ROLES_DATASET if r.id == role_id), None)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID '{role_id}' not found in career taxonomy."
        )
    return role

@router.post("/match", response_model=MatchRolesResponse)
def match_candidate_roles(payload: MatchRolesRequest):
    """
    Matches a parsed candidate profile against the ChromaDB vector store
    and returns top matching roles with hybrid scores and skill breakdowns.
    """
    try:
        response = matching_service.match_roles(
            profile=payload.profile,
            top_k=payload.top_k
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error matching roles: {str(e)}"
        )
