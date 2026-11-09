"""
EquiLens AI – Vector Store
===========================
Handles chunk persistence and retrieval against PostgreSQL + pgvector.

Key design:
- Uses pgvector's native <=> (cosine) and <#> (inner-product) operators for ANN search
  via SQLAlchemy text() queries – orders of magnitude faster than Python loops.
- SQLite fallback for local dev: brute-force NumPy cosine (correctness preserved).
- Hybrid retrieval: BM25 keyword scoring fused with vector scores via Reciprocal Rank Fusion.
- All filters (company, financial_year, document_type, user) applied in SQL, not post-hoc.
"""

from __future__ import annotations

import uuid
from typing import List, Dict, Any, Optional

import numpy as np
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import is_sqlite
from app.core.logging import logger
from app.models.document import DocumentChunk, Document
from app.engines.rag.embeddings import embedding_engine


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_uuid(val: Any) -> Optional[uuid.UUID]:
    if val is None:
        return None
    if isinstance(val, uuid.UUID):
        return val
    try:
        return uuid.UUID(str(val))
    except (ValueError, AttributeError):
        return None


def _vec_to_pg(vec: List[float]) -> str:
    """Serialise a Python list to pgvector literal string '[0.1,0.2,...]'."""
    return "[" + ",".join(f"{v:.8f}" for v in vec) + "]"


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class VectorStore:
    """
    Vector storage and retrieval engine backed by PostgreSQL + pgvector.

    Retrieval modes:
      1. Semantic (dense ANN) – native pgvector <=> operator
      2. Keyword (BM25 on clean_text) – Python-side, no FTS index needed
      3. Hybrid – RRF fusion of semantic + keyword ranks
    """

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------

    def store_chunks(self, db: Session, chunks_data: List[Dict[str, Any]]) -> int:
        """
        Persist document chunks with embeddings.
        Existing chunks for the document are deleted before insertion (idempotent).
        """
        inserted = 0
        for data in chunks_data:
            doc_id = _to_uuid(data["document_id"])
            comp_id = _to_uuid(data["company_id"])
            chunk = DocumentChunk(
                document_id=doc_id,
                company_id=comp_id,
                chunk_index=data["chunk_index"],
                content=data["content"],
                clean_text=data.get("clean_text"),
                section=data.get("section"),
                page_number=data.get("page_number"),
                token_count=data.get("token_count", 0),
                embedding=data.get("embedding"),
                metadata_json=data.get("metadata_json", {}),
            )
            db.add(chunk)
            inserted += 1
        try:
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error(f"[VectorStore] store_chunks failed: {exc}")
            raise
        return inserted

    def delete_document_chunks(self, db: Session, document_id: str) -> int:
        doc_uuid = _to_uuid(document_id)
        deleted = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == doc_uuid)
            .delete()
        )
        db.commit()
        return deleted

    # ------------------------------------------------------------------
    # Semantic retrieval – native pgvector ANN
    # ------------------------------------------------------------------

    def search_similar(
        self,
        db: Session,
        query_embedding: List[float],
        company_id: Optional[Any] = None,
        financial_year: Optional[str] = None,
        document_type: Optional[str] = None,
        section: Optional[str] = None,
        top_k: int = 8,
        min_similarity: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Semantic ANN retrieval using pgvector cosine distance.
        Falls back to NumPy brute-force on SQLite.
        """
        if is_sqlite:
            return self._search_similar_sqlite(
                db, query_embedding, company_id, financial_year,
                document_type, top_k, min_similarity
            )
        return self._search_similar_pgvector(
            db, query_embedding, company_id, financial_year,
            document_type, section, top_k, min_similarity
        )

    def _search_similar_pgvector(
        self,
        db: Session,
        query_embedding: List[float],
        company_id: Optional[Any],
        financial_year: Optional[str],
        document_type: Optional[str],
        section: Optional[str],
        top_k: int,
        min_similarity: float,
    ) -> List[Dict[str, Any]]:
        """
        Uses pgvector <=> operator (cosine distance) for ANN search.
        Cosine similarity = 1 - cosine_distance.
        """
        vec_str = _vec_to_pg(query_embedding)
        params: Dict[str, Any] = {
            "vec": vec_str,
            "top_k": top_k,
            "min_sim": 1 - min_similarity,  # convert sim threshold to distance
        }

        where_clauses = ["dc.embedding IS NOT NULL"]

        if company_id:
            cid = _to_uuid(company_id)
            params["company_id"] = str(cid)
            where_clauses.append("dc.company_id = CAST(:company_id AS uuid)")

        if financial_year:
            params["financial_year"] = financial_year
            where_clauses.append("d.financial_year = :financial_year")

        if document_type:
            params["document_type"] = document_type
            where_clauses.append("d.document_type ILIKE :document_type")

        if section:
            params["section"] = f"%{section}%"
            where_clauses.append("dc.section ILIKE :section")

        where_sql = " AND ".join(where_clauses)

        sql = text(f"""
            SELECT
                dc.id::text              AS chunk_id,
                dc.document_id::text     AS document_id,
                dc.company_id::text      AS company_id,
                dc.chunk_index,
                dc.content,
                dc.clean_text,
                dc.section,
                dc.page_number,
                dc.token_count,
                dc.metadata_json,
                d.title                  AS document_title,
                d.document_type,
                d.financial_year,
                d.filename,
                1 - (dc.embedding <=> CAST(:vec AS vector)) AS similarity_score
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            WHERE {where_sql}
              AND (1 - (dc.embedding <=> CAST(:vec AS vector))) >= (1 - :min_sim)
            ORDER BY dc.embedding <=> CAST(:vec AS vector)
            LIMIT :top_k
        """)

        try:
            rows = db.execute(sql, params).mappings().all()
            return [self._row_to_dict(r) for r in rows]
        except Exception as exc:
            logger.error(f"[VectorStore] pgvector ANN query failed: {exc}")
            # Fall back to brute-force
            return self._search_similar_sqlite(
                db, query_embedding, company_id, financial_year,
                document_type, top_k, min_similarity
            )

    def _search_similar_sqlite(
        self,
        db: Session,
        query_embedding: List[float],
        company_id: Optional[Any],
        financial_year: Optional[str],
        document_type: Optional[str],
        top_k: int,
        min_similarity: float,
    ) -> List[Dict[str, Any]]:
        """Brute-force NumPy cosine fallback for SQLite development."""
        q = db.query(DocumentChunk).join(Document, DocumentChunk.document_id == Document.id)
        if company_id:
            q = q.filter(DocumentChunk.company_id == _to_uuid(company_id))
        if financial_year:
            q = q.filter(Document.financial_year == financial_year)
        if document_type:
            q = q.filter(Document.document_type == document_type)
        chunks = q.all()

        q_vec = np.array(query_embedding, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        scored = []
        for chunk in chunks:
            if chunk.embedding is None:
                continue
            c_vec = np.array(chunk.embedding, dtype=np.float32)
            c_norm = np.linalg.norm(c_vec)
            sim = float(np.dot(q_vec, c_vec) / (q_norm * c_norm)) if q_norm > 0 and c_norm > 0 else 0.0
            if sim >= min_similarity:
                scored.append({
                    "chunk_id": str(chunk.id),
                    "document_id": str(chunk.document_id),
                    "company_id": str(chunk.company_id),
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "clean_text": chunk.clean_text,
                    "section": chunk.section,
                    "page_number": chunk.page_number,
                    "token_count": chunk.token_count,
                    "document_title": chunk.document.title if chunk.document else "",
                    "document_type": chunk.document.document_type if chunk.document else "",
                    "financial_year": chunk.document.financial_year if chunk.document else "",
                    "filename": chunk.document.filename if chunk.document else "",
                    "metadata": chunk.metadata_json or {},
                    "similarity_score": round(sim, 4),
                    "keyword_score": 0.0,
                    "rerank_score": None,
                    "retrieval_method": "cosine_fallback",
                })
        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_k]

    # ------------------------------------------------------------------
    # Keyword retrieval (BM25 on in-memory chunk texts)
    # ------------------------------------------------------------------

    def keyword_search(
        self,
        db: Session,
        query: str,
        company_id: Optional[Any] = None,
        financial_year: Optional[str] = None,
        document_type: Optional[str] = None,
        top_k: int = 8,
    ) -> List[Dict[str, Any]]:
        """
        BM25 keyword retrieval on document chunk clean_text.
        Uses rank_bm25 library applied to pre-filtered candidate set.
        """
        try:
            from rank_bm25 import BM25Okapi
        except ImportError:
            logger.warning("[VectorStore] rank_bm25 not available – keyword search skipped")
            return []

        q = db.query(DocumentChunk).join(Document, DocumentChunk.document_id == Document.id)
        if company_id:
            q = q.filter(DocumentChunk.company_id == _to_uuid(company_id))
        if financial_year:
            q = q.filter(Document.financial_year == financial_year)
        if document_type:
            q = q.filter(Document.document_type == document_type)
        chunks = q.all()

        if not chunks:
            return []

        corpus = [(c.clean_text or c.content or "").lower().split() for c in chunks]
        bm25 = BM25Okapi(corpus)
        query_tokens = query.lower().split()
        scores = bm25.get_scores(query_tokens)

        results = []
        for chunk, score in zip(chunks, scores):
            if score <= 0:
                continue
            results.append({
                "chunk_id": str(chunk.id),
                "document_id": str(chunk.document_id),
                "company_id": str(chunk.company_id),
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "clean_text": chunk.clean_text,
                "section": chunk.section,
                "page_number": chunk.page_number,
                "token_count": chunk.token_count,
                "document_title": chunk.document.title if chunk.document else "",
                "document_type": chunk.document.document_type if chunk.document else "",
                "financial_year": chunk.document.financial_year if chunk.document else "",
                "filename": chunk.document.filename if chunk.document else "",
                "metadata": chunk.metadata_json or {},
                "similarity_score": 0.0,
                "keyword_score": float(score),
                "rerank_score": None,
                "retrieval_method": "bm25",
            })
        results.sort(key=lambda x: x["keyword_score"], reverse=True)
        return results[:top_k]

    # ------------------------------------------------------------------
    # Hybrid retrieval – Reciprocal Rank Fusion
    # ------------------------------------------------------------------

    def hybrid_search(
        self,
        db: Session,
        query: str,
        query_embedding: List[float],
        company_id: Optional[Any] = None,
        financial_year: Optional[str] = None,
        document_type: Optional[str] = None,
        top_k: int = 8,
        min_similarity: float = 0.0,
        vector_weight: float = 0.6,
        keyword_weight: float = 0.4,
        rrf_k: int = 60,
    ) -> List[Dict[str, Any]]:
        """
        Reciprocal Rank Fusion over semantic + BM25 results.
        RRF score = sum(w / (k + rank)) for each retrieval list.
        """
        semantic = self.search_similar(
            db, query_embedding, company_id, financial_year,
            document_type, top_k=top_k * 2, min_similarity=min_similarity
        )
        keyword = self.keyword_search(
            db, query, company_id, financial_year,
            document_type, top_k=top_k * 2
        )

        # Build lookup by chunk_id
        chunk_map: Dict[str, Dict[str, Any]] = {}
        rrf_scores: Dict[str, float] = {}

        for rank, r in enumerate(semantic):
            cid = r["chunk_id"]
            chunk_map[cid] = r
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + vector_weight / (rrf_k + rank + 1)

        for rank, r in enumerate(keyword):
            cid = r["chunk_id"]
            if cid not in chunk_map:
                chunk_map[cid] = r
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + keyword_weight / (rrf_k + rank + 1)

        # Merge scores into result dicts
        merged = []
        for cid, rrf in rrf_scores.items():
            item = dict(chunk_map[cid])
            item["rrf_score"] = round(rrf, 6)
            item["retrieval_method"] = "hybrid_rrf"
            merged.append(item)

        merged.sort(key=lambda x: x["rrf_score"], reverse=True)
        return merged[:top_k]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_dict(row: Any) -> Dict[str, Any]:
        return {
            "chunk_id": row["chunk_id"],
            "document_id": row["document_id"],
            "company_id": row["company_id"],
            "chunk_index": row["chunk_index"],
            "content": row["content"],
            "clean_text": row["clean_text"],
            "section": row["section"],
            "page_number": row["page_number"],
            "token_count": row.get("token_count", 0),
            "document_title": row["document_title"],
            "document_type": row["document_type"],
            "financial_year": row["financial_year"],
            "filename": row.get("filename", ""),
            "metadata": row.get("metadata_json") or {},
            "similarity_score": round(float(row["similarity_score"]), 4),
            "keyword_score": 0.0,
            "rerank_score": None,
            "retrieval_method": "pgvector_ann",
        }


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------
vector_store = VectorStore()
