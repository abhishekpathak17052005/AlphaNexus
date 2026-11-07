import pytest
from app.engines.rag.chunker import DocumentChunker
from app.engines.rag.preprocessor import DocumentPreprocessor


def test_table_preservation_in_chunking():
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)

    # Mock page with a financial table
    table_rows = [
        ["Line Item", "FY23 (₹ Cr)", "FY24 (₹ Cr)"],
        ["Revenue from Ops", "10,500", "12,200"],
        ["EBITDA", "2,100", "2,650"],
        ["PAT", "1,200", "1,550"],
    ]

    pages_data = [{
        "page_number": 12,
        "text": "The company delivered strong financial performance across key operating segments.",
        "tables": [table_rows],
    }]

    chunks = chunker.chunk_document(
        pages_data=pages_data,
        company_id="comp-123",
        document_id="doc-456",
        company_symbol="TCS",
        financial_year="FY24",
        document_type="Annual Report",
    )

    assert len(chunks) >= 2
    # Find table chunk
    table_chunk = next((c for c in chunks if c["section"] == "Financial Tables"), None)
    assert table_chunk is not None
    assert "Revenue from Ops" in table_chunk["content"]
    assert "EBITDA" in table_chunk["content"]
    assert table_chunk["page_number"] == 12


def test_empty_page_detection():
    assert DocumentPreprocessor.is_empty_page("   ", []) is True
    assert DocumentPreprocessor.is_empty_page("Substantial content on this page with numbers.", []) is False

