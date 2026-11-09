"""
EquiLens AI – Production Embedding Engine
==========================================
Manages Sentence Transformer model lifecycle for financial document intelligence.
Supports BAAI/bge-base-en-v1.5 (768-d) as primary and bge-small (384-d) as
lightweight alternative.  The active model is determined by EMBEDDING_MODEL_NAME
and EMBEDDING_DIMENSION in settings, making it trivial to swap without code changes.

IMPORTANT: Never mix embeddings from different model families inside the same
pgvector index – rebuild the index and re-embed all documents when changing models.
"""

from __future__ import annotations

import hashlib
import time
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

import numpy as np

from app.core.config import settings
from app.core.logging import logger

# ---------------------------------------------------------------------------
# BGE model query instruction prefix (improves retrieval quality)
# ---------------------------------------------------------------------------
_BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

# ---------------------------------------------------------------------------
# Model dimension registry – prevents index contamination
# ---------------------------------------------------------------------------
KNOWN_MODEL_DIMENSIONS: Dict[str, int] = {
    "BAAI/bge-small-en-v1.5": 384,
    "BAAI/bge-base-en-v1.5": 768,
    "BAAI/bge-large-en-v1.5": 1024,
    "BAAI/bge-m3": 1024,
}

# Module-level singleton – loaded once, reused across all requests
_model_instance = None
_model_failed = False
_model_info: Dict[str, Any] = {}


@dataclass
class EmbeddingModelInfo:
    model_name: str
    dimension: int
    device: str
    max_seq_length: int
    loaded: bool
    fallback_mode: bool
    load_time_s: float = 0.0
    version_tag: str = ""


