"""
RAG Configuration SQLAlchemy model.
Stores versioned RAG pipeline configuration for admin control.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy import Uuid
from ..core.database import Base


class RAGConfiguration(Base):
    __tablename__ = "rag_configurations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    config_version = Column(String(20), nullable=False, default="v1.0")
    is_active = Column(Boolean, default=True, index=True)

    # Embedding
    embedding_model = Column(String(100), default="BAAI/bge-base-en-v1.5")
    embedding_dimension = Column(Integer, default=768)
    embedding_batch_size = Column(Integer, default=32)
    embedding_device = Column(String(20), default="cpu")
    embedding_max_seq_length = Column(Integer, default=512)

    # Chunking
    chunk_strategy = Column(String(50), default="financial_aware")
    chunk_size = Column(Integer, default=600)
    chunk_overlap = Column(Integer, default=100)
    max_chunk_size = Column(Integer, default=1200)
    min_chunk_size = Column(Integer, default=80)
    table_aware_chunking = Column(Boolean, default=True)
    semantic_chunking = Column(Boolean, default=True)
    parent_child_chunking = Column(Boolean, default=True)

    # Retrieval
    retrieval_top_k = Column(Integer, default=8)
    min_similarity_score = Column(Float, default=0.0)
    hybrid_search_enabled = Column(Boolean, default=True)
    vector_weight = Column(Float, default=0.6)
    keyword_weight = Column(Float, default=0.4)
    rrf_k = Column(Integer, default=60)

    # Reranking
    reranking_enabled = Column(Boolean, default=False)
    reranking_model = Column(String(100), default="BAAI/bge-reranker-base")
    reranking_top_k = Column(Integer, default=5)
    reranking_candidate_multiplier = Column(Integer, default=3)

    # Generation
    llm_provider = Column(String(30), default="gemini")
    llm_model = Column(String(100), default="gemini-1.5-flash")
    llm_temperature = Column(Float, default=0.1)
    llm_max_tokens = Column(Integer, default=2048)
    require_citations = Column(Boolean, default=True)

    # Metadata
    description = Column(Text, nullable=True)
    created_by = Column(String(100), default="system")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    extra_config = Column(JSON, default=dict)
