"""
ALPHANEXUS – RAG Application Service
====================================
Service layer mediating between FastAPI REST endpoints and the core RAG pipeline.
"""

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.engines.rag.service import rag_service


class RAGAppService:

    @staticmethod
    def query(
        db: Session,
        query: str,
        company_id: Optional[str] = None,
        top_k: int = 8,
        hybrid: bool = True,
        reranking: bool = False,
    ) -> Dict[str, Any]:
        return rag_service.retrieve(
            db=db,
            query=query,
            company_id=company_id,
            top_k=top_k,
            hybrid=hybrid,
            reranking=reranking,
        )

    @staticmethod
    def chat(
        db: Session,
        session_id: str,
        query: str,
        company_id: Optional[str] = None,
        top_k: int = 8,
        hybrid: bool = True,
        reranking: bool = False,
    ) -> Dict[str, Any]:
        return rag_service.research_chat(
            db=db,
            session_id=session_id,
            user_query=query,
            company_id=company_id,
            top_k=top_k,
            hybrid=hybrid,
            reranking=reranking,
        )


rag_app_service = RAGAppService()

