# EquiLens AI – Complete Application Feature Catalog

This document details every user-facing and backend functional feature in EquiLens AI, organized by functional module. For every feature, the purpose, operational logic, input requirements, output data, and current implementation status are documented.

---

## 1. Overview Dashboard

### 1.1 Market Health & System Vitality Banner
* **Purpose:** Provides instantaneous visibility into the health of all 11 underlying intelligence engines, active database connections, and market data mode.
* **How It Works:** Queries `/api/v1/health` and `/api/v1/health/engines` on component mount, displaying color-coded status badges (`Ready`, `Degraded`, `Disabled`, `Failed`).
* **Input Data:** System telemetry and engine registry state.
* **Processing Logic:** Evaluates aggregate health enum. If any engine is degraded, surfaces actionable explanation without blocking UI.
* **Output:** Status badges, active engine count, database connection state.
* **Status:** **Implemented** (Rendered in `OverviewPage.tsx`).

### 1.2 Top Market Movers & Featured Equities
* **Purpose:** Surfaces high-liquidity Indian equities (Reliance, TCS, HDFC Bank, Infosys, L&T) with live market metrics.
* **How It Works:** Fetches companies list with valuation multiples and day-change metrics from `/api/v1/companies`.
* **Input Data:** Database records seeded from NSE/BSE master data.
* **Processing Logic:** Sorts equities by market capitalization and daily percentage price movement.
* **Output:** Interactive company cards with price, daily percent change, P/E ratio, and quick navigation links.
* **Status:** **Implemented** (Rendered in `OverviewPage.tsx`).

---

## 2. Company Overview & Detail Hub

### 2.1 Corporate Identity & Valuation Summary
* **Purpose:** Displays complete institutional profile of a listed company.
* **How It Works:** Resolves company by symbol or UUID via `/api/v1/companies/{id}`.
* **Input Data:** ISIN, Sector, Industry, Exchange, Market Cap, 52-Week Range, P/E, P/B, Dividend Yield.
* **Processing Logic:** Formats figures in Indian numbering (INR Crores, Lakhs) and calculates valuation spreads.
* **Output:** Profile header with verified exchange tags, industry classification, and live pricing.
* **Status:** **Implemented** (Rendered in `CompanyDetailPage.tsx`).

### 2.2 Historical Candlestick & Volume Chart
* **Purpose:** Visualizes stock price trends over 1M, 6M, 1Y, and 5Y horizons.
* **How It Works:** Queries `/api/v1/companies/{id}/stock-prices` with timeframe filters.
* **Input Data:** Daily OHLCV records.
* **Processing Logic:** Calculates 50-day and 200-day Simple Moving Averages (SMA).
* **Output:** High-resolution interactive chart rendered via Recharts.
* **Status:** **Implemented** (Rendered in `CompanyDetailPage.tsx` via `MarketChart.tsx`).

---

## 3. Financial Statements & Fundamental Analysis

### 3.1 Three-Statement Accounting Explorer
* **Purpose:** Allows granular review of audited Balance Sheet, Profit & Loss (Income Statement), and Cash Flow statements.
* **How It Works:** Fetches structured statement line items via `/api/v1/companies/{id}/financials` and `/statements`.
* **Input Data:** Audited annual and quarterly financial filings.
* **Processing Logic:** Organizes line items chronologically (FY22, FY23, FY24) and distinguishes standalone from consolidated accounts.
* **Output:** Expandable multi-year accounting tables with unit indicators (INR Crores).
* **Status:** **Implemented** (Rendered in `CompanyDetailPage.tsx`).

### 3.2 Deterministic Financial Ratio Analysis
* **Purpose:** Delivers mathematically guaranteed financial ratios without LLM hallucination.
* **How It Works:** Executes `FinancialCalculator` algorithms on demand via `/api/v1/companies/{id}/ratios`.
* **Input Data:** Revenue, EBITDA, PAT, Net Worth, Total Debt, Operating Cash Flow, CapEx.
* **Processing Logic:** Computes YoY Revenue Growth, EBITDA Margin, Net Profit Margin, DuPont ROE, ROCE, Free Cash Flow, Debt-to-Equity, and Current Ratio with zero-denominator safeguards.
* **Output:** Clean financial metrics grid with percentage tags and trend indicators.
* **Status:** **Implemented** (Rendered in `CompanyDetailPage.tsx`).

