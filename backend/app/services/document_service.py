"""
ALPHANEXUS – Document Management Service
=========================================
Handles multi-format document uploads, background indexing dispatches, and deletions.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.engines.rag.service import rag_service
from app.database.repositories.document_repository import document_repository


class DocumentService:

    @staticmethod
    def list_documents(db: Session, company_id: Optional[UUID] = None) -> List[Any]:
        return document_repository.list_by_company(db, company_id=company_id)

    @staticmethod
    def get_document(db: Session, document_id: UUID) -> Optional[Any]:
        return document_repository.get_by_id(db, document_id)

    @staticmethod
    def get_document_stats(db: Session, document_id: str) -> Dict[str, Any]:
        return rag_service.get_document_stats(db, document_id)


document_service = DocumentService()

