# ALPHANEXUS Documentation

Welcome to the comprehensive technical documentation for **ALPHANEXUS** ("See Beyond the Stock Price").

---

## Documentation Sections

### 1. Architecture
- [System Architecture](architecture/system_architecture.md) – End-to-end design, tiers, and data boundaries.
- [Frontend Architecture](architecture/frontend_architecture.md) – Streamlit multi-page workspace and React components.
- [Backend Architecture](architecture/backend_architecture.md) – FastAPI, dependency injection, and service layers.
- [Data Flow Diagram](architecture/data_flow.md) – Sequence flow from document upload to RAG synthesis.

### 2. Core Engines
- [Financial RAG Engine](engines/rag_engine.md) – Chunking, embeddings, Atlas & pgvector search, reranking.
- [Financial Analytics Engine](engines/financial_engine.md) – Deterministic ratio calculations and DuPont models.
- [News Intelligence Engine](engines/news_engine.md) – Event categorization and lexicon sentiment analysis.
- [Forecasting Engine](engines/forecasting_engine.md) – Econometric models and Monte Carlo scenarios.

### 3. Integrations
- [API Integrations](integrations/api_integrations.md) – Gemini, Groq, DhanHQ, Marketaux, FMP.
- [MongoDB Atlas Setup](integrations/mongodb_setup.md) – Vector search index definitions.
- [LLM Setup](integrations/llm_setup.md) – LLM configuration and automatic failover.

### 4. Frontend & Design System
- [Design System](frontend/design_system.md) – Liquid Glass UI principles.
- [Theme System](frontend/theme_system.md) – Dark and light theme palettes.
- [Liquid Glass Implementation](frontend/liquid_glass_ui.md) – Component usage in Streamlit.

### 5. API Reference
- [FastAPI Reference](api/api_reference.md) – Full endpoints, parameters, and schemas.

### 6. Setup & Operations
- [Installation Guide](setup/installation.md) – Step-by-step setup instructions.
- [Environment Variables](setup/environment_variables.md) – Configuration parameters.
- [Troubleshooting](setup/troubleshooting.md) – Diagnosing common errors.

### 7. Development
- [Folder Structure](development/folder_structure.md) – Directory organization.
- [Coding Standards](development/coding_standards.md) – Code quality and safety rules.
- [Testing Guide](development/testing.md) – Pytest commands and execution.
