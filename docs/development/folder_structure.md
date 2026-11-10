# ALPHANEXUS – Target Repository Folder Structure

```
ALPHANEXUS/
├── README.md                # Platform overview and quickstart
├── LICENSE                  # Apache 2.0 license
├── .gitignore               # Strict exclusion of .env, logs, pycache
├── .env.example             # Sanitzed environment template
├── pyproject.toml           # Unified packaging configuration
├── requirements.txt         # Root dependency list
├── Makefile                 # Developer build and run targets
│
├── frontend/                # Streamlit UI & Liquid Glass components
│   ├── streamlit_app.py     # Streamlit entrypoint
│   ├── config/              # Themes, tokens, settings, navigation
│   ├── api/                 # Backend API client wrappers
│   ├── pages/               # 8 analyst workspace pages
│   ├── components/          # Reusable Liquid Glass UI modules
│   ├── custom_components/   # React Vite fluid navigation component
│   └── styles/              # Modular CSS sheets
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py          # FastAPI application server
│   │   ├── api/             # Routes, dependencies, v1 endpoints
│   │   ├── core/            # Config, DB connections, engine registry
│   │   ├── database/        # Repositories & MongoDB connection
│   │   ├── engines/         # RAG, Financial, News, Forecasting
│   │   ├── integrations/    # External LLM, Market, News adapters
│   │   ├── models/          # SQLAlchemy relational models
│   │   ├── schemas/         # Pydantic v2 validation models
│   │   ├── services/        # Business logic service layer
│   │   └── workers/         # Background tasks & document ingestion
│   ├── alembic/             # Migration scripts
│   └── requirements.txt     # Backend specific dependencies
│
├── tests/                   # Test suites
│   ├── unit/                # Unit tests for RAG, finance, forecasting, news
│   ├── integration/         # API and DB integration tests
│   └── e2e/                 # Full analyst workflow tests
│
├── configs/                 # YAML operational configurations
├── scripts/                 # Administration and database scripts
├── data/                    # Document uploads, datasets, and cache
├── models/                  # ML embeddings & forecasting model weights
└── docs/                    # Architecture and developer documentation
```

