"""
ALPHANEXUS – Embedding Vector Cache
====================================
In-memory LRU cache preventing duplicate inference on identical text chunks.
"""

from typing import Dict, List, Optional
import hashlib

_EMBEDDING_CACHE: Dict[str, List[float]] = {}
MAX_CACHE_ENTRIES = 50000


def get_cached_embedding(text: str) -> Optional[List[float]]:
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return _EMBEDDING_CACHE.get(key)


def set_cached_embedding(text: str, embedding: List[float]) -> None:
    if len(_EMBEDDING_CACHE) >= MAX_CACHE_ENTRIES:
        # Evict oldest entry
        _EMBEDDING_CACHE.pop(next(iter(_EMBEDDING_CACHE)))
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    _EMBEDDING_CACHE[key] = embedding
