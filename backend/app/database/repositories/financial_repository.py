"""
ALPHANEXUS – Financial Repository
==================================
Data access layer for financial metrics, multi-year accounting statements, and ratios.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.financial import FinancialMetric, FinancialStatement


class FinancialRepository:

    @staticmethod
    def get_metrics_by_company(db: Session, company_id: UUID) -> List[FinancialMetric]:
        return (
            db.query(FinancialMetric)
            .filter(FinancialMetric.company_id == company_id)
            .order_by(FinancialMetric.period_end.desc())
            .all()
        )

    @staticmethod
    def get_statements_by_type(
        db: Session,
        company_id: UUID,
        statement_type: Optional[str] = None,
    ) -> List[FinancialStatement]:
        q = db.query(FinancialStatement).filter(FinancialStatement.company_id == company_id)
        if statement_type:
            q = q.filter(FinancialStatement.statement_type == statement_type)
        return q.order_by(FinancialStatement.period_end.desc()).all()


financial_repository = FinancialRepository()

