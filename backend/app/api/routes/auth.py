"""
ALPHANEXUS – Authentication & Session Route
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.config import settings

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    authenticated: bool
    user: Dict[str, Any]
    token: Optional[str] = None
    role: str = "analyst"


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    """Authenticate user credentials and return an analyst session."""
    # Development/demo permissive authentication
    if payload.username and payload.password:
        return AuthResponse(
            authenticated=True,
            user={
                "username": payload.username,
                "role": "senior_analyst",
                "app": settings.APP_NAME,
            },
            token=f"alphanexus-sess-{payload.username}",
            role="senior_analyst",
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials provided.",
    )


@router.get("/me")
def get_current_session():
    """Retrieve active session details."""
    return {
        "status": "authenticated",
        "role": "analyst",
        "app_env": settings.APP_ENV,
        "app_name": settings.APP_NAME,
    }

