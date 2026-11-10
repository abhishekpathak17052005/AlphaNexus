"""
ALPHANEXUS – Common FastAPI Dependencies
=========================================
Reusable dependencies for database sessions, authentication, pagination,
and service injection.
"""

from __future__ import annotations

from typing import Generator, Optional
from fastapi import Depends, HTTPException, Header, Query, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings
from app.core.logging import logger


def get_db() -> Generator[Session, None, None]:
    """Provide a transactional database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_pagination(
    skip: int = Query(0, ge=0, description="Items to skip for pagination"),
    limit: int = Query(50, ge=1, le=100, description="Maximum items to return"),
) -> dict:
    """Standardized pagination parameter dependency."""
    return {"skip": skip, "limit": limit}


def get_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    authorization: Optional[str] = Header(None),
) -> Optional[str]:
    """
    Validate optional API key or Bearer token.
    Permissive in development mode; enforces authentication in production.
    """
    token = x_api_key or (authorization.replace("Bearer ", "") if authorization else None)
    if not token and settings.APP_ENV == "production":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key or Bearer token required in production environment.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

