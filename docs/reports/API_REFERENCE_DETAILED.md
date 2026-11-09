# EquiLens AI – Complete REST API Specification

**Base URL:** `http://localhost:8000/api/v1`  
**OpenAPI Specification:** Available at `/openapi.json` and interactive Swagger UI at `/docs`  
**Total Registered Endpoints:** 29 Endpoints across 10 Feature Routers

---

## 1. Health & Central Engine Registry

### `GET /health`
Returns high-level system vitality, environment mode, and database reachability.
* **Auth Required:** None
* **Query Parameters:** None
* **Response (200 OK):**
  ```json
  {
    "status": "Healthy",
    "environment": "development",
    "data_mode": "demo",
    "timestamp": "2026-11-09T09:16:41.122798",
    "database_connected": true,
    "version": "1.0.0"
  }
  ```

### `GET /health/engines`
Returns dynamic health introspection for all 11 core intelligence engines and provider adapters.
* **Auth Required:** None
* **Response (200 OK):**
  ```json
  {
    "status": "Healthy",
    "timestamp": "2026-11-09T09:16:41.122798",
    "total_engines": 11,
    "ready_count": 9,
    "degraded_count": 2,
    "disabled_count": 0,
    "failed_count": 0,
    "engines": {
      "backend": { "name": "Application Backend", "state": "Ready", "provider": "FastAPI / Python 3.13" },
      "database": { "name": "Database Engine", "state": "Ready", "provider": "PostgreSQL / Supabase" },
      "pgvector": { "name": "PostgreSQL / pgvector", "state": "Ready", "provider": "pgvector" },
      "embedding": { "name": "Embedding Model", "state": "Ready", "provider": "BAAI/bge-small-en-v1.5" },
      "llm": { "name": "LLM Provider", "state": "Ready", "provider": "Google Gemini (gemini-3.5-flash)" },
      "rag": { "name": "RAG Engine", "state": "Ready", "provider": "EquiLens RAG Core" },
      "storage": { "name": "Document Storage", "state": "Ready", "provider": "Supabase Private Storage" },
      "news": { "name": "News Engine", "state": "Ready", "provider": "Marketaux Live API" },
      "market_data": { "name": "Market Data Provider", "state": "Degraded", "details": "Operating with verified fixtures" },
      "analytics": { "name": "Financial Analytics", "state": "Ready", "provider": "Deterministic Engine (NumPy/Pandas)" },
      "forecasting": { "name": "Forecasting Engine", "state": "Ready", "provider": "Scikit-Learn / Statsmodels" }
    }
  }
  ```

### `GET /health/integrations`
Executes real-time live network probes against all 9 external service endpoints.
* **Auth Required:** None
* **Response (200 OK):**
  ```json
  {
    "timestamp": "2026-11-09T09:17:08.530429+00:00",
    "total_integrations": 9,
    "connected_count": 6,
    "degraded_count": 2,
    "failed_count": 0,
    "not_configured_count": 1,
    "integrations": [
      { "provider": "Google Gemini", "status": "Connected", "model": "gemini-3.5-flash", "http_status": 200, "latency_ms": 4563.0 },
      { "provider": "Groq", "status": "Connected", "model": "qwen/qwen3.8-27b", "http_status": 200, "latency_ms": 2136.3 },
      { "provider": "PostgreSQL / Supabase", "status": "Connected", "model": "PostgreSQL 17.11 (Supabase)", "http_status": 200, "latency_ms": 194.0 },
      { "provider": "pgvector", "status": "Connected", "model": "pgvector v0.8.2", "http_status": 200, "latency_ms": 5.0 },
      { "provider": "DhanHQ", "status": "Degraded", "model": "DhanHQ Account APIs", "http_status": 200, "latency_ms": 171.2 },
      { "provider": "Marketaux", "status": "Connected", "model": "Marketaux News v1", "http_status": 200, "latency_ms": 3581.0 },
      { "provider": "Financial Modeling Prep (FMP)", "status": "Degraded", "model": "FMP /stable", "http_status": 200, "latency_ms": 1843.9 },
      { "provider": "Langfuse", "status": "Connected", "model": "Langfuse Cloud (US)", "http_status": 207, "latency_ms": 2152.3 },
      { "provider": "Sentry", "status": "Not Configured", "model": null, "http_status": null, "latency_ms": 0 }
    ]
  }
  ```

---

## 2. Companies & Equities

