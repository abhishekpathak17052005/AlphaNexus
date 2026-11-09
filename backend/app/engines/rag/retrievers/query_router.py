"""
ALPHANEXUS – LangChain Query Router & Intent Classifier
=======================================================
Multi-route dispatcher distinguishing quantitative queries, document Q&A, news, and forecasts.
"""

from app.engines.rag.query_router import QueryRouter, QueryRoute, query_router

__all__ = ["QueryRouter", "QueryRoute", "query_router"]
