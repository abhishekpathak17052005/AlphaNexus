"""
ALPHANEXUS – Document Repository
=================================
Data access layer for regulatory filings, annual reports, and extracted vector chunks.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.document import Document, DocumentChunk


class DocumentRepository:

    @staticmethod
    def get_by_id(db: Session, document_id: UUID) -> Optional[Document]:
        return db.query(Document).filter(Document.id == document_id).first()

    @staticmethod
    def get_by_checksum(db: Session, checksum: str) -> Optional[Document]:
        return db.query(Document).filter(Document.file_hash == checksum).first()

    @staticmethod
    def list_by_company(
        db: Session,
        company_id: Optional[UUID] = None,
        document_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Document]:
        q = db.query(Document)
        if company_id:
            q = q.filter(Document.company_id == company_id)
        if document_type:
            q = q.filter(Document.document_type == document_type)
        return q.order_by(Document.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_chunks_for_document(db: Session, document_id: UUID) -> List[DocumentChunk]:
        return (
            db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index.asc())
            .all()
        )

    @staticmethod
    def delete(db: Session, doc: Document) -> None:
        db.delete(doc)
        db.commit()


document_repository = DocumentRepository()

