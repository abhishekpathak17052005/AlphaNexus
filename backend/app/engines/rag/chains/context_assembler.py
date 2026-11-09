"""
ALPHANEXUS – RAG Context Assembler & Citation Formatter
=======================================================
Formats retrieved chunks into tagged context blocks with [Source N] brackets.
"""

from app.engines.rag.citations import CitationEngine

__all__ = ["CitationEngine"]
