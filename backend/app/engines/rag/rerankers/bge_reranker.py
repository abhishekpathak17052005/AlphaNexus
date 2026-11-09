"""
EquiLens AI – BGE Reranker
===========================
Optional cross-encoder reranking step using FlagEmbedding's BGE Reranker.
Can be toggled on/off per request via RAG configuration.

When enabled:
  1. Retrieve top_k * 3 candidates via hybrid search
  2. Score each (query, chunk) pair with cross-encoder
  3. Return top_k by reranker score

When disabled: skip entirely (zero latency overhead).

Model: BAAI/bge-reranker-base (default, ~280M params)
Alternative: BAAI/bge-reranker-large (~560M params, higher quality)
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger

# Singleton
_reranker_instance = None
_reranker_failed = False


class BGEReranker:
    """
    Cross-encoder reranker for RAG result refinement.
    Loaded lazily to avoid import overhead when reranking is disabled.
    """

    DEFAULT_MODEL = "BAAI/bge-reranker-base"

    def __init__(self, model_name: Optional[str] = None, top_k: int = 5):
        self.model_name = model_name or self.DEFAULT_MODEL
        self.top_k = top_k
        self._model = None
        self._available = False
        self._load()

    def _load(self) -> None:
        global _reranker_instance, _reranker_failed
        if _reranker_failed:
            return
        if _reranker_instance is not None:
            self._model = _reranker_instance
            self._available = True
            return
        try:
            from FlagEmbedding import FlagReranker
            logger.info(f"[Reranker] Loading {self.model_name}…")
            _reranker_instance = FlagReranker(self.model_name, use_fp16=True)
            self._model = _reranker_instance
            self._available = True
            logger.info(f"[Reranker] {self.model_name} loaded successfully.")
        except Exception as exc:
            _reranker_failed = True
            logger.warning(
                f"[Reranker] Could not load {self.model_name}: {exc}. "
                f"Reranking will be skipped."
            )

    @property
    def is_available(self) -> bool:
        return self._available and self._model is not None

    def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Rerank candidate chunks by cross-encoder score.

        Args:
            query: User query string
            candidates: List of chunk dicts (must have 'content' or 'clean_text')
            top_k: How many to return (defaults to self.top_k)

        Returns:
            Sorted list with 'rerank_score' added to each dict.
        """
        k = top_k or self.top_k
        if not self.is_available or not candidates:
            return candidates[:k]

        try:
            pairs = [
                (query, (c.get("clean_text") or c.get("content") or "")[:512])
                for c in candidates
            ]
            scores = self._model.compute_score(pairs, normalize=True)
            if not isinstance(scores, list):
                scores = list(scores)

            for c, sc in zip(candidates, scores):
                c["rerank_score"] = round(float(sc), 4)

            candidates.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
            return candidates[:k]

        except Exception as exc:
            logger.error(f"[Reranker] Error during reranking: {exc}")
            return candidates[:k]


# Module singleton (lazy load – only initialises when first accessed)
_reranker: Optional[BGEReranker] = None


def get_reranker() -> BGEReranker:
    global _reranker
    if _reranker is None:
        _reranker = BGEReranker()
    return _reranker
