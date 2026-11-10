"""
ALPHANEXUS – News Application Service
======================================
Coordinates news retrieval, real-time external syncing, and sentiment scoring.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.engines.news.service import news_service


class NewsAppService:

    @staticmethod
    def get_articles(
        db: Session,
        company_id: Optional[UUID] = None,
        limit: int = 50,
    ) -> List[Any]:
        return news_service.get_articles(db, company_id=company_id, limit=limit)

    @staticmethod
    def sync_news(db: Session, limit: int = 50) -> Dict[str, Any]:
        return news_service.sync_market_news(db, limit=limit)


news_app_service = NewsAppService()

