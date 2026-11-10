"""
ALPHANEXUS – Company Repository
================================
Data access layer for Indian listed equities (NSE/BSE).
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.company import Company


class CompanyRepository:

    @staticmethod
    def get_by_id(db: Session, company_id: UUID) -> Optional[Company]:
        return db.query(Company).filter(Company.id == company_id).first()

    @staticmethod
    def get_by_symbol(db: Session, symbol: str) -> Optional[Company]:
        return db.query(Company).filter(Company.symbol == symbol.upper()).first()

    @staticmethod
    def list_all(
        db: Session,
        query: Optional[str] = None,
        sector: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Company]:
        q = db.query(Company).filter(Company.is_active == True)
        if query:
            pattern = f"%{query}%"
            q = q.filter((Company.name.ilike(pattern)) | (Company.symbol.ilike(pattern)))
        if sector:
            q = q.filter(Company.sector == sector)
        return q.order_by(Company.market_cap.desc().nullslast()).offset(offset).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(Company).filter(Company.is_active == True).count()


company_repository = CompanyRepository()

