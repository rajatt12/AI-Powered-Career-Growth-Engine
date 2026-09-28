import logging
from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from ...services.auth_service import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["User Authentication & Personalization"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SaveStateRequest(BaseModel):
    profile: Optional[Dict[str, Any]] = None
    target_role_id: Optional[str] = None
    roadmap: Optional[Dict[str, Any]] = None
    completed_weeks: Optional[List[int]] = None

def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication token. Please sign in."
        )
    token = authorization.split(" ")[1]
    payload = AuthService.decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid token. Please sign in again."
        )
    return int(payload["sub"])

@router.post("/register")
def register(payload: RegisterRequest):
    success, msg, data = AuthService.register_user(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return {"success": True, "message": msg, "data": data}

@router.post("/login")
def login(payload: LoginRequest):
    success, msg, data = AuthService.authenticate_user(
        email=payload.email,
        password=payload.password
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)
    return {"success": True, "message": msg, "data": data}

@router.get("/me")
def get_me(authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    user = AuthService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return {"success": True, "user": user}

@router.post("/save-state")
def save_user_state(payload: SaveStateRequest, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    ok = AuthService.save_user_state(
        user_id=user_id,
        profile=payload.profile,
        target_role_id=payload.target_role_id,
        roadmap=payload.roadmap,
        completed_weeks=payload.completed_weeks
    )
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not save state.")
    return {"success": True, "message": "Personalized career state saved successfully."}
