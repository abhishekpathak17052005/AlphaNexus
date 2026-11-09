"""
ALPHANEXUS – AI Research Chat Service
======================================
Manages multi-turn research conversations and persists sessions and citations.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.research import ResearchSession, ResearchMessage
from app.engines.rag.service import rag_service


class ChatService:

    @staticmethod
    def create_session(db: Session, title: str = "Research Session", company_id: Optional[UUID] = None) -> ResearchSession:
        session = ResearchSession(title=title, company_id=company_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def list_sessions(db: Session, company_id: Optional[UUID] = None) -> List[ResearchSession]:
        q = db.query(ResearchSession)
        if company_id:
            q = q.filter(ResearchSession.company_id == company_id)
        return q.order_by(ResearchSession.created_at.desc()).all()

    @staticmethod
    def send_message(
        db: Session,
        session_id: str,
        query: str,
        company_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return rag_service.research_chat(
            db=db,
            session_id=session_id,
            user_query=query,
            company_id=company_id,
        )


chat_service = ChatService()
