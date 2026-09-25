from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ...schemas.projects import (
    RecommendProjectsRequest, 
    RecommendProjectsResponse, 
    ProjectTemplate
)
from ...services.project_recommender import ProjectRecommenderService
from ...data.projects_dataset import PROJECTS_DATASET

router = APIRouter(prefix="/api/projects", tags=["Project Recommendations & Portfolio Builder"])

recommender_service = ProjectRecommenderService()

@router.get("/catalog", response_model=List[ProjectTemplate])
def get_project_catalog(role_id: Optional[str] = Query(None, description="Filter projects by target role ID")):
    """
    Returns the curated catalog of production portfolio project blueprints.
    """
    if role_id:
        return [p for p in PROJECTS_DATASET if role_id.lower() in [r.lower() for r in p.target_roles]]
    return PROJECTS_DATASET

@router.get("/{project_id}", response_model=ProjectTemplate)
def get_project_details(project_id: str):
    """
    Retrieves full architectural specifications, Mermaid diagram, and XYZ resume bullets for a project.
    """
    project = next((p for p in PROJECTS_DATASET if p.id == project_id), None)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found in portfolio catalog."
        )
    return project

@router.post("/recommend", response_model=RecommendProjectsResponse)
def recommend_gap_closing_projects(payload: RecommendProjectsRequest):
    """
    Analyzes candidate's skill gaps against a target role and recommends the top
    production projects to eliminate those gaps and boost hiring odds.
    """
    try:
        response = recommender_service.recommend_projects(
            profile=payload.profile,
            target_role_id=payload.target_role_id,
            max_recommendations=payload.max_recommendations
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error recommending projects: {str(e)}"
        )
