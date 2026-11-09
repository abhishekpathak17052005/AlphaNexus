# EquiLens AI – Comprehensive System Architecture Specification

## 1. System Vision & Design Philosophy

EquiLens AI is an institutional-grade financial intelligence research terminal combining:
1. **Retrieval-Augmented Generation (RAG):** Document intelligence with verifiable page-level citations back to authentic corporate filings.
2. **Deterministic Financial Analytics:** Zero-tolerance mathematical computation for fundamental ratios (DuPont ROE, ROCE, FCF, Margins).
3. **Econometric Performance Forecasting:** Multi-period scenario bands (Bull, Base, Bear) backed by walk-forward cross-validation and parametric confidence intervals.
4. **News & Corporate Deals Intelligence:** Collision-safe entity matching, event classification, and sentiment tone scoring for Indian equities (NSE/BSE).
5. **Central Engine Registry:** Dynamic health introspection, graceful degradation, and provider failover.

---

## 2. High-Level System Architecture

```mermaid
graph TB
    subgraph Client["Client Tier (React 18 + TypeScript + Vite)"]
        UI_Shell["App Shell & Navigation"]
        State_Zustand["Zustand Global State (Company / Theme)"]
        Cache_Query["TanStack React Query (Server State Cache)"]
        Charts_Recharts["Recharts Visualization Engine"]
        API_Axios["Axios Interceptor Client (/api/v1)"]
    end

    subgraph Gateway["API & Application Gateway (FastAPI + Python 3.13)"]
        Router["FastAPI Central Router (/api/v1)"]
        CORS["CORS & Request Middleware"]
        Lifecycle["Lifespan Startup & Health Hooks"]
        Registry["Central Engine Registry (11 Core Engines)"]
    end

    subgraph Engines["Core Intelligence Engines"]
        RAG_Svc["RAG Document Ingestion & Retrieval"]
        Calc_Svc["Financial Analytics Calculator"]
        Fore_Svc["Econometric Forecasting Service"]
        News_Svc["News & Event Intelligence Service"]
        Audit_Svc["Live Integration Audit Service"]
    end

    subgraph Persistence["Persistence & Storage Tier"]
        DB_Postgres["PostgreSQL 17.11 (Supabase Hosted)"]
        DB_Vector["pgvector v0.8.2 Extension (Cosine Similarity)"]
        Obj_Storage["Supabase Private File Storage"]
    end

    subgraph Providers["External AI & Market Services"]
        LLM_Gemini["Google Gemini (gemini-3.5-flash)"]
        LLM_Groq["Groq Cloud (qwen/qwen3.8-27b)"]
        Mkt_Marketaux["Marketaux Financial News API"]
        Mkt_Dhan["DhanHQ Brokerage API"]
        Data_FMP["Financial Modeling Prep (FMP)"]
        Telemetry["Langfuse Cloud US (Tracing)"]
    end

    Client -->|HTTP REST / JSON| Gateway
    Gateway --> Engines
    Engines --> Persistence
    Engines --> Providers
    Gateway --> Telemetry
```

---

## 3. Frontend Architecture

### 3.1 Technology Stack & Directory Structure
* **Framework:** React 18.3 with TypeScript (strict type checking enabled).
* **Build System:** Vite 5.4 generating optimized production chunks in ~1.2s.
* **Styling:** Tailwind CSS 3.4 featuring a specialized financial dark palette (`slate-900`, `slate-950`, `blue-500`, `emerald-500`, `rose-500`, `amber-500`).
* **Routing:** `react-router-dom` v6 with layout nesting:
  * `/` -> `OverviewPage`
  * `/explore` -> `ExploreCompaniesPage`
  * `/company/:symbol` -> `CompanyDetailPage`
  * `/documents` -> `DocumentIntelligencePage`
  * `/research` -> `AIResearchPage`
  * `/forecasts` -> `ForecastsPage`
  * `/news` -> `NewsIntelligencePage`
  * `/corporate-actions` -> `CorporateActionsPage`
  * `/market-events` -> `MarketEventsPage`
  * `/compare` -> `PeerComparisonPage`
  * `/watchlist` -> `WatchlistPage`
  * `/reports` -> `ResearchReportsPage`
  * `/settings` -> `SettingsPage`

