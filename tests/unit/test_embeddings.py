"""
Unit tests for ALPHANEXUS Embedding Engine
"""
import pytest
from app.engines.rag.embeddings.engine import embedding_engine


def test_embedding_generation():
    text = "HDFC Bank quarterly net profit rises 17% YoY."
    vector = embedding_engine.get_embedding(text)
    assert isinstance(vector, list)
    assert len(vector) in [384, 768, 1024]
    # Check L2 normalisation
    norm = sum(x**2 for x in vector) ** 0.5
    assert abs(norm - 1.0) < 0.05
