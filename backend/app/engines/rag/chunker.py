"""
ALPHANEXUS – Chunker Compatibility Shim
"""
from .chunking.chunker import FinancialDocumentChunker as DocumentChunker, FinancialDocumentChunker

__all__ = ["DocumentChunker", "FinancialDocumentChunker"]

