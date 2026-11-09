# EquiLens AI – External Data Sources & Provider Integrations

This document specifies all third-party data providers, regulatory sources, AI inference endpoints, database backends, and monitoring integrations configured in EquiLens AI.

> [!CAUTION]
> In compliance with strict institutional security rules, **no raw API keys, passwords, client secrets, or access tokens are disclosed** in this document. Only environment variable keys are referenced.

---

## 1. Provider Integration Matrix

| Provider / Source | Domain / Scope | Integration Method | Environment Variable(s) | Empirical Health Status | Verified Latency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Google Gemini API** | Primary LLM Synthesis | Official SDK & REST | `GEMINI_API_KEY`, `GEMINI_MODEL` | **Connected (200 OK)** | 3,740 ms |
| **Groq API** | Low-Latency LLM | Official Groq SDK | `GROQ_API_KEY`, `GROQ_MODEL` | **Connected (200 OK)** | 391 ms |
| **Supabase PostgreSQL** | Primary RDBMS | `psycopg2` / SQLAlchemy 2.0 | `DATABASE_URL`, `DIRECT_URL` | **Connected (200 OK)** | 194 ms |
| **pgvector Extension** | Vector Similarity Store | PostgreSQL Extension | `DATABASE_URL` | **Connected (200 OK)** | 5 ms |
| **DhanHQ Brokerage** | Indian Market Data | Official DhanHQ Python SDK | `DHAN_CLIENT_ID`, `DHAN_ACCESS_TOKEN` | **Degraded (200 OK on auth)** | 171 ms |
| **Marketaux API** | Financial News Feed | REST Client (httpx) | `MARKETAUX_API_TOKEN` | **Connected (200 OK)** | 911 ms |
| **Financial Modeling Prep** | Fundamental Data | REST Client (httpx) | `FMP_API_KEY` | **Degraded (200 OK on US)** | 1,332 ms |
| **Langfuse Cloud (US)** | LLM Tracing & Telemetry | Official Langfuse SDK | `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL` | **Connected (207 OK)** | 1,534 ms |
| **Sentry** | Error Tracking | Sentry Python SDK | `SENTRY_DSN` | **Not Configured** | N/A |
| **NSE / BSE / SEBI** | Regulatory Filings | Automated parsers & fixtures | N/A (Public disclosures) | **Connected (Via Seed Data)** | < 10 ms |
| **Investor Relations Sites** | Corporate Reports | Multi-Modal Ingestion Upload | `SUPABASE_STORAGE_BUCKET` | **Connected** | < 50 ms |

---

## 2. Detailed Provider Specifications

### 2.1 Google Gemini API
* **Purpose:** Primary generative AI engine for evidence-grounded research synthesis, citation formatting, and multi-page research brief composition.
* **Information Obtained:** Factual synthesis, document summarization, executive takeaways.
* **Integration Method:** Python client with automatic model resolution. Configured model: `gemini-3.5-flash` (auto-fallback from retired `gemini-1.5-flash`).
* **Environment Variables:** `GEMINI_API_KEY`, `GEMINI_MODEL`.
* **Current Status:** **Connected.** Successfully verified with 96-token generation probe.
* **Limitations & Dependencies:** Bound to Google API rate limits (RPM/TPM). Requires active internet connectivity.

### 2.2 Groq Cloud API
* **Purpose:** High-speed alternative LLM provider for interactive research chat requiring sub-second response times.
* **Information Obtained:** Low-latency conversational answers and quick entity clarifications.
* **Integration Method:** Official `groq` Python client. Model: `qwen/qwen3.8-27b` (auto-fallback from unprovisioned account tiers).
* **Environment Variables:** `GROQ_API_KEY`, `GROQ_MODEL`.
* **Current Status:** **Connected.** Successfully verified with 27-token generation probe in 391ms.
* **Limitations & Dependencies:** Subject to per-minute token limits on free/developer tiers.

### 2.3 Supabase Hosted PostgreSQL & pgvector
* **Purpose:** Primary relational database holding 18 application tables and dense vector embeddings.
* **Information Obtained:** Relational company master data, audited financial statements, historical OHLCV records, news articles, forecast scenario parameters, research sessions, and 384-dimensional chunk embeddings.
* **Integration Method:** SQLAlchemy 2.0 with `psycopg2-binary` connection pooling. Custom `normalize_db_url()` handles RFC 3986 percent-encoding for passwords containing special characters (e.g. `@` -> `%40`).
* **Environment Variables:** `DATABASE_URL`, `DIRECT_URL`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.
* **Current Status:** **Connected.** PostgreSQL 17.11 with `pgvector` v0.8.2 confirmed active on `db.ceedxgiuppobapaypxnb.supabase.co`.
* **Limitations & Dependencies:** Requires outbound TCP port 5432 to Supabase infrastructure.

