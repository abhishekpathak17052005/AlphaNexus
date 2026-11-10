"""
ALPHANEXUS – Document Ingestion and Indexing Worker
===================================================
Handles asynchronous end-to-end processing of uploaded financial documents:
extraction, table structure parsing, chunking, dense embedding generation,
and dual-store persistence (PostgreSQL pgvector and MongoDB Atlas).
"""

from __future__ import annotations

import os
import time
from typing import Dict, Any, Optional

from app.core.logging import logger
from app.core.database import SessionLocal
from app.models.document import Document
from app.engines.rag.service import rag_service


class DocumentWorker:
    """
    Background worker for processing uploaded financial documents asynchronously.
    """

    def __init__(self):
        self.rag_service = rag_service

    def process_document(
        self,
        document_id: int,
        file_path: str,
        company_id: Optional[int] = None,
        title: Optional[str] = None,
        doc_type: str = "annual_report",
    ) -> Dict[str, Any]:
        """
        Execute full document indexing pipeline for a stored document.
        """
        logger.info(f"[DocumentWorker] Starting background processing for doc_id={document_id}, path={file_path}")
        start_time = time.time()

        if not os.path.exists(file_path):
            error_msg = f"Document file not found at path: {file_path}"
            logger.error(f"[DocumentWorker] {error_msg}")
            self._update_document_status(document_id, status="FAILED", error=error_msg)
            return {"status": "error", "error": error_msg}

        try:
            self._update_document_status(document_id, status="PROCESSING")

            # Ingest via RAG service
            result = self.rag_service.ingest_document(
                file_path=file_path,
                document_id=str(document_id),
                company_id=str(company_id) if company_id else "",
                document_type=doc_type,
            )

            chunks_count = result.get("chunks_created", 0)
            elapsed = time.time() - start_time

            self._update_document_status(
                document_id,
                status="INDEXED",
                chunks_count=chunks_count,
            )

            logger.info(
                f"[DocumentWorker] Successfully indexed doc_id={document_id} in {elapsed:.2f}s "
                f"({chunks_count} chunks created)"
            )
            return {
                "status": "success",
                "document_id": document_id,
                "chunks_created": chunks_count,
                "elapsed_s": round(elapsed, 2),
            }

        except Exception as exc:
            logger.exception(f"[DocumentWorker] Failed to process doc_id={document_id}: {exc}")
            self._update_document_status(document_id, status="FAILED", error=str(exc))
            return {"status": "error", "document_id": document_id, "error": str(exc)}

    def _update_document_status(
        self,
        document_id: int,
        status: str,
        chunks_count: Optional[int] = None,
        error: Optional[str] = None,
    ) -> None:
        """Update document record in PostgreSQL database."""
        db = SessionLocal()
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                doc.status = status
                if chunks_count is not None:
                    doc.chunks_count = chunks_count
                if error:
                    doc.error_message = error
                db.commit()
        except Exception as exc:
            logger.warning(f"[DocumentWorker] Could not update document status in DB: {exc}")
            db.rollback()
        finally:
            db.close()


document_worker = DocumentWorker()

