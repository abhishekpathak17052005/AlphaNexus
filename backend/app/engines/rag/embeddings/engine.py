"""
ALPHANEXUS – Dense Embedding Engine
===================================
Sentence Transformers BAAI/bge-base-en-v1.5 768-d inference engine.
"""

from app.engines.rag.embeddings import EmbeddingEngine, embedding_engine

__all__ = ["EmbeddingEngine", "embedding_engine"]