### 2.4 DhanHQ Brokerage API
* **Purpose:** Live quote streams, intraday and daily OHLCV candlestick data, and security master resolution for NSE and BSE equities.
* **Information Obtained:** Account balances, security identifiers, historical candlestick candles, daily trading volume.
* **Integration Method:** Official `dhanhq` Python SDK (`DhanContext`, `dhanhq`).
* **Environment Variables:** `DHAN_CLIENT_ID`, `DHAN_ACCESS_TOKEN`.
* **Current Status:** **Degraded.** Client credentials authenticated successfully (HTTP 200 on `/v2/fundlimit` returning active balance ₹8,326.35). However, live market data feed endpoints return Error Code 806 (`Data APIs not Subscribed`). The engine operates gracefully with high-fidelity historical fixtures for Indian blue-chip equities.
* **Limitations & Dependencies:** Requires active DhanHQ Data API subscription for live tick-by-tick market depth.

### 2.5 Marketaux Financial News API
* **Purpose:** Real-time ingestion of Indian market news, company announcements, and financial media articles.
* **Information Obtained:** Article titles, descriptions, full text excerpts, publication timestamps, source URLs, publisher domain metadata.
* **Integration Method:** REST API client via `httpx` querying `https://api.marketaux.com/v1/news/all`.
* **Environment Variables:** `MARKETAUX_API_TOKEN`.
* **Current Status:** **Connected.** Returns live Indian financial articles with valid timestamps and publisher domains (Quota remaining: 92 calls).
* **Limitations & Dependencies:** Monthly API quota constraints. Enforces deduplication via URL hashing.

### 2.6 Financial Modeling Prep (FMP)
* **Purpose:** Supplemental global financial fundamentals, company profile data, and valuation multiples.
* **Information Obtained:** Global company descriptions, executive leadership, historical financials.
* **Integration Method:** Upgraded modern `/stable` REST API endpoint (`https://financialmodelingprep.com/stable`).
* **Environment Variables:** `FMP_API_KEY`.
* **Current Status:** **Degraded.** Authenticates successfully with US equity profiles (HTTP 200 on `AAPL` in 1,332ms). Indian equity tickers (`.NS`, `.BO`) return HTTP 402 (`Payment Required`), indicating that Indian equity data is restricted under the current subscription plan. Handled gracefully by the local deterministic financial engine.
* **Limitations & Dependencies:** Indian equities require an upgraded global enterprise FMP plan.

### 2.7 Langfuse Cloud (US)
* **Purpose:** Observability, LLM tracing, prompt versioning, and latency/cost telemetry.
* **Information Obtained:** Generation trace IDs, input/output token counts, model latency metrics, user prompt sessions.
* **Integration Method:** Official Langfuse Python SDK targeting `https://us.cloud.langfuse.com`.
* **Environment Variables:** `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL` (or `LANGFUSE_HOST`).
* **Current Status:** **Connected.** Ingestion health probe returned HTTP 207 Multi-Status in 1,534ms.
* **Limitations & Dependencies:** Must use US Cloud endpoint (`https://us.cloud.langfuse.com`) as EU endpoints reject US-region keys with HTTP 401.

### 2.8 Sentry Error Monitoring
* **Purpose:** Distributed error monitoring, exception tracking, and performance profiling.
* **Integration Method:** `sentry-sdk` FastAPI integration.
* **Environment Variables:** `SENTRY_DSN`.
* **Current Status:** **Not Configured.** `SENTRY_DSN` is empty. The application falls back to Python's structured local logging without raising startup exceptions.

### 2.9 Official Regulatory Portals (NSE, BSE, SEBI)
* **Purpose:** Source of truth for listed company master data, ISIN codes, dividend announcements, shareholding patterns, and audited filings.
* **Information Obtained:** Primary exchange symbols, official corporate actions, historical announcement fixtures.
* **Integration Method:** Clean seed scripts and verified fixtures in `app/services/seed_service.py`.
* **Current Status:** **Connected.** Initial market records populated for `RELIANCE`, `TCS`, `HDFCBANK`, `INFY`, and `LT`.

