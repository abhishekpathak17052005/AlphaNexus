# ALPHANEXUS

> **See Beyond the Stock Price.**

ALPHANEXUS is an enterprise AI-powered financial intelligence and equity research platform purpose-built for Indian listed companies (NSE & BSE) with scalable architecture for global markets.

---

## 🏛️ Architecture Overview

ALPHANEXUS organizes quantitative analytics, document intelligence, econometric forecasting, and real-time market signals into a decoupled architecture:

- **Frontend (`frontend/`):** Streamlit application with Liquid Glass-inspired UI components, dynamic light/dark theming, and responsive Plotly financial visualizations.
- **Backend (`backend/`):** Asynchronous FastAPI application exposing strict OpenAPI contracts with Pydantic validation.
- **RAG & AI Intelligence (`backend/app/engines/rag/`):** LangChain and LangGraph retrieval-augmented generation orchestrating structure-aware chunking, dense vector similarity, and sparse BM25 retrieval.
- **Vector & Storage Engines:** MongoDB Atlas Vector Search and PostgreSQL with `pgvector` hosting 768-dimensional normalized BGE embeddings.
- **Financial Analytics (`backend/app/engines/financial/`):** Strictly deterministic valuation ratios, DuPont ROE decompositions, and multi-year accounting statement tables.
- **Forecasting Engine (`backend/app/engines/forecasting/`):** Walk-forward econometric modeling generating Bull, Base, and Bear scenarios with backtested confidence intervals.

---

## 📂 Project Structure

```text
ALPHANEXUS/
├── frontend/              # Streamlit financial terminal & Liquid Glass UI
├── backend/               # FastAPI ASGI backend & AI intelligence engines
├── data/                  # Sample documents, filings, and cache storage
├── models/                # Local model configurations and artifacts
├── configs/               # System YAML configurations (RAG, logging, etc.)
├── scripts/               # Operational utility scripts and index builders
├── tests/                 # Unit, integration, and E2E test suites
└── docs/                  # Comprehensive engineering and architectural guides
```

---

## ⚡ Quick Start

### 1. Environment Configuration
```bash
cp .env.example .env
# Configure your database and API credentials in .env
```

### 2. Install Dependencies
```bash
make install
```

### 3. Launch Backend Server
```bash
make run-backend
# FastAPI running on http://127.0.0.1:8000
# OpenAPI Docs available at http://127.0.0.1:8000/docs
```

### 4. Launch Frontend Terminal
```bash
make run-frontend
# Streamlit interface running on http://127.0.0.1:8501
```

---

## 🛡️ License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.
