# EquiLens AI – System Workflows & Sequence Specifications

This document outlines the end-to-end execution workflows of EquiLens AI. Each workflow details the interaction between the frontend client, backend application server, core intelligence engines, database tier, and external provider APIs.

---

## 1. User Authentication & Session Lifecycle

### Workflow Description
EquiLens AI supports analyst authentication via Supabase Auth and local JWT token issuance. Upon logging in, access tokens are securely managed, and session contexts are injected into subsequent API queries.

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as Analyst / User
    participant Web as Frontend Client (React)
    participant Auth as Auth Middleware (FastAPI)
    participant DB as PostgreSQL (Supabase)
    
    Analyst->>Web: Enter Credentials (Email / Password)
    Web->>Auth: POST /api/v1/auth/token (OAuth2 form)
    Auth->>DB: Query User by Email
    DB-->>Auth: Return User Record (Hashed Password, Role)
    Auth->>Auth: Verify PBKDF2/Bcrypt Hash
    alt Invalid Credentials
        Auth-->>Web: HTTP 401 Unauthorized
        Web-->>Analyst: Show Error Notification
    else Valid Credentials
        Auth->>Auth: Generate JWT Access Token (HS256)
        Auth-->>Web: Return {access_token, token_type, expires_in}
        Web->>Web: Store in Memory / Secure Session Storage
        Web-->>Analyst: Redirect to Overview Dashboard
    end
```

---

## 2. Company Search & Symbol Autocompletion

### Workflow Description
Fast symbol and corporate name resolution across Indian equity markets (NSE and BSE).

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as Analyst
    participant Web as Global Search Modal / Search Input
    participant API as Backend (/api/v1/companies/search)
    participant DB as PostgreSQL (companies table)

    Analyst->>Web: Types query string (e.g. "REL" or "Tata")
    Web->>Web: Debounce keystrokes (250ms)
    Web->>API: GET /api/v1/companies/search?q={query}
    API->>DB: SELECT * FROM companies WHERE symbol ILIKE query OR name ILIKE query LIMIT 10
    DB-->>API: Return matching company records
    API-->>Web: Return JSON array of Company summaries
    Web-->>Analyst: Render dropdown list with Symbol, Sector, Market Cap & Live Price
```

---

## 3. Company Overview & Financial Profile Retrieval

### Workflow Description
Aggregates fundamental accounting metrics, valuation multiples, historical stock prices, and corporate profiles into a unified company dashboard.

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as Analyst
    participant Web as CompanyDetailPage
    participant API as Backend (/api/v1/companies/{id})
    participant DB as PostgreSQL Database
    participant Dhan as DhanHQ Provider / Market Fixtures

    Analyst->>Web: Navigate to /company/{symbol}
    Web->>API: GET /api/v1/companies/{symbol}
    API->>DB: Fetch Company Profile & Master Identifiers
    DB-->>API: Company Record
    Web->>API: GET /api/v1/companies/{id}/financials?period_type=annual
    API->>DB: Fetch Financial Statements & Line Items
    DB-->>API: P&L, Balance Sheet, Cash Flow rows
    Web->>API: GET /api/v1/companies/{id}/ratios
    API->>API: Compute DuPont ROE, ROCE, FCF, Margins via FinancialCalculator
    Web->>API: GET /api/v1/companies/{id}/stock-prices
    API->>Dhan: Fetch Daily OHLCV / Moving Averages
    Dhan-->>API: OHLCV time series
    API-->>Web: Consolidated Profile, Financials, Ratios & Price History
    Web-->>Analyst: Render Interactive Charts & Financial Summary