### 3.2 State Management & Data Fetching
* **Zustand Stores:**
  * `useCompanyStore`: Tracks the currently selected equity, symbol search string, active financial year, and document filters.
  * `useThemeStore`: Controls dark/light UI theme toggling.
* **TanStack React Query v5:**
  * Queries configured with `refetchOnWindowFocus: false` and `retry: 1` to optimize network traffic.
  * Cache invalidation triggered automatically upon document upload or forecast generation.
* **Axios API Client:** Centralized instance in `src/services/api.ts` with global response interceptors surfacing typed API error messages.

---

## 4. Backend Application Architecture

### 4.1 Dependency Injection & ASGI Runtime
* **FastAPI Lifespan Management:** Database schemas verified, initial market seed data populated, and engine registry initialized during application startup in `app/main.py`.
* **Database Session Dependency:** Scoped SQLAlchemy sessions yielded via `get_db()` with automated closure in `finally` blocks.
* **Modular Routing:** 10 endpoint controllers mounted cleanly under `app/api/v1/router.py`:
  * `health.py`: Application health, engine health, and live API integration audits.
  * `companies.py`: Company profiles, symbol search, valuation multiples.
  * `documents.py`: Document upload, status polling, processing triggers.
  * `research.py`: Grounded conversational RAG, session management.
  * `news.py`: Marketaux synchronization, news feeds, entity filtering.
  * `financials.py`: Three-statement financials, deterministic ratios, peer matrices.
  * `corporate_actions.py`: Dividends, stock splits, bonus issues.
  * `market_events.py`: Major commercial contracts and M&A tracking.
  * `forecasts.py`: Scenario generation, out-of-sample backtesting metrics.
  * `watchlist.py`: Analyst equity tracking and price target notes.

---

## 5. RAG & Document Intelligence Pipeline

```mermaid
flowchart TD
    DocUpload["Document Upload (PDF, DOCX, XLSX, CSV)"] --> FileCheck["Validation: MIME Check, File Size (<50MB)"]
    FileCheck --> HashDedupe["SHA-256 Checksum Deduplication"]
    HashDedupe --> RawStore["Store Raw Bytes in Supabase Storage"]
    RawStore --> DBRecord["Create Document Record (status='UPLOADED')"]
    
    DBRecord --> Extraction["Multi-Modal Extractor:
    - PDF: pdfplumber & pypdf
    - DOCX: python-docx
    - Tabular: pandas & openpyxl"]
    
    Extraction --> Cleaning["DocumentPreprocessor:
    - Whitespace & encoding sanitization
    - Empty page suppression (<20 chars)
    - Classification: Annual Report / 10-K / Transcripts"]
    
    Cleaning --> Chunking["DocumentChunker:
    - Financial Table Isolation (Markdown blocks)
    - Text windowing (size: 900, overlap: 120)
    - Metadata tags: [Company | FY | Type | Section | Page]"]
    
    Chunking --> Embedding["EmbeddingEngine:
    - BAAI/bge-small-en-v1.5
    - Dense 384-dimensional vector
    - L2 Normalization (||v|| = 1.0)"]
    
    Embedding --> VectorStore["VectorStore: Persist to PostgreSQL document_chunks"]
    
    UserQuery["Analyst Submits Research Query"] --> QueryEmbed["EmbeddingEngine: Embed Query to 384-d"]
    QueryEmbed --> CosineSearch["pgvector: Cosine Distance Search (<=>)
    Filtered by company_id, doc_type, FY"]
    
    CosineSearch --> TopK["Select Top-K Relevant Chunks (Cosine Distance < 0.65)"]
    TopK --> PromptContext["Context Assembler: Format Grounded Excerpts"]
    PromptContext --> LLMInference["LLM Provider (Gemini 3.5 Flash / Groq)"]
    
    LLMInference --> CitationGen["CitationEngine: Build Page-Level Citations"]
    CitationGen --> Output["Evidence-Grounded Response with Clickable References"]
```

---

## 6. Financial Analytics & Forecasting Architecture

