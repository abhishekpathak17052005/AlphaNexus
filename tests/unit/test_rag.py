"""
Unit tests for ALPHANEXUS RAG Pipeline and Hybrid Retrieval
"""
import pytest
from app.engines.rag.service import rag_service


def test_rag_service_initialization():
    assert rag_service is not None
    assert rag_service.embedding_engine is not None
    assert rag_service.vector_store is not None


def test_rag_query_routing():
    from app.engines.rag.query_router import query_router
    route = query_router.route_query("What was the FY24 revenue of TCS?")
    assert route in ["financial", "hybrid", "dense", "general"]
