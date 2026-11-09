"""
ALPHANEXUS – Common API Contracts & Envelopes
==============================================
Standard response wrappers, pagination schemas, and system status models.
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard success envelope for ALPHANEXUS endpoints."""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error schema."""
    success: bool = False
    error: str
    code: str = "INTERNAL_ERROR"
    details: Optional[Dict[str, Any]] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard pagination metadata contract."""
    items: List[T]
    total: int
    page: int = 1
    page_size: int = 20
    pages: int = 1
