"""
ALPHANEXUS – Document Chunking Strategies & Token Limits
=========================================================
Configurable token thresholds by document classification.
"""

from typing import Dict, Any

CHUNK_STRATEGIES: Dict[str, Dict[str, Any]] = {
    "Annual Report": {
        "chunk_size": 600,
        "chunk_overlap": 100,
        "table_aware": True,
        "preserve_sections": True,
    },
    "Management Discussion": {
        "chunk_size": 700,
        "chunk_overlap": 100,
        "table_aware": False,
        "preserve_sections": True,
    },
    "Earnings Call Transcript": {
        "chunk_size": 500,
        "chunk_overlap": 75,
        "speaker_aware": True,
        "preserve_sections": True,
    },
    "Financial Statement": {
        "chunk_size": 800,
        "chunk_overlap": 50,
        "table_aware": True,
        "preserve_sections": True,
    },
    "Corporate Announcement": {
        "chunk_size": 400,
        "chunk_overlap": 50,
        "event_aware": True,
        "preserve_sections": False,
    },
}

