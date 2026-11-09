# ALPHANEXUS – Backend Architecture

## 1. Overview

The backend is built with **FastAPI** providing high-concurrency asynchronous execution, structured dependency injection, and clean separation of concerns.

---

## 2. Directory Layout & Flow

```
backend/
├── app/
│   ├── main.py              # Application entrypoint & lifespan management
│   ├── api/                 # Endpoint routers & dependency injection
│   │   ├── dependencies.py  # Session & token resolution
│   │   ├── routes/          # Domain controller routers
│   │   └── v1/              # v1 endpoint handlers
│   ├── core/                # Configuration, logging, DB pool, engine registry
│   ├── database/            # MongoDB & PostgreSQL repository implementations
│   ├── engines/             # Core algorithms (RAG, Financial, News, Forecast)
│   ├── integrations/        # Adapters for external APIs (Gemini, Groq, Dhan, etc.)
│   ├── models/              # SQLAlchemy relational models
│   ├── schemas/             # Pydantic v2 schemas
│   ├── services/            # Application business logic layer
│   ├── utils/               # File validators, helpers, date utilities
│   └── workers/             # Asynchronous ingestion and task workers
```

---

## 3. Lifespan & Central Registry

On startup:
1. `Base.metadata.create_all()` verifies that database tables exist.
2. `seed_initial_market_data()` checks if demo tickers are present and populates them if empty.
3. `engine_registry.initialize_engines()` probes the availability of all external services and initializes embedding models and LLM adapters.
