"""
ALPHANEXUS – Financial Analysis Application Service
===================================================
Provides statement queries, DuPont breakdown calculations, and peer comparisons.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.database.repositories.financial_repository import financial_repository
from app.engines.financial.analysis import (
    calculate_roe,
    calculate_roce,
    calculate_dupont_roe,
    calculate_ebitda_margin,
    calculate_net_profit_margin,
    calculate_debt_to_equity,
    calculate_current_ratio,
    peer_analyzer,
)


class FinancialService:

    @staticmethod
    def get_metrics(db: Session, company_id: UUID) -> List[Any]:
        return financial_repository.get_metrics_by_company(db, company_id)

    @staticmethod
    def get_statements(db: Session, company_id: UUID, statement_type: Optional[str] = None) -> List[Any]:
        return financial_repository.get_statements_by_type(db, company_id, statement_type)

    @staticmethod
    def get_ratios(db: Session, company_id: UUID) -> Dict[str, Any]:
        metrics = financial_repository.get_metrics_by_company(db, company_id)
        if not metrics:
            return {}
        latest = metrics[0]
        roe = calculate_roe(latest.net_profit, latest.total_equity)
        roce = calculate_roce(latest.operating_profit, latest.total_assets, latest.total_liabilities)
        dupont = calculate_dupont_roe(latest.net_profit, latest.revenue, latest.total_assets, latest.total_equity)
        ebitda_margin = calculate_ebitda_margin(latest.ebitda, latest.revenue)
        pat_margin = calculate_net_profit_margin(latest.net_profit, latest.revenue)
        de = calculate_debt_to_equity(latest.total_debt, latest.total_equity)
        cr = calculate_current_ratio(latest.current_assets, latest.current_liabilities)

        return {
            "company_id": str(company_id),
            "financial_year": latest.financial_year,
            "period_end": str(latest.period_end) if latest.period_end else None,
            "roe": roe,
            "roce": roce,
            "dupont": dupont,
            "ebitda_margin": ebitda_margin,
            "net_profit_margin": pat_margin,
            "operating_margin": ebitda_margin,
            "debt_to_equity": de,
            "current_ratio": cr,
            "asset_turnover": dupont.get("asset_turnover") if isinstance(dupont, dict) else None,
        }


financial_service = FinancialService()
