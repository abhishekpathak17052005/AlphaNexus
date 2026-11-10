"""
ALPHANEXUS – Dense Embeddings Package
"""
from .engine import EmbeddingEngine, embedding_engine
from .cache import get_cached_embedding, set_cached_embedding

__all__ = ["EmbeddingEngine", "embedding_engine", "get_cached_embedding", "set_cached_embedding"]