### `GET /companies`
Lists tracked equities with optional filtering.
* **Query Parameters:**
  * `exchange` (string, optional): e.g. `NSE`, `BSE`.
  * `sector` (string, optional): e.g. `Energy`, `Information Technology`.
  * `search` (string, optional): Keyword search against symbol or name.
* **Response (200 OK):** Array of `CompanyResponse` objects.

### `GET /companies/search`
High-speed autocompletion for global search modal.
* **Query Parameters:** `q` (string, required): Minimum 1 character.
* **Response (200 OK):** Array of matching Company summaries.

### `GET /companies/{company_id}`
Retrieves full institutional profile, ISIN, valuation multiples, and 52-week price range.
* **Path Parameters:** `company_id` (UUID or symbol string, e.g. `RELIANCE`).
* **Response (200 OK):** Complete `CompanyResponse` schema.
* **Errors:** `404 Not Found` if symbol does not exist.

---

## 3. Financial Analytics & Peer Benchmarking

### `GET /companies/{company_id}/financials`
Returns structured historical financial metrics.
* **Query Parameters:** `period_type` (string, default: `annual`).
* **Response (200 OK):** Array of `FinancialMetricResponse` objects.

### `GET /companies/{company_id}/statements`
Returns full audited balance sheet, income statement, or cash flow statement line items.
* **Query Parameters:** `statement_type` (string, optional): `INCOME_STATEMENT`, `BALANCE_SHEET`, `CASH_FLOW`.
* **Response (200 OK):** Array of `FinancialStatementResponse` objects.

### `GET /companies/{company_id}/ratios`
Computes deterministic accounting ratios on demand.
* **Response (200 OK):**
  ```json
  {
    "company_symbol": "RELIANCE",
    "computed_metrics": {
      "revenue_growth_yoy": 10.82,
      "ebitda_margin": 17.82,
      "net_profit_margin": 6.96,
      "roe": 8.78,
      "roce": 9.42,
      "debt_to_equity": 0.44,
      "current_ratio": 1.15,
      "free_cash_flow": 15420.50
    }
  }
  ```

### `POST /companies/compare`
Calculates peer comparison matrix across 2 to 5 selected companies.
* **Request Body:**
  ```json
  {
    "company_ids": ["b6363cc5-d4fe-44c6-805c-254917dd1a2a", "c1234567-d4fe-44c6-805c-254917dd1a2b"]
  }
  ```
* **Response (200 OK):** Peer comparison matrix with sector medians and metric leaders.

---

## 4. Document Intelligence & Vector Ingestion

### `POST /documents/upload`
Uploads corporate regulatory filings (PDF, DOCX, XLSX, CSV).
* **Content-Type:** `multipart/form-data`
* **Form Fields:**
  * `company_id` (UUID, required)
  * `title` (string, required)
  * `financial_year` (string, optional: e.g. `FY24`)
  * `document_type` (string, required: `Annual Report`, `Quarterly Result`, etc.)
  * `file` (binary stream, max 50MB)
  * `auto_process` (boolean, default: `true`)
* **Response (201 Created):** `DocumentResponse` with status `UPLOADED` or `PROCESSED`.
* **Errors:** `409 Conflict` (Duplicate SHA-256 file hash), `413 Payload Too Large`.

### `GET /documents`
Lists uploaded documents.
* **Query Parameters:** `company_id` (UUID), `document_type` (string), `status` (string).
* **Response (200 OK):** Array of `DocumentResponse` objects.

### `GET /documents/{document_id}`
Retrieves document status, page count, and chunk count.
* **Response (200 OK):** `DocumentResponse` schema.

### `POST /documents/{document_id}/process`
Triggers manual re-extraction, table preservation, chunking, and vector embedding calculation.
* **Response (200 OK):** Updated `DocumentResponse`.

### `DELETE /documents/{document_id}`
Deletes document record, associated storage file, and all derived `document_chunks`.
* **Response (200 OK):** `{"status": "Deleted", "document_id": "..."}`.

---

## 5. AI Research Terminal & Conversational RAG

