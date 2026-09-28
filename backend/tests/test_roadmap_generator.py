import pytest
from app.schemas.resume import ParsedResumeProfile, SkillCategories, ContactInfo, WorkExperience
from app.services.roadmap_service import RoadmapService
from app.data.roadmap_curriculum import ROLE_CURRICULUM_DATABASE

@pytest.fixture
def backend_learner_profile():
    # Knows Python, FastAPI, PostgreSQL, but lacks Redis, Celery, Docker, System Design
    return ParsedResumeProfile(
        summary="Junior backend developer proficient in Python and FastAPI.",
        contact=ContactInfo(name="Alex", email="alex@example.com"),
        skills=SkillCategories(
            languages=["Python", "SQL"],
            frameworks=["FastAPI"],
            databases_and_storage=["PostgreSQL"],
            cloud_and_devops=["Git"],
            ai_and_ml=[],
            tools_and_platforms=["Postman"],
            soft_skills=[]
        ),
        work_experience=[],
        total_experience_years=1.0,
        detected_seniority="Junior"
    )

def test_roadmap_curriculum_loaded():
    assert "backend-engineer" in ROLE_CURRICULUM_DATABASE
    assert "ai-ml-engineer" in ROLE_CURRICULUM_DATABASE
    assert len(ROLE_CURRICULUM_DATABASE["backend-engineer"]) >= 4

def test_generate_backend_roadmap(backend_learner_profile):
    service = RoadmapService()
    response = service.generate_roadmap(
        profile=backend_learner_profile,
        target_role_id="backend-engineer",
        duration_weeks=6,
        available_hours_per_week=12
    )

    assert response.success is True
    roadmap = response.roadmap
    assert roadmap.duration_weeks == 6
    assert roadmap.weekly_hours == 12
    assert roadmap.total_estimated_hours == 72
    assert len(roadmap.milestones) == 6

    # Verify milestone details
    week1 = roadmap.milestones[0]
    assert week1.week_number == 1
    assert len(week1.key_topics) > 0
    assert len(week1.curated_resources) > 0
    assert week1.practical_coding_task
    assert week1.interview_checkpoint_question

    # Final week should feature Capstone Project
    week6 = roadmap.milestones[5]
    assert "Capstone" in week6.phase_name or "Capstone" in week6.title
    assert roadmap.capstone_project_title is not None
