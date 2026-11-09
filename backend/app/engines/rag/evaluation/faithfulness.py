"""
ALPHANEXUS – RAG Faithfulness & Hallucination Evaluator
======================================================
Verifies whether assertions in LLM answers are strictly grounded in retrieved evidence chunks.
"""

from typing import List, Dict, Any


def evaluate_faithfulness(answer: str, context_chunks: List[str]) -> float:
    """Computes heuristic faithfulness ratio between claims and context tokens."""
    if not answer or not context_chunks:
        return 0.0
    ans_words = set(answer.lower().split())
    ctx_words = set(" ".join(context_chunks).lower().split())
    overlap = len(ans_words.intersection(ctx_words))
    return min(1.0, overlap / max(1, len(ans_words) * 0.7))