### `POST /research/chat`
Evidence-grounded conversational equity research query.
* **Request Body:**
  ```json
  {
    "company_id": "b6363cc5-d4fe-44c6-805c-254917dd1a2a",
    "query": "What are the key growth drivers in retail and digital services?",
    "session_id": "optional-uuid",
    "financial_year": "FY24",
    "document_type": "Annual Report",
    "top_k": 5
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "id": "e0b57fa2-16ad-45c1-84fe-fc60ea4eaee6",
    "session_id": "78901234-d4fe-44c6-805c-254917dd1a2c",
    "role": "assistant",
    "content": "According to the Reliance Industries Integrated Annual Report FY24...",
    "message_type": "fact_grounded",
    "token_count": 142,
    "citations": [
      {
        "document_title": "Reliance Industries Annual Report FY24",
        "page_number": 42,
        "section": "Financial Highlights & EBITDA",
        "excerpt": "Consolidated Revenue for FY24 crossed the milestone of ₹10,00,122 Crore...",
        "confidence_score": 0.985
      }
    ]
  }
  ```

### `GET /research/sessions`
Lists user's active and archived research sessions.
* **Response (200 OK):** Array of `ResearchSessionResponse` objects.

### `GET /research/sessions/{session_id}`
Retrieves full conversational message history with attached citations.
* **Response (200 OK):** `ResearchSessionDetailResponse` schema.

---

## 6. Econometric Performance Forecasting

### `GET /companies/{company_id}/forecasts`
Retrieves stored multi-scenario projections and historical validation metrics.
* **Query Parameters:** `metric_name` (string, default: `revenue`).
* **Response (200 OK):**
  ```json
  {
    "company_id": "b6363cc5-d4fe-44c6-805c-254917dd1a2a",
    "metric_name": "revenue",
    "scenarios": {
      "base": [{ "period": "FY25", "value": 1105000.0, "lower_bound": 1050000.0, "upper_bound": 1160000.0 }],
      "bull": [{ "period": "FY25", "value": 1270000.0, "lower_bound": 1210000.0, "upper_bound": 1330000.0 }],
      "bear": [{ "period": "FY25", "value": 939000.0, "lower_bound": 890000.0, "upper_bound": 988000.0 }]
    },
    "validation": { "mae": 1420.5, "rmse": 1890.2, "mape": 2.45, "directional_accuracy": 85.0 },
    "disclaimer": "Statistical forecasts are quantitative estimates based on historical filings..."
  }
  ```

### `POST /companies/{company_id}/forecasts/generate`
Re-runs time-series model estimation and walk-forward cross-validation.
* **Request Body:**
  ```json
  {
    "metric_name": "revenue",
    "forecast_horizon_years": 3
  }
  ```
* **Response (200 OK):** Freshly computed forecast scenario data.

---

## 7. News & Corporate Events

### `GET /news`
Fetches categorized news stream with company, category, and sentiment filters.
* **Query Parameters:** `company_id` (UUID), `category` (string), `sentiment` (string).
* **Response (200 OK):** Array of `NewsArticleResponse` objects.

### `POST /news/sync`
Triggers synchronization from Marketaux API or seed market announcement fixtures.
* **Response (200 OK):** `{"status": "Synced", "new_articles": 5}`.

### `GET /news/{article_id}`
Retrieves full article text, financial impact analysis, and matched company tags.
* **Response (200 OK):** `NewsArticleResponse` schema.

### `GET /corporate-actions`
Lists dividends, stock splits, bonus issues, and rights offerings.
* **Query Parameters:** `company_id` (UUID), `action_type` (string).
* **Response (200 OK):** Array of `CorporateActionResponse` objects.

### `GET /corporate-actions/companies/{company_id}/corporate-actions`
Retrieves corporate actions specific to a company.
* **Response (200 OK):** Array of `CorporateActionResponse` objects.

### `GET /market-events`
Lists material commercial announcements, large contract wins, and acquisitions.
* **Query Parameters:** `company_id` (UUID), `event_type` (string).
* **Response (200 OK):** Array of `MarketEventResponse` objects.

### `GET /market-events/companies/{company_id}/market-events`
Retrieves market deals specific to a company.
* **Response (200 OK):** Array of `MarketEventResponse` objects.

---

## 8. Analyst Watchlist

### `GET /watchlist`
Lists user's tracked equities, target prices, and analyst investment notes.
* **Response (200 OK):** Array of `WatchlistItemResponse` objects.

### `POST /watchlist`
Adds an equity to the watchlist.
* **Request Body:**
  ```json
  {
    "company_id": "b6363cc5-d4fe-44c6-805c-254917dd1a2a",
    "target_price": 3200.00,
    "notes": "Target based on FY26 EBITDA expansion in retail and telecom."
  }
  ```
* **Response (201 Created):** `WatchlistItemResponse`.

### `DELETE /watchlist/{company_id}`
Removes equity from analyst watchlist.
* **Response (200 OK):** `{"status": "Removed", "company_id": "..."}`.

