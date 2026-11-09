from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db, parse_uuid
from app.models.company import Company
from app.models.market_event import MarketEvent
from app.schemas.market_event import MarketEventResponse

router = APIRouter()


@router.get("", response_model=List[MarketEventResponse])
def list_market_events(
    company_id: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(MarketEvent)
    if company_id:
        query = query.filter(MarketEvent.company_id == parse_uuid(company_id))
    if event_type:
        query = query.filter(MarketEvent.event_type.ilike(f"%{event_type}%"))

    return query.order_by(MarketEvent.disclosed_date.desc()).limit(limit).all()


@router.get("/companies/{company_id}/market-events", response_model=List[MarketEventResponse])
def get_company_market_events(company_id: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == parse_uuid(company_id)).first()
    if not company:
        company = db.query(Company).filter(Company.symbol == company_id.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return (
        db.query(MarketEvent)
        .filter(MarketEvent.company_id == company.id)
        .order_by(MarketEvent.disclosed_date.desc())
        .all()
    )