class EmbeddingEngine:
    """
    Production embedding engine for EquiLens AI financial RAG pipeline.

    Design decisions:
    - Singleton model instance (load once, reuse)
    - Normalised embeddings (L2) → cosine similarity via dot-product
    - BGE query instruction applied at query time only (not document time)
    - Batch encode with configurable batch_size
    - Deterministic SHA-256 fallback if model load fails (consistent, not semantic)
    - Embedding dimension validated against known model registry
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        dimension: Optional[int] = None,
        device: Optional[str] = None,
        batch_size: int = 32,
        max_seq_length: int = 512,
    ):
        self.model_name: str = model_name or settings.EMBEDDING_MODEL_NAME
        self.dimension: int = dimension or settings.EMBEDDING_DIMENSION
        self.device: str = device or settings.EMBEDDING_DEVICE
        self.batch_size = batch_size
        self.max_seq_length = max_seq_length
        self._load_model()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _load_model(self) -> None:
        global _model_instance, _model_failed, _model_info
        if _model_instance is not None or _model_failed:
            return

        # Validate dimension matches known registry
        expected = KNOWN_MODEL_DIMENSIONS.get(self.model_name)
        if expected and expected != self.dimension:
            logger.warning(
                f"Configured EMBEDDING_DIMENSION={self.dimension} does not match "
                f"known dimension for {self.model_name} ({expected}). "
                f"Correcting to {expected}."
            )
            self.dimension = expected

        t0 = time.monotonic()
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(
                f"[EmbeddingEngine] Loading {self.model_name} on {self.device} "
                f"(expected_dim={self.dimension})"
            )
            model = SentenceTransformer(self.model_name, device=self.device)
            # Optional: override max sequence length
            if hasattr(model, "max_seq_length"):
                model.max_seq_length = self.max_seq_length
            _model_instance = model
            elapsed = round(time.monotonic() - t0, 2)
            _model_info = {
                "model_name": self.model_name,
                "dimension": self.dimension,
                "device": self.device,
                "max_seq_length": self.max_seq_length,
                "loaded": True,
                "fallback_mode": False,
                "load_time_s": elapsed,
                "version_tag": f"{self.model_name}@dim{self.dimension}",
            }
            logger.info(
                f"[EmbeddingEngine] Model loaded in {elapsed}s – "
                f"version={_model_info['version_tag']}"
            )
        except Exception as exc:
            logger.warning(
                f"[EmbeddingEngine] Failed to load SentenceTransformer: {exc}. "
                f"Activating deterministic fallback embeddings."
            )
            _model_failed = True
            _model_info = {
                "model_name": self.model_name,
                "dimension": self.dimension,
                "device": self.device,
                "loaded": False,
                "fallback_mode": True,
                "load_time_s": 0.0,
                "version_tag": f"fallback@dim{self.dimension}",
            }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_model_info(self) -> Dict[str, Any]:
        """Returns runtime model metadata including dimension and version tag."""
        return dict(_model_info)

    def warm_up(self) -> None:
        """Run a single dummy encode to pre-JIT the model on CPU/GPU."""
        try:
            self.get_query_embedding("warm up inference")
            logger.info("[EmbeddingEngine] Model warm-up complete.")
        except Exception as exc:
            logger.warning(f"[EmbeddingEngine] Warm-up failed: {exc}")

    def validate_embedding_dimension(self, embedding: List[float]) -> bool:
        """Returns True if the embedding vector has the expected dimension."""
        return len(embedding) == self.dimension

    def normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        """L2-normalise a 2-D numpy array of embedding vectors."""
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        return embeddings / norms

    # ------------------------------------------------------------------
    # Document embeddings (no query instruction)
    # ------------------------------------------------------------------

    def generate_document_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate normalised embeddings for document chunks.
        Does NOT prepend the BGE query instruction.
        """
        return self._encode(texts, apply_query_instruction=False)

    # ------------------------------------------------------------------
    # Query embedding (with BGE query instruction for bge models)
    # ------------------------------------------------------------------

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate a single normalised embedding for a user query.
        Prepends the BGE retrieval instruction for BGE-family models.
        """
        prefixed = (
            f"{_BGE_QUERY_INSTRUCTION}{query}"
            if "bge" in self.model_name.lower()
            else query
        )
        return self._encode([prefixed], apply_query_instruction=False)[0]

    # convenience aliases used by existing code
    def get_embedding(self, text: str) -> List[float]:
        return self.generate_query_embedding(text)

    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        return self.generate_document_embeddings(texts)

    # ------------------------------------------------------------------
    # Batch encode
    # ------------------------------------------------------------------

    def generate_embeddings_batch(
        self, texts: List[str], *, is_query: bool = False
    ) -> List[List[float]]:
        if is_query:
            return [self.generate_query_embedding(t) for t in texts]
        return self.generate_document_embeddings(texts)

    # ------------------------------------------------------------------
    # Cosine similarity utility
    # ------------------------------------------------------------------

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        a = np.array(v1, dtype=np.float32)
        b = np.array(v2, dtype=np.float32)
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0:
            return 0.0
        return float(np.dot(a, b) / (na * nb))

    # ------------------------------------------------------------------
    # Internal encode
    # ------------------------------------------------------------------

    def _encode(
        self, texts: List[str], *, apply_query_instruction: bool = False
    ) -> List[List[float]]:
        global _model_instance

        if not texts:
            return []

        if _model_instance is not None:
            try:
                raw_texts = (
                    [f"{_BGE_QUERY_INSTRUCTION}{t}" for t in texts]
                    if apply_query_instruction
                    else texts
                )
                vecs = _model_instance.encode(
                    raw_texts,
                    batch_size=self.batch_size,
                    show_progress_bar=False,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                )
                return [v.tolist() for v in vecs]
            except Exception as exc:
                logger.error(f"[EmbeddingEngine] Inference error: {exc}")

        # Deterministic fallback (SHA-256 hash projection, L2-normalised)
        return self._fallback_encode(texts)

    def _fallback_encode(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            vec = np.zeros(self.dimension, dtype=np.float32)
            for i in range(self.dimension):
                digest = hashlib.sha256(f"{i}:{text}".encode()).digest()
                val = int.from_bytes(digest[:4], "big", signed=True) / (2 ** 31)
                vec[i] = val
            norm = np.linalg.norm(vec)
            results.append((vec / norm if norm > 0 else vec).tolist())
        return results


# ---------------------------------------------------------------------------
# Module singleton – import this everywhere
# ---------------------------------------------------------------------------
embedding_engine = EmbeddingEngine()
