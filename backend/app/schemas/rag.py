"""
Pydantic schemas for the RAG API endpoints.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="User research question")
    session_id: Optional[str] = None
    company_id: Optional[str] = None
    financial_year: Optional[str] = None
    document_type: Optional[str] = None
    top_k: int = Field(default=8, ge=1, le=25)
    hybrid: bool = True
    reranking: bool = False
    min_similarity: float = Field(default=0.0, ge=0.0, le=1.0)
    vector_weight: float = Field(default=0.6, ge=0.0, le=1.0)
    keyword_weight: float = Field(default=0.4, ge=0.0, le=1.0)


class RAGRetrieveRequest(BaseModel):
    query: str = Field(..., min_length=3)
    company_id: Optional[str] = None
    financial_year: Optional[str] = None
    document_type: Optional[str] = None
    top_k: int = Field(default=8, ge=1, le=25)
    hybrid: bool = True
    reranking: bool = False
    min_similarity: float = Field(default=0.0, ge=0.0, le=1.0)
    vector_weight: float = Field(default=0.6)
    keyword_weight: float = Field(default=0.4)


class RAGChatRequest(BaseModel):
    query: str = Field(..., min_length=3)
    session_id: Optional[str] = None
    company_id: Optional[str] = None
    financial_year: Optional[str] = None
    document_type: Optional[str] = None
    top_k: int = Field(default=8, ge=1, le=20)
    hybrid: bool = True
    reranking: bool = False


class RAGConfigUpdateRequest(BaseModel):
    embedding_model: Optional[str] = None
    embedding_dimension: Optional[int] = None
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
    retrieval_top_k: Optional[int] = None
    min_similarity_score: Optional[float] = None
    hybrid_search_enabled: Optional[bool] = None
    vector_weight: Optional[float] = None
    keyword_weight: Optional[float] = None
    reranking_enabled: Optional[bool] = None
    reranking_model: Optional[str] = None
    reranking_top_k: Optional[int] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    llm_temperature: Optional[float] = None
    llm_max_tokens: Optional[int] = None
    description: Optional[str] = None


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class ChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    document_type: Optional[str]
    financial_year: Optional[str]
    filename: Optional[str] = None
    section: Optional[str]
    page_number: Optional[int]
    content: str
    clean_text: Optional[str] = None
    similarity_score: float
    keyword_score: float = 0.0
    rerank_score: Optional[float] = None
    rrf_score: Optional[float] = None
    retrieval_method: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RAGRetrieveResponse(BaseModel):
    query: str
    rewritten_query: str
    route: str
    financial_year_hint: Optional[str]
    retrieved_count: int
    chunks: List[ChunkResponse]
    routing: Dict[str, Any]


class RAGCitationResponse(BaseModel):
    document_id: Optional[str]
    document_chunk_id: Optional[str]
    document_title: Optional[str]
    page_number: Optional[int]
    section: Optional[str]
    excerpt: str
    source_url: Optional[str]
    confidence_score: float


class RAGChatResponse(BaseModel):
    message_id: str
    session_id: str
    role: str
    content: str
    message_type: str
    tokens_used: int
    retrieved_count: int
    route: str
    citations: List[RAGCitationResponse]


class RAGDocumentStatsResponse(BaseModel):
    document_id: str
    status: str
    total_pages: int
    total_chunks: int
    actual_chunk_count: int
    document_type: Optional[str]
    financial_year: Optional[str]
    file_hash: Optional[str]
    embedding_model: str
    embedding_dimension: int


class RAGConfigResponse(BaseModel):
    id: str
    config_version: str
    is_active: bool
    embedding_model: str
    embedding_dimension: int
    embedding_batch_size: int
    embedding_device: str
    chunk_strategy: str
    chunk_size: int
    chunk_overlap: int
    max_chunk_size: int
    min_chunk_size: int
    table_aware_chunking: bool
    semantic_chunking: bool
    parent_child_chunking: bool
    retrieval_top_k: int
    min_similarity_score: float
    hybrid_search_enabled: bool
    vector_weight: float
    keyword_weight: float
    rrf_k: int
    reranking_enabled: bool
    reranking_model: str
    reranking_top_k: int
    llm_provider: str
    llm_model: str
    llm_temperature: float
    llm_max_tokens: int
    require_citations: bool
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class RAGHealthResponse(BaseModel):
    status: str
    embedding_engine: Dict[str, Any]
    pgvector_available: bool
    hybrid_search_available: bool
    reranker_available: bool
    total_chunks_indexed: int
    total_documents_processed: int
    active_config_version: str
    mongodb: Optional[Dict[str, Any]] = None


class EvaluationMetrics(BaseModel):
    retrieval_recall_at_k: Optional[float]
    retrieval_precision_at_k: Optional[float]
    mean_reciprocal_rank: Optional[float]
    context_relevance: Optional[float]
    faithfulness: Optional[float]
    answer_relevance: Optional[float]
    embedding_latency_ms: Optional[float]
    retrieval_latency_ms: Optional[float]
    total_latency_ms: Optional[float]


class RAGEvaluationResponse(BaseModel):
    status: str
    queries_evaluated: int
    metrics: EvaluationMetrics
    details: Optional[List[Dict[str, Any]]]


class RAGMetricsResponse(BaseModel):
    total_documents: int
    processed_documents: int
    failed_documents: int
    total_chunks: int
    avg_chunks_per_document: float
    embedding_model: str
    embedding_dimension: int
    last_ingestion: Optional[str]
