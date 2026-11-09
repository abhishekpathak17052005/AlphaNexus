"""
EquiLens AI – RAG & Research API Module
=======================================
Communicates with FastAPI /rag and /research endpoints for multi-turn research chat,
chunk retrieval, configuration, and diagnostics.
"""

from typing import Any, Dict, List, Optional
from api.client import api_client


def query_rag(
    query: str,
    company_id: Optional[str] = None,
    financial_year: Optional[str] = None,
    document_type: Optional[str] = None,
    top_k: int = 8,
    hybrid: bool = True,
    reranking: bool = False,
) -> Dict[str, Any]:
    payload = {
        "query": query,
        "company_id": company_id,
        "financial_year": financial_year,
        "document_type": document_type,
        "top_k": top_k,
        "hybrid": hybrid,
        "reranking": reranking,
    }
    return api_client.post("rag/query", json_data=payload)


def chat_rag(
    session_id: str,
    user_query: str,
    company_id: Optional[str] = None,
    financial_year: Optional[str] = None,
    document_type: Optional[str] = None,
    top_k: int = 8,
    hybrid: bool = True,
    reranking: bool = False,
) -> Dict[str, Any]:
    payload = {
        "session_id": session_id,
        "query": user_query,
        "company_id": company_id,
        "financial_year": financial_year,
        "document_type": document_type,
        "top_k": top_k,
        "hybrid": hybrid,
        "reranking": reranking,
    }
    return api_client.post("rag/chat", json_data=payload)


def retrieve_chunks(
    query: str,
    company_id: Optional[str] = None,
    financial_year: Optional[str] = None,
    document_type: Optional[str] = None,
    top_k: int = 8,
    min_similarity: float = 0.0,
    hybrid: bool = True,
    reranking: bool = False,
) -> Dict[str, Any]:
    payload = {
        "query": query,
        "company_id": company_id,
        "financial_year": financial_year,
        "document_type": document_type,
        "top_k": top_k,
        "min_similarity": min_similarity,
        "hybrid": hybrid,
        "reranking": reranking,
    }
    return api_client.post("rag/retrieve", json_data=payload)


def get_rag_config() -> Dict[str, Any]:
    return api_client.get("rag/config")


def update_rag_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
    return api_client.put("rag/config", json_data=config_data)


def get_rag_health() -> Dict[str, Any]:
    return api_client.get("rag/health")


def get_rag_metrics() -> Dict[str, Any]:
    return api_client.get("rag/metrics")


def get_sessions(company_id: Optional[str] = None) -> List[Dict[str, Any]]:
    params = {}
    if company_id:
        params["company_id"] = company_id
    res = api_client.get("rag/sessions", params=params)
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and "error" not in res:
        return res.get("items", [])
    return []


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    res = api_client.get(f"rag/sessions/{session_id}")
    if isinstance(res, dict) and "error" not in res:
        return res
    return None

