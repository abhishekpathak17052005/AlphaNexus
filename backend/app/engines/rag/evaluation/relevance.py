"""
ALPHANEXUS – RAG Context & Answer Relevance Evaluator
=====================================================
Measures reciprocal rank and cosine similarity between user query and retrieved passages.
"""

from app.engines.rag.evaluation import RAGEvaluator, rag_evaluator

__all__ = ["RAGEvaluator", "rag_evaluator"]