```

---

## 4. Financial Document Upload & File Validation

### Workflow Description
Multi-format file upload supporting Annual Reports, Quarterly Filings, Earnings Transcripts, and Presentation Decks in PDF, DOCX, XLSX, and CSV formats.

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as Analyst
    participant Web as DocumentIntelligencePage
    participant API as Backend (/api/v1/documents/upload)
    participant Prep as DocumentPreprocessor
    participant Storage as File Storage (Supabase / Local)
    participant DB as PostgreSQL Database

    Analyst->>Web: Select File & Company (Drag & Drop)
    Web->>API: POST /api/v1/documents/upload (Multipart/form-data)
    API->>API: Validate MIME Type, Extension & File Size (< 50MB)
    API->>Prep: Compute SHA-256 Hash of File Stream
    Prep-->>API: File Checksum
    API->>DB: Check for duplicate file_hash under company_id
    alt Duplicate Detected
        API-->>Web: HTTP 409 Conflict (Document already ingested)
    else New Document
        API->>Storage: Persist raw document stream to storage
        Storage-->>API: File Storage Path / URI
        API->>DB: INSERT INTO documents (status='UPLOADED', file_hash, metadata)
        DB-->>API: Document ID
        API-->>Web: HTTP 201 Created {document_id, status: 'UPLOADED'}
        Web-->>Analyst: Show Progress Card in Ingestion Table
    end
```

---

## 5. Document Extraction, Cleaning & Section Classification

### Workflow Description
Multi-modal extraction pipeline parsing textual hierarchies and tabular financial statements.

```mermaid
sequenceDiagram
    autonumber
    participant Task as Ingestion Task / API
    participant Loader as Multi-Modal Loader (PDF/DOCX/Tabular)
    participant Prep as DocumentPreprocessor
    participant DB as PostgreSQL Database

    Task->>Loader: Read raw file from storage by Document ID
    alt File is PDF
        Loader->>Loader: pdfplumber extracts layout, page text & bounding boxes
        Loader->>Loader: Extract table grids using structural line detectors
    else File is DOCX
        Loader->>Loader: python-docx parses headings, bold metadata & paragraphs
    else File is XLSX/CSV
        Loader->>Loader: openpyxl / pandas extracts sheets into DataFrames
    end
    Loader-->>Task: Extracted Page Data [{page_number, text, tables}]
    Task->>Prep: normalize_text() (Whitespace, encoding, non-breaking spaces)
    Task->>Prep: filter_empty_pages() (Pages with < 20 chars & no tables)
    Task->>Prep: infer_document_type() (Annual Report, Quarterly Result, etc.)
    Task->>DB: UPDATE documents SET total_pages=N, status='EXTRACTED', document_type=type
```

---

## 6. Financial-Aware Chunking & Embedding Generation

### Workflow Description
Sections documents into semantically coherent passages while preserving financial tables as unbroken Markdown blocks and computing 384-dimensional dense vectors.

```mermaid
sequenceDiagram
    autonumber
    participant Ingest as Ingestion Pipeline
    participant Chunker as DocumentChunker
    participant Embed as EmbeddingEngine (BAAI/bge-small-en-v1.5)
    participant DB as PostgreSQL + pgvector (document_chunks)

    Ingest->>Chunker: chunk_document(pages_data, company_id, doc_id)
    loop For each page & section
        Chunker->>Chunker: Isolate Financial Tables -> Format as Markdown
        Chunker->>Chunker: Slide text window (chunk_size=900, overlap=120)
        Chunker->>Chunker: Inject metadata prefix [Company | FY | Type | Section | Page]
    end
    Chunker-->>Ingest: List of Chunks (Content, Clean Text, Page, Section, Table Flag)
    Ingest->>Embed: generate_embeddings_batch([chunk.clean_text])
    Embed->>Embed: PyTorch inference on SentenceTransformer
    Embed->>Embed: L2 Unit Normalization (||v|| = 1.0)
    Embed-->>Ingest: Array of 384-dimensional dense float vectors
    Ingest->>DB: Batch INSERT INTO document_chunks (embedding, metadata_json)
    DB-->>Ingest: Confirm Chunks Stored
    Ingest->>DB: UPDATE documents SET status='PROCESSED', total_chunks=len(chunks)
```

