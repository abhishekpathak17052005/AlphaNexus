"""
ALPHANEXUS – PostgreSQL pgvector Vector Store
==============================================
Cosine similarity vector search on 768-dimensional document embeddings.
"""

from app.engines.rag.vector_store import VectorStore, vector_store

__all__ = ["VectorStore", "vector_store"]
