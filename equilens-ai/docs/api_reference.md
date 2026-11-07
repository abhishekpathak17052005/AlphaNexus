# EquiLens AI – REST API Reference (`/api/v1`)

Base URL: `http://localhost:8000/api/v1`

---

## 1. Health & Central Engine Registry

### `GET /health`
Returns high-level application health and database connection status.

**Response:**
```json
{
  "status": "Healthy",
  "environment": "development",
  "data_mode": "demo",
  "database_connected": true,
  "version": "1.0.0"
}
```

### `GET /health/engines`
Returns dynamic health status for all 11 core engines and third-party adapters.

---

## 2. Companies & Equities

### `GET /companies`
Query listed companies with optional filters (`exchange=NSE`, `sector=Information Technology`, `search=TCS`).

### `GET /companies/search?q={query}`
High-speed symbol and name autocompletion.

### `GET /companies/{company_id_or_symbol}`
Retrieves detailed company profile, valuation multiples, and historical stats.

---

## 3. Document Intelligence & Vector Ingestion

### `POST /documents/upload`
Uploads filing (PDF, DOCX, XLSX, CSV).
- `company_id` (UUID)
- `title` (String)
- `financial_year` (String: FY24, FY25)
- `document_type` (Annual Report, Earnings Call, etc.)
- `file` (Multipart file)
- `auto_process` (Boolean)

### `GET /documents`
Lists uploaded documents with processing status (`PROCESSED`, `PROCESSING`, `QUEUED`, `FAILED`).

### `POST /documents/{document_id}/process`
Triggers text/table extraction, section chunking, and vector embedding calculation.

### `DELETE /documents/{document_id}`
Deletes document record and associated pgvector chunks.

---

## 4. AI Research & RAG Chat

### `POST /research/chat`
Evidence-grounded conversational equity research query.

**Request:**
```json
{
  "company_id": "b6363cc5-d4fe-44c6-805c-254917dd1a2a",
  "query": "What are the consolidated revenues and EBITDA for Reliance in FY24?",
  "top_k": 5
}
```

**Response:**
```json
{
  "id": "e0b57fa2-16ad-45c1-84fe-fc60ea4eaee6",
  "role": "assistant",
  "content": "Consolidated Revenue for FY24 crossed the milestone of ₹10,00,122 Crore...",
  "message_type": "fact_grounded",
  "tokens_used": 142,
  "citations": [
    {
      "document_title": "Reliance Industries Integrated Annual Report FY24",
      "page_number": 42,
      "section": "Financial Highlights & EBITDA",
      "excerpt": "Consolidated Revenue for FY24 crossed the milestone of ₹10,00,122 Crore...",
      "confidence_score": 0.985
    }
  ]
}
```

---

## 5. News & Announcements

### `GET /news`
Fetches categorized news stream with `category`, `sentiment`, and `company_id` filters.

### `POST /news/sync`
Triggers synchronization from Marketaux API or seed announcement fixtures.

---

## 6. Financial Analytics & Peer Benchmarking

### `GET /companies/{company_id}/financials`
Returns historical annual/quarterly financial statements and line items.

### `GET /companies/{company_id}/ratios`
Returns deterministic ratios (ROE, ROCE, D/E, FCF, Margins).

### `POST /companies/compare`
Calculates peer comparison matrix across 2 to 5 companies with sector medians.

---

## 7. Performance Forecasting

### `GET /companies/{company_id}/forecasts?metric_name=revenue`
Returns Bull, Base, and Bear scenarios with 80% & 95% confidence intervals and walk-forward validation.

### `POST /companies/{company_id}/forecasts/generate`
Re-runs statistical time-series model estimation.

---

## 8. Watchlist

### `GET /watchlist`
Lists user's tracked equities.

### `POST /watchlist`
Adds equity with target price and analyst thesis.

### `DELETE /watchlist/{company_id}`
Removes equity from watchlist.

