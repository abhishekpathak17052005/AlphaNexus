"""
ALPHANEXUS – Corporate Actions Application Service
==================================================
Manages dividends, stock splits, bonus issues, and shareholder meeting calendars.
"""

from typing import Any, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.corporate_action import CorporateAction


class CorporateActionService:

    @staticmethod
    def list_actions(
        db: Session,
        company_id: Optional[UUID] = None,
        limit: int = 50,
    ) -> List[CorporateAction]:
        q = db.query(CorporateAction)
        if company_id:
            q = q.filter(CorporateAction.company_id == company_id)
        return q.order_by(CorporateAction.ex_date.desc().nullslast()).limit(limit).all()


corporate_action_service = CorporateActionService()
