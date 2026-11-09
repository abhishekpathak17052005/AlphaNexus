"""
ALPHANEXUS – FastAPI Background Task Utilities
==============================================
Convenience dispatch functions for asynchronous operations scheduled
via FastAPI BackgroundTasks: document indexing, news ingestion, and audit logging.
"""

from __future__ import annotations

from typing import Optional, Dict, Any
from app.core.logging import logger
from app.workers.document_worker import document_worker


def task_process_document(
    document_id: int,
    file_path: str,
    company_id: Optional[int] = None,
    doc_type: str = "annual_report",
) -> None:
    """Execute document indexing in a FastAPI background task."""
    logger.info(f"[BackgroundTask] Dispatched document indexing task for doc_id={document_id}")
    document_worker.process_document(
        document_id=document_id,
        file_path=file_path,
        company_id=company_id,
        doc_type=doc_type,
    )


def task_sync_company_news(ticker: str, limit: int = 10) -> None:
    """Fetch and sync latest news for a specific equity ticker."""
    logger.info(f"[BackgroundTask] Background news sync triggered for {ticker}")
    try:
        from app.services.news_service import news_service
        news_service.get_company_news(ticker=ticker, limit=limit)
    except Exception as exc:
        logger.warning(f"[BackgroundTask] News sync for {ticker} encountered an error: {exc}")


def task_record_audit_event(
    action: str,
    entity_type: str,
    entity_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """Record an audit log entry in the background."""
    try:
        from app.services.audit_service import audit_service
        audit_service.log_event(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {},
        )
    except Exception as exc:
        logger.warning(f"[BackgroundTask] Audit logging failed: {exc}")
