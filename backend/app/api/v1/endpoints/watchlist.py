import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.watchlist import Watchlist
from app.models.company import Company
from app.models.user import User
from app.schemas.watchlist import WatchlistItemResponse, WatchlistAddRequest

router = APIRouter()

# Default dev user helper
def get_default_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        user = User(
            email="analyst@equilens.ai",
            full_name="Lead Equity Analyst",
            role="senior_analyst",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.get("", response_model=List[WatchlistItemResponse])
def get_watchlist(db: Session = Depends(get_db)):
    user = get_default_user(db)
    items = db.query(Watchlist).filter(Watchlist.user_id == user.id).all()
    return items


@router.post("", response_model=WatchlistItemResponse)
def add_to_watchlist(payload: WatchlistAddRequest, db: Session = Depends(get_db)):
    user = get_default_user(db)
    company = db.query(Company).filter(Company.id == payload.company_id).first()
    if not company:
        company = db.query(Company).filter(Company.symbol == payload.company_id.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    existing = db.query(Watchlist).filter(
        Watchlist.user_id == user.id,
        Watchlist.company_id == company.id,
    ).first()

    if existing:
        if payload.target_price is not None:
            existing.target_price = payload.target_price
        if payload.alert_threshold_percent is not None:
            existing.alert_threshold_percent = payload.alert_threshold_percent
        if payload.notes is not None:
            existing.notes = payload.notes
        db.commit()
        db.refresh(existing)
        return existing

    item = Watchlist(
        user_id=user.id,
        company_id=company.id,
        target_price=payload.target_price,
        alert_threshold_percent=payload.alert_threshold_percent,
        notes=payload.notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{company_id}")
def remove_from_watchlist(company_id: str, db: Session = Depends(get_db)):
    user = get_default_user(db)
    item = db.query(Watchlist).filter(
        Watchlist.user_id == user.id,
        (Watchlist.company_id == company_id) | (Watchlist.id == company_id),
    ).first()

    if not item:
        # Also try via company symbol
        comp = db.query(Company).filter(Company.symbol == company_id.upper()).first()
        if comp:
            item = db.query(Watchlist).filter(
                Watchlist.user_id == user.id,
                Watchlist.company_id == comp.id,
            ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Watchlist entry not found")

    db.delete(item)
    db.commit()
    return {"message": "Company removed from watchlist"}

