# ALPHANEXUS – FastAPI Endpoints Reference

Base URL: `http://localhost:8000/api/v1`

## 1. Health & Diagnostics
- `GET /health` – System uptime, database reachability, and engine availability.
- `GET /health/engines` – Status of RAG, Analytics, Forecasting, and News engines.

## 2. Companies & Equities
- `GET /companies` – List active companies with search, sector, and exchange filters.
- `GET /companies/{symbol}` – Get detailed company overview and fundamental snapshot.
- `GET /companies/{symbol}/metrics` – Historical financial statements and ratios.

## 3. Financial RAG Engine
- `POST /documents/upload` – Upload financial PDF/DOCX for parsing & vector indexing.
- `GET /documents` – List processed documents and ingestion status.
- `POST /research/chat` – Conversational RAG with source page citations.
- `POST /rag/retrieve` – Direct similarity retrieval for research tools.

## 4. News & Corporate Events
- `GET /news` – Market news with sentiment score and event classification.
- `GET /corporate-actions` – Dividends, stock splits, bonus issues, and AGM notices.

## 5. Forecasting
- `GET /forecasts/{symbol}` – Multi-scenario forecast projections (Base, Bull, Bear).