### 6.1 Deterministic Accounting Calculator
* Strictly separates mathematical computation from generative language models.
* `FinancialCalculator` implements zero-denominator safeguards across all ratios:
  * YoY Revenue Growth: $(\frac{\text{Value}_t - \text{Value}_{t-1}}{|\text{Value}_{t-1}|}) \times 100$
  * EBITDA & PAT Margins: $(\frac{\text{Metric}}{\text{Revenue}}) \times 100$
  * DuPont ROE: $(\frac{\text{Net Profit}}{\text{Equity}}) \times 100$
  * ROCE: $(\frac{\text{EBIT}}{\text{Total Assets} - \text{Current Liabilities}}) \times 100$
  * Free Cash Flow: $\text{Operating Cash Flow} - |\text{CapEx}|$
  * Solvency: $\text{Debt-to-Equity} = \frac{\text{Total Debt}}{\text{Equity}}$, $\text{Current Ratio} = \frac{\text{Current Assets}}{\text{Current Liabilities}}$

### 6.2 Econometric Forecasting Engine
* Combines autoregressive modeling $AR(p)$ with linear ordinary least squares (OLS) time-series trends.
* Generates 3 discrete operational trajectories:
  * **Base Case:** Historical econometric trajectory.
  * **Bullish Scenario:** $+15\%$ to $+20\%$ expansion band.
  * **Bearish Scenario:** $-15\%$ contraction band.
* Evaluates out-of-sample forecast accuracy using chronological walk-forward cross-validation (MAE, RMSE, MAPE, Directional Accuracy).
* Attaches mandatory regulatory compliance disclaimers to all outputs.

---

## 7. News & Corporate Deals Intelligence Architecture

* **Multi-Source Ingestion:** Marketaux REST API integration with fallback to high-fidelity Indian equity fixtures.
* **Collision-Safe Entity Matching (`NewsEntityMatcher`):** Employs word-boundary regular expressions (`\bSYMBOL\b`) to prevent false positives on common words (e.g. matching "IT" to L&T Infotech or "reliance" in prose).
* **Taxonomy Classification (`NewsEventClassifier`):** Categorizes articles into `Earnings`, `Contracts`, `M&A`, `Regulatory`, `Dividends`, and `Partnerships`.
* **Tone Sentiment Scoring (`NewsSentimentAnalyzer`):** Lexicon-weighted tone scoring between `-1.0` (Extremely Bearish) and `+1.0` (Extremely Bullish).

---

## 8. External API Communication & Resilient Failover

```mermaid
graph LR
    Engine["Backend Engine Registry"] --> Router["Provider Router"]
    
    Router -->|Primary LLM| Gemini["Google Gemini (gemini-3.5-flash)"]
    Router -->|Fast LLM| Groq["Groq Cloud (qwen/qwen3.8-27b)"]
    Router -->|News Stream| Marketaux["Marketaux API"]
    Router -->|Broker Auth| Dhan["DhanHQ Brokerage"]
    Router -->|Global Data| FMP["Financial Modeling Prep (/stable)"]
    Router -->|Telemetry| Langfuse["Langfuse Cloud US"]

    Gemini -.->|404 Deprecation Fallback| Gemini_Fall["Auto-resolve to 3.5/3.8 Flash"]
    Groq -.->|404 Tier Fallback| Groq_Fall["Auto-resolve to qwen3.8-27b"]
    Dhan -.->|Code 806 Data Unsubscribed| Dhan_Fall["Graceful Fallback to Fixtures"]
    FMP -.->|HTTP 402 Plan Restriction| FMP_Fall["Graceful Fallback to Local Engine"]
```

---

## 9. Security & Access Architecture

* **Authentication:** JWT tokens signed via HMAC-SHA256 (`HS256`) with configurable expiration.
* **Database Isolation:** Supabase PostgreSQL with SSL encryption and Row Level Security (RLS) isolating documents and chat sessions by `user_id`.
* **Prompt Injection Defense:** Strict XML delimitation between system instructions and untrusted document chunks.
* **Input Validation:** Pydantic v2 strict schema enforcement and file extension/MIME whitelisting.

