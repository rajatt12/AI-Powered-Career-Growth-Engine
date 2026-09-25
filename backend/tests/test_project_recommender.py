import pytest
from app.schemas.resume import ParsedResumeProfile, SkillCategories, ContactInfo, WorkExperience
from app.services.project_recommender import ProjectRecommenderService
from app.data.projects_dataset import PROJECTS_DATASET

@pytest.fixture
def backend_profile_with_gaps():
    # Has Python, FastAPI, PostgreSQL, Git, but missing Redis, Celery, Docker
    return ParsedResumeProfile(
        summary="Backend developer building standard CRUD APIs with Python and PostgreSQL.",
        contact=ContactInfo(name="Sam", email="sam@example.com"),
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
        total_experience_years=1.5,
        detected_seniority="Junior"
    )

@pytest.fixture
def aiml_profile_with_gaps():
    # Has Python, PyTorch, Scikit-Learn, but missing ChromaDB, RAG, Embeddings, Docker
    return ParsedResumeProfile(
        summary="AI researcher with background in PyTorch model training.",
        contact=ContactInfo(name="Elena", email="elena@example.com"),
        skills=SkillCategories(
            languages=["Python", "SQL"],
            frameworks=["PyTorch", "Scikit-Learn"],
            databases_and_storage=[],
            cloud_and_devops=["Git"],
            ai_and_ml=["Machine Learning", "Deep Learning"],
            tools_and_platforms=["Jupyter"],
            soft_skills=[]
        ),
        work_experience=[],
        total_experience_years=1.0,
        detected_seniority="Junior"
    )

def test_projects_dataset_integrity():
    assert len(PROJECTS_DATASET) >= 6
    for proj in PROJECTS_DATASET:
        assert proj.id
        assert proj.title
        assert len(proj.skills_covered) > 0
        assert len(proj.resume_bullet_points) > 0
        assert "graph" in proj.system_architecture_mermaid

def test_recommend_for_backend_gaps(backend_profile_with_gaps):
    service = ProjectRecommenderService()
    response = service.recommend_projects(
        profile=backend_profile_with_gaps,
        target_role_id="backend-engineer",
        max_recommendations=3
    )
    
    assert response.success is True
    assert len(response.recommendations) > 0
    
    # Top recommendation should target backend gaps (e.g. distributed-task-queue or ecommerce-rate-limited-api)
    top_rec = response.recommendations[0]
    assert top_rec.project.id in ["distributed-task-queue", "ecommerce-rate-limited-api", "realtime-collaborative-workspace"]
    assert len(top_rec.skills_bridged) > 0
    assert len(top_rec.project.resume_bullet_points) > 0

def test_recommend_for_aiml_gaps(aiml_profile_with_gaps):
    service = ProjectRecommenderService()
    response = service.recommend_projects(
        profile=aiml_profile_with_gaps,
        target_role_id="ai-ml-engineer",
        max_recommendations=3
    )
    
    assert response.success is True
    top_rec = response.recommendations[0]
    assert top_rec.project.id in ["production-rag-agent", "mlops-retraining-pipeline"]
    assert len(top_rec.skills_bridged) > 0
