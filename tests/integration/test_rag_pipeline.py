"""
Integration tests for ALPHANEXUS End-to-End RAG Ingestion & Query
"""
import pytest
from app.engines.rag.service import rag_service


def test_rag_pipeline_search():
    results = rag_service.search_documents(
        query="operating profit margin and capital expenditure",
        top_k=3,
    )
    assert isinstance(results, list)