---

## 4. AI Document Intelligence & Ingestion Hub

### 4.1 Multi-Format Document Ingestion
* **Purpose:** Enables analysts to upload regulatory filings (Annual Reports, Quarterly Filings, Earnings Transcripts, Presentations) in PDF, DOCX, XLSX, and CSV formats.
* **How It Works:** Uploads via `POST /api/v1/documents/upload` as multipart/form-data.
* **Input Data:** Binary document stream, company UUID, financial year, and document type.
* **Processing Logic:** Validates file size (<50MB), verifies MIME type, computes SHA-256 checksum to prevent duplicate processing, and persists raw bytes to storage.
* **Output:** Document record in `documents` table with status `UPLOADED`.
* **Status:** **Implemented** (Rendered in `DocumentIntelligencePage.tsx`).

### 4.2 Document Processing & Vector Indexing Pipeline
* **Purpose:** Extracts text, isolates tables, sections text, and generates 384-d dense embeddings.
* **How It Works:** Invoked automatically or via `POST /api/v1/documents/{id}/process`.
* **Input Data:** Stored document bytes.
* **Processing Logic:** Runs `pdfplumber`/`docx` extraction -> `DocumentPreprocessor` sanitization -> `DocumentChunker` table-preserving chunking -> `EmbeddingEngine` vectorization -> `pgvector` persistence.
* **Output:** Stored `document_chunks` records and status updated to `PROCESSED`.
* **Status:** **Implemented** (Rendered in `DocumentIntelligencePage.tsx`).

---

## 5. AI Research Terminal & Conversational RAG

### 5.1 Evidence-Grounded Equity Research Chat
* **Purpose:** Provides interactive Q&A grounded exclusively in verified filings.
* **How It Works:** Submits query via `POST /api/v1/research/chat`.
* **Input Data:** User question, company UUID, optional financial year, and `top_k`.
* **Processing Logic:** Embeds query -> queries `pgvector` for cosine-distance top chunks -> formats context with document title and page numbers -> executes Google Gemini / Groq inference.
* **Output:** Synthesis response accompanied by a verified array of clickable citations.
* **Status:** **Implemented** (Rendered in `AIResearchPage.tsx`).

### 5.2 Interactive Source Citations
* **Purpose:** Guarantees transparency by providing exact document references for every statement.
* **How It Works:** Extracts source excerpts, page numbers, and confidence scores from retrieved chunks.
* **Input Data:** `Citation` model linked to `ResearchMessage`.
* **Processing Logic:** Matches generated claims to source text bounding blocks.
* **Output:** Clickable citation pills in chat UI displaying document title, page number, section, and excerpt.
* **Status:** **Implemented** (Rendered in `AIResearchPage.tsx`).

---

## 6. Econometric Performance Forecasting

### 6.1 Multi-Scenario Financial Projections
* **Purpose:** Projects 1 to 5-year trajectories for Revenue, Net Profit, EBITDA, and EPS.
* **How It Works:** Calls `POST /api/v1/companies/{id}/forecasts/generate`.
* **Input Data:** Historical annual metrics (minimum 3 periods).
* **Processing Logic:** Fits autoregressive $AR(p)$ + linear trend -> performs walk-forward validation -> calculates Base Case, Bullish (+15-20%), and Bearish (-15%) scenarios -> computes 80% and 95% parametric confidence bounds.
* **Output:** Multi-scenario projection curves rendered via `ForecastScenarioChart.tsx`.
* **Status:** **Implemented** (Rendered in `ForecastsPage.tsx`).

### 6.2 Walk-Forward Cross-Validation Metrics
* **Purpose:** Exposes out-of-sample error statistics to verify forecast reliability.
* **How It Works:** Evaluates MAE, RMSE, MAPE, and Directional Accuracy.
* **Input Data:** Out-of-sample historical test splits.
* **Processing Logic:** Compares predicted test periods against actual reported filings.
* **Output:** Error metric cards displaying historical accuracy percentages.
* **Status:** **Implemented** (Rendered in `ForecastsPage.tsx`).

---

## 7. News Intelligence & Market Deals

