"""
ALPHANEXUS – Document Text Cleaner
==================================
Cleans OCR artifacts, normalizes punctuation, and removes noisy headers/footers.
"""

from app.engines.rag.preprocessor import DocumentPreprocessor

__all__ = ["DocumentPreprocessor"]
