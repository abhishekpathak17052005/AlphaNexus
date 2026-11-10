"""
ALPHANEXUS – AI Research Chat Schemas
======================================
Contracts for multi-turn research conversations, user questions, and fact-grounded assistant responses.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ChatCitation(BaseModel):
    id: Optional[UUID] = None
    document_id: Optional[UUID] = None
    document_chunk_id: Optional[UUID] = None
    page_number: Optional[int] = None
    section: Optional[str] = None
    excerpt: str
    confidence_score: float = 0.95
    source_url: Optional[str] = None


class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=4000)
    company_id: Optional[str] = None
    financial_year: Optional[str] = None
    document_type: Optional[str] = None
    hybrid: bool = True
    reranking: bool = False
    top_k: int = 8


class ChatMessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    message_type: str = "fact_grounded"
    token_count: Optional[int] = None
    route: Optional[str] = None
    citations: List[ChatCitation] = []
    created_at: datetime


class ChatSessionCreate(BaseModel):
    title: Optional[str] = "Equity Research Session"
    company_id: Optional[UUID] = None


class ChatSessionResponse(BaseModel):
    id: UUID
    title: str
    company_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []

