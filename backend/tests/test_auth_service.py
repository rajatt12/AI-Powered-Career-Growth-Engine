import pytest
import uuid
from app.services.auth_service import AuthService

def test_user_registration_and_login():
    rand_id = uuid.uuid4().hex[:8]
    email = f"testuser_{rand_id}@example.com"
    password = "secretpassword123"
    name = "Test Developer"

    # Register
    success, msg, data = AuthService.register_user(email, password, name)
    assert success is True
    assert data["email"] == email
    assert data["token"] is not None

    # Login
    success, msg, login_data = AuthService.authenticate_user(email, password)
    assert success is True
    assert login_data["user_id"] == data["user_id"]
    assert login_data["full_name"] == name

def test_save_and_retrieve_user_state():
    rand_id = uuid.uuid4().hex[:8]
    email = f"state_user_{rand_id}@example.com"
    password = "secretpassword123"
    name = "State User"

    success, msg, data = AuthService.register_user(email, password, name)
    assert success is True
    user_id = data["user_id"]

    sample_profile = {"summary": "Experienced engineer", "skills": {"languages": ["Python"]}}
    sample_roadmap = {"duration_weeks": 6, "total_estimated_hours": 60}
    completed_weeks = [1, 2]

    # Save state
    ok = AuthService.save_user_state(
        user_id=user_id,
        profile=sample_profile,
        target_role_id="ai-ml-engineer",
        roadmap=sample_roadmap,
        completed_weeks=completed_weeks
    )
    assert ok is True

    # Retrieve state
    user_state = AuthService.get_user_by_id(user_id)
    assert user_state is not None
    assert user_state["state"]["target_role_id"] == "ai-ml-engineer"
    assert user_state["state"]["completed_weeks"] == [1, 2]
    assert user_state["state"]["profile"]["summary"] == "Experienced engineer"
