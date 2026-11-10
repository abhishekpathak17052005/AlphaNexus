"""
ALPHANEXUS – Frontend Auth API Client
"""
from typing import Dict, Any, Optional
from .client import api_client


def login(username: str, password: str) -> Dict[str, Any]:
    """Authenticate analyst credentials against the backend API."""
    try:
        return api_client.post(
            "/auth/login",
            payload={"username": username, "password": password},
        )
    except Exception as e:
        return {"authenticated": False, "error": str(e)}


def check_auth_status() -> Dict[str, Any]:
    """Verify active session status."""
    try:
        return api_client.get("/auth/me")
    except Exception as e:
        return {"authenticated": False, "error": str(e)}