---

## 7. Vector Retrieval & Semantic Similarity Search

### Workflow Description
Cosine distance search against `document_chunks` using PostgreSQL `pgvector`.

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as Analyst
    participant Web as AIResearchPage
    participant API as Backend (/api/v1/research/chat)
    participant Embed as EmbeddingEngine
    participant DB as pgvector (<=> operator)

    Analyst->>Web: Enter query (e.g., "What was Reliance Retail revenue in FY24?")
    Web->>API: POST /api/v1/research/chat {company_id, query, top_k=5}
    API->>Embed: generate_query_embedding(query)
    Embed-->>API: Normalized Query Vector [384]
    API->>DB: SELECT *, (embedding <=> query_vector) AS cosine_distance<br/>FROM document_chunks<br/>WHERE company_id = {company_id}<br/>ORDER BY cosine_distance ASC LIMIT 5
    DB-->>API: Top-5 Most Relevant Chunks with Metadata
    Note over API: Filter chunks where distance < threshold (0.65)
```

---

## 8. AI Question Answering & Citation Synthesis

### Workflow Description
Orchestrates retrieved evidence into a structured system prompt, invokes Google Gemini (or Groq), and constructs verifiable page-level citations.

```mermaid
sequenceDiagram
    autonumber
    participant API as RAG Service Orchestrator
    participant Prompt as Prompt & Context Assembler
    participant LLM as Google Gemini (gemini-3.5-flash) / Groq
    participant Citations as CitationEngine
    participant DB as PostgreSQL Database
    actor Analyst as Analyst

    API->>Prompt: Build Context Block with [Doc Title | Page # | Section | Excerpt]
    Prompt->>LLM: Dispatch System Prompt + Grounded Evidence + Query
    LLM-->>API: Generated Synthesis & Findings
    API->>Citations: build_citations_from_retrieval(retrieved_chunks, message_id)
    Citations-->>API: List of Citation Objects {document_id, page_number, excerpt, confidence}
    API->>DB: INSERT INTO research_messages (content, message_type='fact_grounded')
    API->>DB: Batch INSERT INTO citations (message_id, document_id, page_number, excerpt)
    API-->>Analyst: Stream or Return JSON response with interactive clickable citations
```

---

## 9. Deterministic Financial Analysis Workflow

### Workflow Description
Computes standard equity research ratios with strict zero-division prevention.

```mermaid
flowchart TD
    Start["Request Financial Ratios (/api/v1/companies/{id}/ratios)"] --> FetchDB["Query financial_metrics for historical P&L & Balance Sheet"]
    FetchDB --> Clean["Sanitize Inputs: Handle NaN, Zero & Missing Periods"]
    
    Clean --> CalcGrowth["Calculate Revenue YoY: ((Rev_t - Rev_{t-1}) / |Rev_{t-1}|) * 100"]
    Clean --> CalcMargin["Calculate EBITDA & PAT Margins: (Metric / Revenue) * 100"]
    Clean --> CalcDuPont["DuPont ROE: (Net Profit / Equity) * 100"]
    Clean --> CalcROCE["ROCE: (EBIT / (Total Assets - Current Liabilities)) * 100"]
    Clean --> CalcSolvency["Solvency: Debt-to-Equity & Current Ratio"]
    Clean --> CalcFCF["Free Cash Flow: Operating Cash Flow - |CapEx|"]

    CalcGrowth --> Assemble["Assemble Deterministic Output Payload"]
    CalcMargin --> Assemble
    CalcDuPont --> Assemble
    CalcROCE --> Assemble
    CalcSolvency --> Assemble
    CalcFCF --> Assemble

    Assemble --> Return["Return JSON to Frontend (Zero Hallucination Guaranteed)"]
```

---

## 10. Performance Forecasting & Econometric Scenario Generation

### Workflow Description
Executes walk-forward cross-validation, models baseline trends, and projects Bull, Base, and Bear scenarios with 80% and 95% parametric confidence intervals.

```mermaid
flowchart TD
    Req["POST /api/v1/companies/{id}/forecasts/generate"] --> DataCheck["Check Historical Data Adequacy (>= 3 periods required)"]
    DataCheck -->|Adequate| Split["Chronological Train/Test Split (Walk-Forward)"]
    DataCheck -->|Insufficient| Fallback["Generate Scenarios based on Sector Medians & Heuristics"]

    Split --> Fit["Fit Baseline Model: AR(p) + Linear OLS Trend"]
    Fit --> OutOfSample["Compute Out-of-Sample Validation: MAE, RMSE, MAPE, Directional Accuracy"]
    
    Fit --> Project["Project Horizon (1 to 5 years into Future)"]
    Project --> Base["Base Case: Predicted Econometric Trajectory"]
    Project --> Bull["Bull Case: +15% to +20% Expansion Band"]
    Project --> Bear["Bear Case: -15% Contraction Band"]

    Base --> ConfBounds["Compute 80% (z=1.28) and 95% (z=1.96) Parametric Intervals"]
    Bull --> ConfBounds
    Bear --> ConfBounds

    ConfBounds --> Store["Store Forecast & ForecastEvaluation records in PostgreSQL"]
    Store --> Disclaimer["Attach Mandatory Regulatory Compliance Disclaimer"]
    Disclaimer --> ReturnUI["Render ForecastScenarioChart in React UI"]
```

---

## 11. News Retrieval, Entity Matching & Tone Sentiment Analysis

### Workflow Description
Pulls live market news, classifies events, calculates sentiment tone, and prevents ticker collisions.

```mermaid
sequenceDiagram
    autonumber
    actor Cron as Background Scheduler / Sync Trigger
    participant API as News Service (/api/v1/news/sync)
    participant Mkt as Marketaux API
    participant Entity as NewsEntityMatcher (Regex word boundaries)
    participant Classify as NewsEventClassifier
    participant Tone as NewsSentimentAnalyzer
    participant DB as PostgreSQL (news_articles)

    Cron->>API: Trigger News Synchronization
    API->>Mkt: GET /v1/news/all?countries=in&filter_entities=true
    Mkt-->>API: Raw Articles JSON
    loop For each article
        API->>Entity: match_companies(article_title, article_description)
        Note over Entity: Validates symbol boundaries (e.g. avoids matching 'IT' or 'A')
        Entity-->>API: Matched Company IDs
        API->>Classify: classify_event(text) -> Earnings / Contracts / M&A / Regulatory / Dividends
        API->>Tone: compute_sentiment(text) -> Score [-1.0, 1.0] & Label (Bullish/Bearish/Neutral)
        API->>DB: INSERT INTO news_articles ON CONFLICT (url) DO NOTHING
    end
    API-->>Cron: Sync Complete {new_articles_count}
```

---

## 12. Corporate Actions & Market Event Tracking

### Workflow Description
Monitors dividends, stock splits, bonus shares, rights issues, and major contracts/deals.

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as Analyst
    participant Web as CorporateActionsPage / MarketEventsPage
    participant API as Backend Router
    participant DB as PostgreSQL (corporate_actions / market_events)

    Analyst->>Web: Open Corporate Actions / Market Events Tab
    Web->>API: GET /api/v1/corporate-actions?company_id={id}
    API->>DB: Query corporate_actions ordered by announcement_date DESC
    DB-->>API: Return Dividend, Split & Bonus events
    Web->>API: GET /api/v1/market-events?company_id={id}
    API->>DB: Query market_events (Deal value, Counterparty, Strategic implications)
    DB-->>API: Return M&A, large contract wins & strategic partnerships
    API-->>Web: Formatted event timelines
    Web-->>Analyst: Display interactive chronological timeline cards with impact badges
```

---

## 13. Peer Comparison & Sector Benchmarking

### Workflow Description
Compares 2 to 5 companies across valuation multiples, growth rates, and margins.

```mermaid
flowchart TD
    UI["Analyst selects 2 to 5 Peer Companies in UI"] --> Req["POST /api/v1/companies/compare {company_ids: [...]}"]
    Req --> DBQuery["Query companies, financial_metrics, and ratios for all targets"]
    DBQuery --> Matrix["Build Comparative Matrix (P/E, P/B, ROE, ROCE, Growth, Debt)"]
    Matrix --> Medians["Compute Sector Medians & Rank Order"]
    Medians --> Strengths["Identify Outliers: Leader in Margin, Lowest Debt, Best Valuation"]
    Strengths --> Response["Return Peer Matrix JSON"]
    Response --> Render["Render Comparative Bar Chart & Matrix in PeerComparisonPage"]
```

---

## 14. Stock Price History & Technical Indicator Generation

### Workflow Description
Retrieves daily candlestick OHLCV and derives 50-day & 200-day Simple Moving Averages.

```mermaid
sequenceDiagram
    autonumber
    participant Web as MarketChart Component (Lightweight Charts / Recharts)
    participant API as Backend (/api/v1/companies/{id}/stock-prices)
    participant Dhan as DhanHQ Provider / Historical Fixtures
    participant DB as PostgreSQL (stock_prices)

    Web->>API: GET /api/v1/companies/{id}/stock-prices?range=1Y
    API->>DB: Check cached daily OHLCV records
    alt Cache Valid
        DB-->>API: Daily candles
    else Cache Miss / Live Query
        API->>Dhan: Fetch historical daily candles (Open, High, Low, Close, Volume)
        Dhan-->>API: Raw OHLCV records
        API->>DB: Cache records in stock_prices table
    end
    API->>API: Calculate SMA(50), SMA(200), and Day Change Percent
    API-->>Web: Candlestick array + Moving Average overlays
    Web-->>Web: Render High-Resolution Price & Volume Chart
```

---

## 15. Research Report Synthesis Workflow

### Workflow Description
Generates a comprehensive multi-page institutional equity research brief combining qualitative filing excerpts with quantitative ratios and forecasting scenario bands.

```mermaid
flowchart TD
    User["Analyst clicks 'Generate Research Report' for Company"] --> Trigger["POST /api/v1/reports/generate"]
    
    Trigger --> Step1["Step 1: Pull Company Profile, Identifiers & Key Multiples"]
    Trigger --> Step2["Step 2: Fetch Last 3 Years Audited Financials & Compute Ratios"]
    Trigger --> Step3["Step 3: Retrieve Top RAG Chunks from latest Annual Report (MD&A, Risks)"]
    Trigger --> Step4["Step 4: Execute Econometric Forecast (Base, Bull, Bear Scenarios)"]
    Trigger --> Step5["Step 5: Fetch Recent Material News, Deals & Corporate Actions"]

    Step1 --> Synth["Orchestration Engine: Assemble Grounded Research Context"]
    Step2 --> Synth
    Step3 --> Synth
    Step4 --> Synth
    Step5 --> Synth

    Synth --> LLMPrompt["Format Strict Financial Synthesis Prompt"]
    LLMPrompt --> Gemini["Google Gemini 3.5 Flash Inference"]
    Gemini --> ReportDoc["Generate Structured Report Sections:
    - Executive Summary
    - Financial Highlights & Growth
    - Management Commentary & Strategy
    - Key Risks & Governance
    - Multi-Scenario Valuation Outlook
    - Source Citations & Disclaimers"]
    
    ReportDoc --> StoreDB["Store Report in research_reports table"]
    StoreDB --> ClientUI["Display Report in ResearchReportsPage with Export Options"]
```

