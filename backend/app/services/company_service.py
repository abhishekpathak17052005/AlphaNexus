"""
ALPHANEXUS – Company Application Service
=========================================
Encapsulates company discovery, profile retrieval, and master security tracking.
"""

from typing import Any, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.database.repositories.company_repository import company_repository


class CompanyService:

    @staticmethod
    def get_company(db: Session, company_id: UUID) -> Optional[Any]:
        return company_repository.get_by_id(db, company_id)

    @staticmethod
    def list_companies(
        db: Session,
        query: Optional[str] = None,
        sector: Optional[str] = None,
        limit: int = 100,
    ) -> List[Any]:
        return company_repository.list_all(db, query=query, sector=sector, limit=limit)


company_service = CompanyService()
