"""
ALPHANEXUS – Settings & System Configuration Route
"""
from typing import Dict, Any
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("")
def get_system_settings() -> Dict[str, Any]:
    """Return public platform configuration and runtime modes."""
    return {
        "app_name": settings.APP_NAME,
        "app_env": settings.APP_ENV,
        "data_mode": settings.DATA_MODE,
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "embedding_dimension": settings.EMBEDDING_DIMENSION,
        "gemini_model": settings.GEMINI_MODEL,
        "groq_model": settings.GROQ_MODEL,
        "cors_origins": settings.CORS_ORIGINS,
    }
