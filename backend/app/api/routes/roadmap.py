from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ...schemas.roadmap import (
    GenerateRoadmapRequest, 
    GenerateRoadmapResponse
)
from ...services.roadmap_service import RoadmapService
from ...data.roadmap_curriculum import ROLE_CURRICULUM_DATABASE

router = APIRouter(prefix="/api/roadmap", tags=["Personalized Roadmap & Learning Planner"])

roadmap_service = RoadmapService()

@router.get("/curriculum/{role_id}")
def get_role_curriculum(role_id: str):
    """
    Returns the foundational curriculum knowledge base nodes for a specific tech track.
    """
    curriculum = ROLE_CURRICULUM_DATABASE.get(role_id.lower())
    if not curriculum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curriculum not found for role '{role_id}'."
        )
    return {
        "role_id": role_id,
        "total_modules": len(curriculum),
        "modules": curriculum
    }

@router.post("/generate", response_model=GenerateRoadmapResponse)
def generate_personalized_roadmap(payload: GenerateRoadmapRequest):
    """
    Generates a personalized, time-boxed learning roadmap with pruned prerequisites,
    vetted learning links, practical coding exercises, and a capstone finale.
    """
    try:
        response = roadmap_service.generate_roadmap(
            profile=payload.profile,
            target_role_id=payload.target_role_id,
            duration_weeks=payload.duration_weeks,
            available_hours_per_week=payload.available_hours_per_week
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating roadmap: {str(e)}"
        )
