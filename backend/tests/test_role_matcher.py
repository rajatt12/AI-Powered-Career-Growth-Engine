import pytest
from app.schemas.resume import ParsedResumeProfile, SkillCategories, ContactInfo, WorkExperience
from app.services.matching_service import MatchingService
from app.services.vector_store_service import VectorStoreService
from app.data.roles_taxonomy import TECH_ROLES_DATASET

@pytest.fixture
def sample_backend_profile():
    return ParsedResumeProfile(
        summary="Backend Software Engineer with 3 years experience building REST APIs, asynchronous workers, and database architectures.",
        contact=ContactInfo(name="Jordan Smith", email="jordan@example.com"),
        skills=SkillCategories(
            languages=["Python", "SQL", "Go"],
            frameworks=["FastAPI", "Django"],
            databases_and_storage=["PostgreSQL", "Redis"],
            cloud_and_devops=["Docker", "AWS", "Git"],
            ai_and_ml=[],
            tools_and_platforms=["Postman", "Linux"],
            soft_skills=["System Design", "Agile"]
        ),
        work_experience=[
            WorkExperience(
                company="TechCorp",
                role="Backend Developer",
                quantified_impacts=["Built FastAPI microservices handling 10k RPS", "Reduced database query latency by 40% with Redis"],
                tech_stack=["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"]
            )
        ],
        total_experience_years=3.0,
        detected_seniority="Mid-Level"
    )

@pytest.fixture
def sample_aiml_profile():
    return ParsedResumeProfile(
        summary="Machine Learning Engineer specializing in deep learning, PyTorch, LLMs, and RAG architectures.",
        contact=ContactInfo(name="Maya Lin", email="maya@example.com"),
        skills=SkillCategories(
            languages=["Python", "SQL", "C++"],
            frameworks=["PyTorch", "TensorFlow", "Scikit-Learn"],
            databases_and_storage=["ChromaDB", "PostgreSQL"],
            cloud_and_devops=["Docker", "Git"],
            ai_and_ml=["HuggingFace", "Transformers", "RAG", "LLMs", "Embeddings"],
            tools_and_platforms=["Jupyter", "Linux"],
            soft_skills=["Research", "Mathematical Modeling"]
        ),
        work_experience=[
            WorkExperience(
                company="AI Labs",
                role="AI Research Engineer",
                quantified_impacts=["Fine-tuned 7B parameter LLMs achieving 92% benchmark accuracy", "Built RAG retrieval pipeline with ChromaDB"],
                tech_stack=["Python", "PyTorch", "HuggingFace", "ChromaDB", "Docker"]
            )
        ],
        total_experience_years=2.5,
        detected_seniority="Mid-Level"
    )

def test_roles_taxonomy_loaded():
    assert len(TECH_ROLES_DATASET) >= 8
    role_ids = [r.id for r in TECH_ROLES_DATASET]
    assert "backend-engineer" in role_ids
    assert "ai-ml-engineer" in role_ids
    assert "fullstack-developer" in role_ids

def test_vector_store_seeding_and_search():
    vector_store = VectorStoreService()
    results = vector_store.search_matching_roles("FastAPI Python backend microservices PostgreSQL Redis", top_k=3)
    assert len(results) > 0
    top_role_id = results[0]["role"].id
    assert top_role_id in ["backend-engineer", "fullstack-developer"]

def test_matching_service_backend_candidate(sample_backend_profile):
    service = MatchingService()
    response = service.match_roles(sample_backend_profile, top_k=5)
    
    assert response.success is True
    assert len(response.top_matches) > 0
    
    top_match = response.top_matches[0]
    # The top match for a Python/FastAPI backend engineer should be Backend or Full-Stack
    assert top_match.role_id in ["backend-engineer", "fullstack-developer"]
    assert top_match.match_score_percentage > 60.0
    assert "Python" in top_match.key_strengths or "FastAPI" in top_match.key_strengths

def test_matching_service_aiml_candidate(sample_aiml_profile):
    service = MatchingService()
    response = service.match_roles(sample_aiml_profile, top_k=5)
    
    assert response.success is True
    top_match = response.top_matches[0]
    # The top match for a PyTorch/Transformers profile should be AI/ML or MLOps
    assert top_match.role_id in ["ai-ml-engineer", "mlops-engineer"]
    assert top_match.match_score_percentage > 60.0
    assert "PyTorch" in top_match.key_strengths or "Scikit-Learn" in top_match.key_strengths
