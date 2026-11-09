from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.news import NewsArticle
from app.engines.news.service import news_service
from app.schemas.news import NewsArticleResponse, NewsSyncResponse

router = APIRouter()


@router.get("", response_model=List[NewsArticleResponse])
def list_news(
    company_id: Optional[str] = None,
    category: Optional[str] = None,
    sentiment: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Fetches normalized financial intelligence articles with filtering."""
    query = db.query(NewsArticle).filter(NewsArticle.is_duplicate == False)

    if company_id:
        query = query.filter(NewsArticle.company_id == company_id)
    if category:
        query = query.filter(NewsArticle.category == category)
    if sentiment:
        query = query.filter(NewsArticle.sentiment_label == sentiment.capitalize())

    articles = query.order_by(NewsArticle.published_at.desc()).offset(skip).limit(limit).all()

    # If database is empty initially, trigger auto-sync of seed news
    if not articles and skip == 0:
        news_service.sync_news(db, limit=10)
        articles = query.order_by(NewsArticle.published_at.desc()).offset(skip).limit(limit).all()

    return articles


@router.get("/{article_id}", response_model=NewsArticleResponse)
def get_article(article_id: str, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    return article


@router.post("/sync", response_model=NewsSyncResponse)
def sync_news(limit: int = Query(15, ge=1, le=50), db: Session = Depends(get_db)):
    """Triggers news synchronization from Marketaux API or demo fixtures."""
    res = news_service.sync_news(db, limit=limit)
    return NewsSyncResponse(
        synced_count=res["synced_count"],
        is_live_provider=res["is_live_provider"],
        status="Success",
    )

