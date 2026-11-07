from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db, parse_uuid
from app.models.company import Company
from app.models.corporate_action import CorporateAction
from app.schemas.corporate_action import CorporateActionResponse

router = APIRouter()


@router.get("", response_model=List[CorporateActionResponse])
def list_corporate_actions(
    company_id: Optional[str] = None,
    action_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(CorporateAction)
    if company_id:
        query = query.filter(CorporateAction.company_id == parse_uuid(company_id))
    if action_type:
        query = query.filter(CorporateAction.action_type.ilike(f"%{action_type}%"))

    return query.order_by(CorporateAction.ex_date.desc().nullslast()).limit(limit).all()


@router.get("/companies/{company_id}/corporate-actions", response_model=List[CorporateActionResponse])
def get_company_corporate_actions(company_id: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == parse_uuid(company_id)).first()
    if not company:
        company = db.query(Company).filter(Company.symbol == company_id.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return (
        db.query(CorporateAction)
        .filter(CorporateAction.company_id == company.id)
        .order_by(CorporateAction.ex_date.desc().nullslast())
        .all()
    )
