"""
ALPHANEXUS – RAG Pipeline Orchestrator
======================================
Unified RAG pipeline interface re-exporting the central RAGService.
"""

from app.engines.rag.service import RAGService, rag_service

__all__ = ["RAGService", "rag_service"]

