"""
ALPHANEXUS – Custom Domain Exceptions
======================================
Defines typed application exceptions for standard error handling across engines.
"""

from typing import Optional, Any, Dict


class AlphaNexusException(Exception):
    """Base exception for all ALPHANEXUS domain errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class EntityNotFoundError(AlphaNexusException):
    """Raised when an equity, document, or record is not found."""
    pass


class DocumentProcessingError(AlphaNexusException):
    """Raised when document ingestion, chunking, or OCR fails."""
    pass


class VectorIndexError(AlphaNexusException):
    """Raised when vector similarity search or embedding indexing fails."""
    pass


class ExternalAPIError(AlphaNexusException):
    """Raised when an external financial provider (Dhan, Marketaux, Gemini, Groq) fails."""
    pass


class QuantitativeCalculationError(AlphaNexusException):
    """Raised when financial ratio or econometric forecast computation encounters illegal mathematical state."""
    pass

