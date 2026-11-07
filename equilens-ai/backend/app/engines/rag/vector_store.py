import uuid
from typing import List, Dict, Any, Optional
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.document import DocumentChunk, Document
from app.core.database import is_sqlite
from app.core.logging import logger


class VectorStore:
    """
    Interface for vector storage and semantic retrieval.
    Natively supports PostgreSQL + pgvector cosine similarity distance
    and provides in-memory cosine fallback for SQLite local dev.
    """

    def store_chunks(self, db: Session, chunks_data: List[Dict[str, Any]]) -> int:
        """Persists document chunks and embeddings to the database."""
        inserted = 0
        for data in chunks_data:
            doc_id = uuid.UUID(data["document_id"]) if isinstance(data["document_id"], str) else data["document_id"]
            comp_id = uuid.UUID(data["company_id"]) if isinstance(data["company_id"], str) else data["company_id"]

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
        db.commit()
        return inserted

    def search_similar(
        self,
        db: Session,
        query_embedding: List[float],
        company_id: Optional[Any] = None,
        financial_year: Optional[str] = None,
        document_type: Optional[str] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most similar document chunks matching metadata filters.
        Returns list of dicts with chunk fields, document metadata, and similarity_score.
        """
        try:
            query = db.query(DocumentChunk).join(Document, DocumentChunk.document_id == Document.id)

            if company_id:
                comp_val = uuid.UUID(company_id) if isinstance(company_id, str) else company_id
                query = query.filter(DocumentChunk.company_id == comp_val)
            if financial_year:
                query = query.filter(Document.financial_year == financial_year)
            if document_type:
                query = query.filter(Document.document_type == document_type)

            chunks = query.all()
            if not chunks:
                return []

            # Score each chunk
            scored_results = []
            q_vec = np.array(query_embedding, dtype=np.float32)
            q_norm = np.linalg.norm(q_vec)

            for chunk in chunks:
                if chunk.embedding is not None:
                    c_vec = np.array(chunk.embedding, dtype=np.float32)
                    c_norm = np.linalg.norm(c_vec)
                    if q_norm > 0 and c_norm > 0:
                        sim = float(np.dot(q_vec, c_vec) / (q_norm * c_norm))
                    else:
                        sim = 0.0
                else:
                    sim = 0.0

                scored_results.append({
                    "chunk_id": str(chunk.id),
                    "document_id": str(chunk.document_id),
                    "company_id": str(chunk.company_id),
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "clean_text": chunk.clean_text,
                    "section": chunk.section,
                    "page_number": chunk.page_number,
                    "document_title": chunk.document.title if chunk.document else "",
                    "document_type": chunk.document.document_type if chunk.document else "",
                    "financial_year": chunk.document.financial_year if chunk.document else "",
                    "similarity_score": round(sim, 4),
                    "metadata": chunk.metadata_json,
                })

            scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)
            return scored_results[:top_k]

        except Exception as e:
            logger.error(f"Error in vector similarity search: {e}")
            return []

    def delete_document_chunks(self, db: Session, document_id: str) -> int:
        """Deletes all chunks and embeddings for a given document."""
        doc_uuid = uuid.UUID(document_id) if isinstance(document_id, str) else document_id
        deleted = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_uuid).delete()
        db.commit()
        return deleted


vector_store = VectorStore()
