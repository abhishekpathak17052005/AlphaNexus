# EquiLens AI – API Integration & Connectivity Audit Report

**Date of Audit:** November 9, 2026  
**Audit Conducted By:** Senior Backend, API Integration & DevOps Engineering Team  
**Platform Version:** 1.0.0  
**Data Mode:** Hybrid (Live Authenticated APIs with Graceful Fixture Fallbacks)  

---

## 1. Executive Summary

A comprehensive, live integration audit was conducted across all external third-party services, AI foundation models, relational and vector databases, market data providers, news aggregation endpoints, and telemetry infrastructure configured in EquiLens AI.

### Status Overview
- **Total External Services Audited:** 9
- **Fully Connected & Operational (Live HTTP 200/207):** 6 (Google Gemini, Groq, Supabase PostgreSQL 17, pgvector 0.8.2, Marketaux, Langfuse)
- **Degraded / Plan Restricted (Graceful Fallback Active):** 2 (DhanHQ - Code 806; FMP - HTTP 402 for Indian Equities)
- **Not Configured:** 1 (Sentry - `SENTRY_DSN` empty)
- **Critical Failures / Unhandled Outages:** **0**

---

## 2. API Integration Matrix

| Provider | Service Role | Auth Status | Live Status | Protocol / Endpoint | Measured Latency | HTTP Status | Operational Finding / Notes |
|---|---|---|---|---|---|---|---|
| **Google Gemini** | LLM Synthesis & RAG Research | Authenticated | **Connected** | `generativelanguage.googleapis.com/v1beta` | 3,740 ms | `200 OK` | `gemini-1.5-flash` model identifier deprecated; automatically upgraded/fallback to `gemini-3.5-flash` and `gemini-3.8-flash`. Token tracking verified. |
| **Groq Cloud** | High-Speed LLM Inference | Authenticated | **Connected** | `api.groq.com/openai/v1/chat/completions` | 391 ms | `200 OK` | `llama-3.3-70b-versatile` unavailable on current tier (404); resiliently resolved to `qwen/qwen3.8-27b` and `openai/gpt-oss-120b`. Sub-second latency. |
| **Supabase PostgreSQL** | Relational Database & Master Storage | Authenticated | **Connected** | `db.ceedxgiuppobapaypxnb.supabase.co:5432/postgres` | 916 ms | `200 OK` | PostgreSQL 17.11 verified. Special `@` character in credentials safely URL-encoded (`%40`). All 18 relational tables migrated and verified. |
| **pgvector** | Vector Similarity Search | Authenticated | **Connected** | PostgreSQL Extension (`extname='vector'`) | 5 ms | `200 OK` | Version 0.8.2 active on Supabase. Cosine distance similarity operators (`<=>`) enabled for 384-dimensional dense embeddings. |
| **DhanHQ** | Indian Market Data (NSE & BSE) | Authenticated | **Degraded** | `api.dhan.co/v2/fundlimit` & `/marketfeed/ltp` | 180 ms | `200 OK` / `401` | Client ID and JWT token are valid (funds balance returned `200 OK`). Marketfeed LTP returned `"806": "Data APIs not Subscribed"`. Safe fallback to verified NSE/BSE fixtures. |
| **Marketaux** | Financial News & Announcements | Authenticated | **Connected** | `api.marketaux.com/v1/news/all` | 911 ms | `200 OK` | Live queries return authentic Indian financial headlines with source URLs and timestamps. Quota tracking active (`x-usagelimit-remaining: 95`). |
| **Financial Modeling Prep** | Fundamental Financials | Authenticated | **Degraded** | `financialmodelingprep.com/stable/profile` | 1,332 ms | `200 OK` / `402` | Global equities (`AAPL`) return valid profiles (`200 OK`). Indian equities (`.NS`/`.BO`) return `HTTP 402 Payment Required` (requires FMP Global plan). |
| **Langfuse** | LLM Tracing & Observability | Authenticated | **Connected** | `us.cloud.langfuse.com/api/public/ingestion` | 1,534 ms | `207 Multi-Status` | Authenticated against Langfuse US region (`us.cloud.langfuse.com`). Ingestion and trace delivery verified. |
| **Sentry** | Production Exception Tracking | Unconfigured | **Disabled** | N/A | 0 ms | `N/A` | `SENTRY_DSN` is empty. Local structured logging remains active. |

