"""
ALPHANEXUS – Autonomous Equity Research Agent
==============================================
Orchestrates multi-hop information retrieval across filings, statements, and deals.
"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.engines.rag.service import rag_service


class ResearchAgent:

    @staticmethod
    def conduct_deep_research(
        db: Session,
        session_id: str,
        user_query: str,
        company_id: str,
    ) -> Dict[str, Any]:
        return rag_service.research_chat(
            db=db,
            session_id=session_id,
            user_query=user_query,
            company_id=company_id,
        )


research_agent = ResearchAgent()
