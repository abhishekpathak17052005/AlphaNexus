"""
Unit tests for ALPHANEXUS Financial Document Chunking
"""
import pytest
from app.engines.rag.chunking.chunker import FinancialDocumentChunker


def test_chunker_basic():
    chunker = FinancialDocumentChunker(chunk_size=500, chunk_overlap=50)
    sample_text = (
        "Operating revenue stood at Rs. 1,00,000 Cr. representing 15% YoY growth. "
        "EBITDA increased to Rs. 20,000 Cr with margins expanding by 120 bps. "
    ) * 10
    chunks = chunker.chunk_text(sample_text)
    assert len(chunks) > 0
    for c in chunks:
        assert hasattr(c, "text") or isinstance(c, dict)

