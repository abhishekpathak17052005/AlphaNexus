import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyResponse, CompanyDetailResponse

router = APIRouter()


@router.get("", response_model=List[CompanyResponse])
def list_companies(
    exchange: Optional[str] = Query(None, description="NSE or BSE filter"),
    sector: Optional[str] = Query(None, description="Sector filter"),
    search: Optional[str] = Query(None, description="Search term for symbol or name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Company).filter(Company.is_active == True)

    if exchange:
        query = query.filter(Company.exchange == exchange.upper())
    if sector:
        query = query.filter(Company.sector == sector)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Company.symbol.ilike(search_pattern),
                Company.name.ilike(search_pattern),
            )
        )

    return query.order_by(Company.market_cap.desc().nullslast()).offset(skip).limit(limit).all()


@router.get("/search", response_model=List[CompanyResponse])
def search_companies(
    q: str = Query(..., min_length=1, description="Company symbol or name"),
    limit: int = Query(10, ge=1, le=30),
    db: Session = Depends(get_db),
):
    search_pattern = f"%{q}%"
    results = (
        db.query(Company)
        .filter(
            Company.is_active == True,
            or_(
                Company.symbol.ilike(search_pattern),
                Company.name.ilike(search_pattern),
            ),
        )
        .limit(limit)
        .all()
    )
    return results


@router.get("/{company_id}", response_model=CompanyDetailResponse)
def get_company(company_id: str, db: Session = Depends(get_db)):
    company = None
    try:
        val_uuid = uuid.UUID(company_id)
        company = db.query(Company).filter(Company.id == val_uuid).first()
    except (ValueError, AttributeError):
        pass

    if not company:
        company = db.query(Company).filter(Company.symbol == company_id.upper()).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
