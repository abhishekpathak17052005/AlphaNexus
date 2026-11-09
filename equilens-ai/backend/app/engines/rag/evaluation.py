"""
EquiLens AI – RAG Evaluation Engine
=====================================
Deterministic retrieval evaluation suite for the financial RAG pipeline.

Test categories:
  1. Company-specific retrieval (RELIANCE, TCS, HDFCBANK chunks)
  2. Financial year retrieval (FY24 vs FY23 specificity)
  3. Consolidated vs standalone distinction
  4. Financial table retrieval
  5. Cross-year comparison
  6. Missing information handling (graceful no-result)

Metrics:
  - Recall@K, Precision@K (when ground-truth chunk IDs available)
  - Mean Reciprocal Rank
  - Context relevance (keyword overlap heuristic)
  - Embedding latency, retrieval latency, total latency
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.logging import logger

# Module-level cache for last evaluation results
_last_results: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Test query bank
# ---------------------------------------------------------------------------

EVAL_QUERIES = [
    # Company-specific
    {
        "query": "What are Reliance Industries key capital expenditure initiatives in green energy?",
        "company_hint": "RELIANCE",
        "financial_year": "FY24",
        "expected_keywords": ["capex", "green energy", "jamnagar", "giga", "solar"],
        "category": "company_specific",
    },
    {
        "query": "Explain TCS operating margin expansion and subcontractor expense management",
        "company_hint": "TCS",
        "financial_year": "FY24",
        "expected_keywords": ["operating margin", "subcontractor", "24.6", "tcv"],
        "category": "company_specific",
    },
    {
        "query": "What is HDFC Bank asset quality and GNPA ratio?",
        "company_hint": "HDFCBANK",
        "expected_keywords": ["gnpa", "npa", "provision", "1.24"],
        "category": "company_specific",
    },
    # Financial year retrieval
    {
        "query": "Infosys revenue for FY24",
        "company_hint": "INFY",
        "financial_year": "FY24",
        "expected_keywords": ["revenue", "153670", "fy24", "topaz"],
        "category": "fy_specific",
    },
    # Table retrieval
    {
        "query": "L&T order book breakdown and segment revenue",
        "company_hint": "LT",
        "expected_keywords": ["order book", "crore", "segment"],
        "category": "table_retrieval",
    },
    # Cross-year comparison
    {
        "query": "Compare Reliance revenue growth from FY21 to FY24",
        "company_hint": "RELIANCE",
        "expected_keywords": ["fy21", "fy24", "revenue", "growth"],
        "category": "cross_year",
    },
    # Missing information (should return graceful empty or low-score result)
    {
        "query": "Quantum computing investments by Infosys in FY19",
        "company_hint": "INFY",
        "financial_year": "FY19",
        "expected_keywords": [],
        "category": "missing_info",
    },
]


def _keyword_overlap(text: str, keywords: List[str]) -> float:
    """Simple keyword recall metric: fraction of expected keywords found in text."""
    if not keywords:
        return 1.0  # no expected keywords = trivially satisfied
    text_lower = text.lower()
    hits = sum(1 for kw in keywords if kw.lower() in text_lower)
    return hits / len(keywords)


def run_retrieval_evaluation(db: Session) -> Dict[str, Any]:
    """
    Execute the test query bank against the live RAG pipeline.
    Returns metrics and per-query details.
    """
    global _last_results

    from app.engines.rag.embeddings import embedding_engine
    from app.engines.rag.vector_store import vector_store
    from app.engines.rag.query_router import query_router
    from app.models.company import Company

    t_start = time.monotonic()
    details = []
    total_recall = 0.0
    total_mrr = 0.0
    total_context_rel = 0.0
    emb_latencies = []
    ret_latencies = []
    queries_with_results = 0

    for test in EVAL_QUERIES:
        query = test["query"]
        company_hint = test.get("company_hint")
        fy = test.get("financial_year")
        expected_kws = test.get("expected_keywords", [])

        # Resolve company UUID
        comp_uuid = None
        if company_hint:
            c = db.query(Company).filter(Company.symbol == company_hint).first()
            if c:
                comp_uuid = str(c.id)

        # Embed
        t0 = time.monotonic()
        routing = query_router.route(query, company_hint=company_hint)
        q_vec = embedding_engine.generate_query_embedding(routing.rewritten_queries[0])
        emb_lat = (time.monotonic() - t0) * 1000

        # Retrieve (hybrid)
        t1 = time.monotonic()
        results = vector_store.hybrid_search(
            db=db,
            query=routing.rewritten_queries[0],
            query_embedding=q_vec,
            company_id=comp_uuid,
            financial_year=fy,
            top_k=5,
        )
        ret_lat = (time.monotonic() - t1) * 1000

        emb_latencies.append(emb_lat)
        ret_latencies.append(ret_lat)

        # Compute context relevance (keyword overlap in top chunk)
        if results:
            queries_with_results += 1
            top_text = (results[0].get("clean_text") or results[0].get("content") or "")
            context_rel = _keyword_overlap(top_text, expected_kws)

            # MRR: first chunk that contains any expected keyword
            mrr = 0.0
            for rank, r in enumerate(results, 1):
                chunk_text = (r.get("clean_text") or r.get("content") or "").lower()
                if any(kw.lower() in chunk_text for kw in expected_kws if kw):
                    mrr = 1.0 / rank
                    break

            total_context_rel += context_rel
            total_mrr += mrr
        else:
            context_rel = 0.0
            mrr = 0.0
            if test["category"] == "missing_info":
                # Expected no results – treat as success
                total_context_rel += 1.0
                total_mrr += 1.0
                queries_with_results += 1

        details.append({
            "query": query,
            "company": company_hint,
            "financial_year": fy,
            "category": test["category"],
            "results_found": len(results),
            "context_relevance": round(context_rel, 3),
            "mrr": round(mrr, 3),
            "top_result": {
                "document": results[0].get("document_title") if results else None,
                "page": results[0].get("page_number") if results else None,
                "score": results[0].get("rrf_score") or results[0].get("similarity_score") if results else 0,
            },
            "embedding_latency_ms": round(emb_lat, 1),
            "retrieval_latency_ms": round(ret_lat, 1),
        })

    n = len(EVAL_QUERIES)
    total_elapsed = round((time.monotonic() - t_start) * 1000, 1)

    metrics = {
        "retrieval_recall_at_k": None,  # requires ground-truth chunk IDs
        "retrieval_precision_at_k": None,
        "mean_reciprocal_rank": round(total_mrr / n, 3) if n > 0 else 0.0,
        "context_relevance": round(total_context_rel / n, 3) if n > 0 else 0.0,
        "faithfulness": None,          # requires LLM judge
        "answer_relevance": None,
        "embedding_latency_ms": round(sum(emb_latencies) / len(emb_latencies), 1) if emb_latencies else 0,
        "retrieval_latency_ms": round(sum(ret_latencies) / len(ret_latencies), 1) if ret_latencies else 0,
        "total_latency_ms": total_elapsed,
    }

    _last_results = {
        "status": "completed",
        "queries_evaluated": n,
        "queries_with_results": queries_with_results,
        "metrics": metrics,
        "details": details,
    }

    logger.info(
        f"[Evaluation] Completed {n} queries | "
        f"MRR={metrics['mean_reciprocal_rank']} | "
        f"ContextRel={metrics['context_relevance']} | "
        f"TotalTime={total_elapsed}ms"
    )
    return _last_results


def get_last_evaluation_results() -> Dict[str, Any]:
    if _last_results is None:
        return {
            "status": "not_run",
            "queries_evaluated": 0,
            "metrics": {
                "retrieval_recall_at_k": None,
                "retrieval_precision_at_k": None,
                "mean_reciprocal_rank": None,
                "context_relevance": None,
                "faithfulness": None,
                "answer_relevance": None,
                "embedding_latency_ms": None,
                "retrieval_latency_ms": None,
                "total_latency_ms": None,
            },
            "details": None,
        }
    return _last_results
