"""
ALPHANEXUS – Hybrid Dense + Sparse Retriever
=============================================
Combines dense BGE cosine similarity with sparse BM25 keyword matching via Reciprocal Rank Fusion (RRF).
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.engines.rag.vector_store import vector_store


class HybridRetriever:

    @staticmethod
    def retrieve(
        db: Session,
        query: str,
        query_embedding: List[float],
        company_id: Optional[str] = None,
        top_k: int = 8,
        vector_weight: float = 0.6,
        keyword_weight: float = 0.4,
    ) -> List[Dict[str, Any]]:
        return vector_store.hybrid_search(
            db=db,
            query=query,
            query_embedding=query_embedding,
            company_id=company_id,
            top_k=top_k,
            vector_weight=vector_weight,
            keyword_weight=keyword_weight,
        )


hybrid_retriever = HybridRetriever()