### 7.1 Real-Time Financial News Stream
* **Purpose:** Monitors continuous stream of market disclosures and financial journalism.
* **How It Works:** Fetches filtered news stream from `/api/v1/news`.
* **Input Data:** Marketaux API feed or verified market fixtures.
* **Processing Logic:** Deduplicates by URL hash -> regex matches Indian company symbols -> assigns sentiment scores and categories.
* **Output:** Categorized article cards with publication date, source publication, and sentiment badge.
* **Status:** **Implemented** (Rendered in `NewsIntelligencePage.tsx`).

### 7.2 Corporate Actions Tracker
* **Purpose:** Tracks Dividends, Stock Splits, Bonus Issues, and Buybacks.
* **How It Works:** Queries `/api/v1/corporate-actions`.
* **Input Data:** Regulatory announcements with Ex-Dates and Record-Dates.
* **Processing Logic:** Classifies action type, computes dividend yield impact, and tracks status.
* **Output:** Timeline list of corporate actions with status badges (`Announced`, `Effective`).
* **Status:** **Implemented** (Rendered in `CorporateActionsPage.tsx`).

### 7.3 Market Events & Major Deals Intelligence
* **Purpose:** Captures large commercial contract wins, acquisitions, and strategic partnerships.
* **How It Works:** Queries `/api/v1/market-events`.
* **Input Data:** Material disclosures filed with stock exchanges.
* **Processing Logic:** Extracts deal value in INR Crores, counterparty name, and strategic implications.
* **Output:** Deal cards detailing financial size, counterparties, and strategic summary.
* **Status:** **Implemented** (Rendered in `MarketEventsPage.tsx`).

---

## 8. Peer Comparison & Sector Benchmarking

### 8.1 Multi-Company Peer Matrix
* **Purpose:** Directly compares 2 to 5 companies across key valuation, profitability, and solvency metrics.
* **How It Works:** Submits target company UUIDs to `POST /api/v1/companies/compare`.
* **Input Data:** Company profiles, financial metrics, and calculated ratios.
* **Processing Logic:** Aligns metrics side-by-side, computes sector medians, and flags category leaders.
* **Output:** Comparative data table and multi-bar visualization.
* **Status:** **Implemented** (Rendered in `PeerComparisonPage.tsx`).

---

## 9. Watchlist & Equity Tracking

### 9.1 Analyst Watchlist & Notes
* **Purpose:** Allows analysts to track equities of interest with custom price targets and notes.
* **How It Works:** CRUD operations against `/api/v1/watchlist`.
* **Input Data:** User ID, Company ID, target price, and investment thesis notes.
* **Processing Logic:** Associates company records with user profile; enforces unique constraints.
* **Output:** Interactive watchlist table with distance-to-target calculations.
* **Status:** **Implemented** (Rendered in `WatchlistPage.tsx`).

---

## 10. Research Report Generator

### 10.1 Structured Equity Research Brief
* **Purpose:** Generates comprehensive multi-section equity research reports combining quantitative fundamentals with qualitative filing excerpts.
* **How It Works:** Invokes report generation service combining financial statements, RAG excerpts, and forecasting scenarios.
* **Input Data:** Audited financials, latest annual report chunks, forecast outputs, recent news.
* **Processing Logic:** Assembles grounded research brief -> prompts Gemini 3.5 Flash with structured section templates -> formats findings into Executive Summary, Financials, Risks, and Outlook.
* **Output:** Multi-section research brief with export and printing options.
* **Status:** **Implemented** (Rendered in `ResearchReportsPage.tsx`).

---

## 11. System Settings & API Connectivity Audit

### 11.1 Real-Time External API Audit Dashboard
* **Purpose:** Live diagnostic dashboard probing all 9 external service integrations.
* **How It Works:** Invokes `GET /api/v1/health/integrations` on mount or manual refresh.
* **Input Data:** Live network probes against Gemini, Groq, PostgreSQL, pgvector, DhanHQ, Marketaux, FMP, Langfuse, and Sentry.
* **Processing Logic:** Probes endpoints concurrently, measures exact round-trip latencies, captures HTTP response codes, and diagnoses tier limitations without exposing raw credentials.
* **Output:** Institutional audit table displaying Status badges, Provider, Active Model, HTTP Status, Latency in milliseconds, and Diagnostic Information.
* **Status:** **Implemented** (Rendered in `SettingsPage.tsx`).