---

## 3. Detailed Provider Diagnostic Findings

### A. Google Gemini
- **Configured Key:** Active and authorized.
- **Model Compatibility:** `gemini-1.5-flash` returned `404 Not Found` as Google has transitioned to Gemini 2.5 / 3.5 / 3.8.
- **Empirical Fix:** Provider adapter now transparently supports `gemini-3.5-flash` and `gemini-3.8-flash`. Live test response: *"Tata Consultancy Services (TCS) reported an operating margin of 24.6% for FY24."*

### B. Groq Inference
- **Configured Key:** Active and authorized.
- **Model Compatibility:** `llama-3.3-70b-versatile` returned `404 model_not_found`. Groq endpoint model discovery identified `qwen/qwen3.8-27b` and `openai/gpt-oss-120b`.
- **Empirical Fix:** Provider adapter added fallback to `qwen/qwen3.8-27b`. Generates sub-second responses (391 ms latency, 24 tokens).

### C. Supabase & pgvector
- **Host:** `db.ceedxgiuppobapaypxnb.supabase.co:5432`
- **Engine:** PostgreSQL 17.11 on x86_64-pc-linux-gnu.
- **Credential Normalization:** Database passwords containing special characters (e.g., `@`) are now URL-percent-encoded (`%40`) via `normalize_db_url()`, avoiding DNS misparsing errors.
- **Extension:** `CREATE EXTENSION IF NOT EXISTS vector;` executed; pgvector v0.8.2 enabled.
- **Schema:** All 18 relational tables created and Alembic revision stamped at `b232c19f2190`.

### D. DhanHQ (NSE/BSE)
- **Client ID & Access Token:** Verified via `/v2/fundlimit` (HTTP 200, returned active balance `₹8,326.35`).
- **Data Entitlement:** `/v2/marketfeed/ltp` returned `"data": {"806": "Data APIs not Subscribed"}`.
- **Handling:** Rather than failing, the system identifies the subscription tier constraint, logs a structured notice, and falls back to verified historical market data fixtures.

### E. Marketaux News
- **Token:** Valid and verified.
- **Request:** `GET /v1/news/all` with keyword search for Indian market news returned HTTP 200 with 3 live articles, publication timestamps, and publisher URLs. Rate limit remaining: 95 calls.

### F. Financial Modeling Prep (FMP)
- **Token:** Valid on modern `/stable` endpoints.
- **US Equities (`AAPL`):** HTTP 200 with full fundamental profile (Market cap: $4.99T, Price: $342.37).
- **Indian Equities (`RELIANCE.NS`, `TCS.NS`):** HTTP 402 (*"Special Endpoint: This value set for 'symbol' is not available under your current subscription"*).
- **Handling:** Explicitly documented as a plan restriction. Indian company financials are supplied by the verified local fundamental data engine and official filings.

### G. Langfuse Observability
- **Host Region Conflict:** `.env` originally specified `LANGFUSE_HOST=https://cloud.langfuse.com` (EU region), causing `401 Unauthorized` for a US-region API key.
- **Resolution:** Added `LANGFUSE_BASE_URL` and `effective_langfuse_host` resolving to `https://us.cloud.langfuse.com`. Authentication succeeded with HTTP 207 (Multi-Status Accepted).

---

## 4. Architectural & Safety Mitigations Implemented

1. **RFC 3986 URL Encoding in Database Engine:** `normalize_db_url()` automatically parses URLs from the rightmost `@` to guarantee credentials with symbols never corrupt hostname resolution.
2. **LLM Provider Graceful Fallbacks:** Both Gemini and Groq adapters now catch model retirement 404 errors and switch to currently supported models without halting user queries.
3. **No Hardcoded Secrets:** All secrets, keys, and tokens remain strictly inside ignored environment files. Zero credentials printed to logs or documentation.
4. **Administrative Audit Endpoint:** Exposed `GET /api/v1/health/integrations` providing live monitoring metrics to the terminal UI without leaking authorization headers.
