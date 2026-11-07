from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, UUID4, ConfigDict


class CitationResponse(BaseModel):
    id: Optional[str] = None
    document_id: Optional[str] = None
    document_chunk_id: Optional[str] = None
    document_title: Optional[str] = None
    page_number: Optional[int] = None
    section: Optional[str] = None
    excerpt: str
    source_url: Optional[str] = None
    confidence_score: float = 0.95


class ResearchQueryRequest(BaseModel):
    session_id: Optional[str] = None
    company_id: Optional[str] = None
    query: str
    financial_year: Optional[str] = None
    document_type: Optional[str] = None
    top_k: int = 5


class ResearchMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    message_type: str
    tokens_used: int = 0
    citations: List[CitationResponse] = []
    created_at: datetime


class ResearchSessionResponse(BaseModel):
    id: str
    title: str
    company_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[ResearchMessageResponse] = []

