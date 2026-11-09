# ALPHANEXUS – Coding Standards & Conventions

1. **Python Version:** Python 3.10+ with strict type hints on all public methods.
2. **Deterministic Financial Math:** Never let an LLM perform mathematical arithmetic or ratio division. All calculations must reside in `app.engines.financial`.
3. **Pydantic Validation:** All incoming API payloads and outgoing responses must be typed via Pydantic v2 models in `app.schemas`.
4. **Clean Code & Modularity:** No monolithic single-file engines; separate chunking, extraction, embeddings, vector stores, and rerankers into dedicated modules.
5. **No Secret Commits:** Never stage or commit `.env` or credential strings. Use `.env.example` with dummy values.
