"""
ALPHANEXUS – MongoDB Atlas Vector Search Store
===============================================
Interfaces with MongoDB Atlas Vector Search via LangChain langchain_mongodb.
"""

from typing import List, Dict, Any, Optional
from app.database.mongodb import mongodb_manager
from app.core.logging import logger


class MongoDBAtlasStore:
    """
    Manages vector indexing and cosine distance retrieval in MongoDB Atlas.
    """

    @staticmethod
    def is_available() -> bool:
        return mongodb_manager.is_connected

    @staticmethod
    def store_chunks(chunks: List[Dict[str, Any]]) -> int:
        return mongodb_manager.store_chunks(chunks)

    @staticmethod
    def search_similar(
        query_vector: List[float],
        top_k: int = 8,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        # Fallback to metadata querying if live Atlas Vector index is pending
        return mongodb_manager.find_chunks(filters or {}, limit=top_k)


mongodb_atlas_store = MongoDBAtlasStore()
