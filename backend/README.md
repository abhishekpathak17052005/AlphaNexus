# ALPHANEXUS Backend – Financial Intelligence & RAG API

High-performance asynchronous backend powering **ALPHANEXUS** ("See Beyond the Stock Price"). Built on FastAPI, SQLAlchemy, PostgreSQL (pgvector), MongoDB Atlas Vector Search, LangChain, and Sentence Transformers.

---

## Architecture Overview

```
backend/
├── app/
│   ├── api/                 # API routers, dependency injection, and v1 endpoints
│   │   ├── dependencies.py  # Session & auth dependencies
│   │   ├── routes/          # Domain route controllers
│   │   └── v1/              # v1 endpoint specifications
│   ├── core/                # Configuration, logging, DB pool, and engine registry
│   ├── database/            # MongoDB and PostgreSQL repository layer
│   ├── engines/             # Core computational engines:
│   │   ├── rag/             # Dense RAG, chunking, embeddings, hybrid retrieval
│   │   ├── financial/       # Deterministic ratio analysis & peer metrics
│   │   ├── forecasting/     # Econometric projection models & scenarios
│   │   └── news/            # NLP event classification & sentiment scoring
│   ├── integrations/        # Gemini, Groq, DhanHQ, Marketaux, and FMP adapters
│   ├── models/              # SQLAlchemy relational models
│   ├── schemas/             # Pydantic request and response schemas
│   ├── services/            # Application business logic layer
│   ├── utils/               # File validation, date math, text processing
│   └── workers/             # Background ingestion and indexing workers
├── alembic/                 # Database migrations
└── main.py                  # FastAPI application entrypoint
```

---

## Quickstart

```bash
# Activate virtual environment
source .venv/bin/activate

# Start development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation available at `http://localhost:8000/docs`.

