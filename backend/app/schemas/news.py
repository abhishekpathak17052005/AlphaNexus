from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, UUID4, ConfigDict


class NewsArticleResponse(BaseModel):
    id: UUID4
    company_id: Optional[UUID4] = None
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    source: str
    publisher: Optional[str] = None
    published_at: datetime
    category: str
    sentiment_label: str
    sentiment_score: Optional[float] = None
    ai_summary: Optional[str] = None
    financial_impact: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsSyncResponse(BaseModel):
    synced_count: int
    is_live_provider: bool
    status: str

