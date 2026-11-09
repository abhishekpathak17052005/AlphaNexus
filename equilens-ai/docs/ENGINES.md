# EquiLens AI – Core Intelligence Engines Specification

EquiLens AI is constructed around 11 specialized backend intelligence engines and provider adapters. Each engine maintains independent execution scope, typed schemas, and automated error handling registered in the central `EngineRegistry`.

---

## Engine A: RAG & Financial Document Intelligence Engine

**Module Location:** `app/engines/rag/`  
**Current Status:** **Implemented**  
**Core Classes:** `RAGService`, `DocumentPreprocessor`, `DocumentChunker`, `EmbeddingEngine`, `VectorStore`, `CitationEngine`

### 1. Document Ingestion & Multi-Format Loaders
The ingestion layer accepts regulatory filings and company disclosures across 4 primary file types:
* **PDF Loader (`PDFDocumentLoader`):** Uses `pdfplumber` to extract high-fidelity text layouts, column coordinates, and bounding boxes, supplemented by `pypdf` for fast stream reading.
* **DOCX Loader (`DOCXDocumentLoader`):** Uses `python-docx` to iterate through XML paragraphs, extracting heading hierarchies (`Heading 1`, `Heading 2`) and tabular blocks.
* **Tabular Loader (`TabularDocumentLoader`):** Uses `pandas` and `openpyxl` to parse multi-tab Excel workbooks and raw CSV files, preserving numerical precision.
* **Deduplication:** Computes SHA-256 hash across the raw byte stream (`DocumentPreprocessor.compute_file_hash()`). Ingestion halts if a duplicate checksum exists for the company.

### 2. Preprocessing & Normalization
* **Whitespace & Character Sanitization:** Normalizes non-breaking spaces (`\u00a0`), irregular line breaks, and excessive indentation while preserving accounting indentation.
* **Empty-Page Suppression:** Evaluates pages with fewer than 20 non-whitespace characters and zero tables, suppressing blank separator pages.
* **Automated Document Classification (`infer_document_type`):** Scans file titles and opening pages for keywords:
  * Annual Report / 10-K
  * Quarterly Result / 10-Q / Limited Review
  * Earnings Call Transcript
  * Investor Presentation
  * Corporate Announcement

### 3. Financial-Aware Section Chunking (`DocumentChunker`)
Standard NLP token chunking damages financial statements by slicing balance sheets across token boundaries. `DocumentChunker` implements specialized financial heuristics:
* **Table Preservation as Atomic Blocks:** Financial tables are extracted separately and converted into structured Markdown representations before text chunking. Tables are never bifurcated across chunks.
* **Sliding Window:** Narrative text is chunked with a target size of 900 characters and 120-character overlap.
* **Metadata Prefixing:** Each chunk prepends contextual metadata to ensure semantic density:
  ```text
  [Reliance Industries Limited | FY24 | Annual Report | Financial Highlights | Page 42]
  ... chunk text ...
  ```

### 4. Embedding Generation Engine (`EmbeddingEngine`)
* **Primary Model:** `BAAI/bge-small-en-v1.5` loaded via HuggingFace `sentence-transformers`.
* **Dimensions:** 384-dimensional dense float vector.
* **Normalization:** Computes $L_2$ unit normalization ($\|v\|_2 = 1.0$), transforming cosine similarity into a dot product.
* **Lifecycle Management:** Singleton instance loaded once on server startup to prevent GPU/CPU memory leaks.

### 5. Vector Store & Semantic Retrieval (`VectorStore`)
* **Database Backend:** PostgreSQL 17 + `pgvector` extension v0.8.2.
* **Column Schema:** `embedding vector(384)` indexed with cosine distance operator (`<=>`).
* **Query Execution:** Executes vector similarity queries constrained by metadata filters:
  ```sql
  SELECT id, document_id, content, clean_text, section, page_number,
         (embedding <=> :query_vector) AS cosine_distance
  FROM document_chunks
  WHERE company_id = :company_id
  ORDER BY cosine_distance ASC
  LIMIT :top_k;
  ```
* **Fallback Mode:** Provides in-memory cosine similarity calculation when running on SQLite in local dev environments.

### 6. Citation & Source Verification Engine (`CitationEngine`)
* Extracts exact document title, page number, section title, confidence score, and a 250-character excerpt.
* Structures citations into a typed `Citation` model linked to the parent `ResearchMessage`.
* Ensures that responses display clickable footnotes in the frontend UI without hallucinations.

---

## Engine B: Deterministic Financial Analytics Engine

**Module Location:** `app/engines/analytics/`  
**Current Status:** **Implemented**  
**Core Classes:** `FinancialCalculator`, `PeerAnalyzer`

Financial numbers must never be calculated by LLMs. All mathematical computations in EquiLens AI are deterministic and executed in Python using NumPy and Pandas.

### 1. Zero-Denominator Safety
Every formula enforces rigorous error boundaries, returning `None` instead of throwing exceptions or returning `Infinity` on negative or zero denominators:
```python
if current_value is None or previous_value is None or previous_value == 0:
    return None
```

### 2. Implemented Accounting Formulas
* **YoY Revenue & Profit Growth:**
  $$\text{YoY Growth} = \frac{\text{Value}_t - \text{Value}_{t-1}}{|\text{Value}_{t-1}|} \times 100$$
* **EBITDA Margin & Net Profit Margin:**
  $$\text{EBITDA Margin} = \frac{\text{EBITDA}}{\text{Revenue}} \times 100, \quad \text{PAT Margin} = \frac{\text{Net Profit}}{\text{Revenue}} \times 100$$
* **DuPont 3-Way Return on Equity (ROE):**
  $$\text{ROE} = \frac{\text{Net Profit}}{\text{Shareholders' Equity}} \times 100$$
* **Return on Capital Employed (ROCE):**
  $$\text{ROCE} = \frac{\text{EBIT}}{\text{Total Assets} - \text{Current Liabilities}} \times 100$$
* **Free Cash Flow (FCF):**
  $$\text{FCF} = \text{Operating Cash Flow} - |\text{Capital Expenditures}|$$
* **Solvency & Liquidity:**
  $$\text{Debt-to-Equity} = \frac{\text{Total Debt}}{\text{Equity}}, \quad \text{Current Ratio} = \frac{\text{Current Assets}}{\text{Current Liabilities}}$$

### 3. Peer Comparison Analyzer (`PeerAnalyzer`)
* Computes sector medians for P/E, P/B, ROE, ROCE, and EBITDA Margin across 2 to 5 selected peer companies.
* Flags sector leaders and underperformers based on deterministic metric rankings.

---

## Engine C: Market Data Engine

**Module Location:** `app/engines/providers/dhan.py`  
**Current Status:** **Partially Implemented (Live Trading Auth + Offline Fixtures)**  
**Core Classes:** `DhanHQProvider`

### 1. Provider Integration
* Utilizes the official `dhanhq` Python SDK.
* Authenticates using `DHAN_CLIENT_ID` and `DHAN_ACCESS_TOKEN`.
* Verified live connection to DhanHQ Fund Limit API (`/v2/fundlimit`) returning active trading balance.

### 2. Operational Entitlements & Scrip Master
* **Entitlement Distinction:** DhanHQ separates Trading API access from Market Data feed subscriptions. When Market Data APIs return Code 806 (`Data APIs not Subscribed`), the provider degrades to high-fidelity historical fixtures for NSE/BSE leaders.
* **Scrip Master:** Downloads and caches the complete Dhan security master CSV (27.7MB, 50,000+ instruments) mapping symbols to exchange security IDs.

### 3. Normalization & Technical Indicators
* Formats historical OHLCV records into uniform schemas (`timestamp`, `open`, `high`, `low`, `close`, `volume`).
* Computes 50-day and 200-day Simple Moving Averages (SMA) and Day Change percentages.

---

## Engine D: News & Event Intelligence Engine

**Module Location:** `app/engines/news/`  
**Current Status:** **Implemented**  
**Core Classes:** `NewsService`, `NewsEntityMatcher`, `NewsEventClassifier`, `NewsSentimentAnalyzer`

### 1. Ingestion Pipeline
* Connects to the Marketaux REST API (`https://api.marketaux.com/v1/news/all`).
* Filters for Indian financial publications (`countries=in`, `language=en`).
* Deduplicates articles via URL hashing and UUID verification.

### 2. Collision-Safe Entity Matching (`NewsEntityMatcher`)
Generic substring matching causes severe entity collisions (e.g. matching the English word "it" to "L&T Infotech", or "reliance" in general prose). `NewsEntityMatcher` uses word-boundary regex and ticker validation:
```python
pattern = rf"\b{re.escape(symbol)}\b"
```

### 3. Event Classification (`NewsEventClassifier`)
Classifies news and announcements into predefined institutional taxonomy:
* `Earnings`: Results, EBITDA releases, quarterly reports.
* `Contracts`: Order wins, infrastructure awards, client signings.
* `M&A`: Acquisitions, mergers, asset takeovers.
* `Regulatory`: SEBI orders, tax tribunals, audit inquiries.
* `Dividends`: Interim dividend payouts, record date filings.
* `Partnerships`: Strategic JVs and commercial alliances.

### 4. Tone Sentiment Analysis (`NewsSentimentAnalyzer`)
* Evaluates financial vocabulary weights to produce a continuous sentiment score from `-1.0` (Extremely Bearish) to `+1.0` (Extremely Bullish).
* Computes sentiment labels (`Bullish`, `Bearish`, `Neutral`) with numerical confidence bounds.

---

## Engine E: Corporate Actions & Market Deals Engine

**Module Location:** `app/api/v1/endpoints/corporate_actions.py`, `market_events.py`  
**Current Status:** **Implemented**  
**Database Tables:** `corporate_actions`, `market_events`

### 1. Corporate Actions Processing
Tracks lifecycle states (`Announced`, `Ex-Date`, `Record-Date`, `Completed`) across:
* **Cash Dividends:** Interim and final dividends with dividend yields and record dates.
* **Stock Splits:** Face-value subdivisions (e.g. ₹10 to ₹2).
* **Bonus Issues:** Capitalization of reserves into bonus ratios (e.g. 1:1, 2:1).
* **Rights Issues & Buybacks:** Capital restructuring disclosures.

### 2. Market Deals & Contract Tracking
* Captures high-impact commercial developments: counterparty names, disclosed deal values in INR Crores, and strategic execution timelines.
* Computes strategic impact ratings to highlight accretive or dilutive transactions.

---

## Engine F: Econometric Performance Forecasting Engine

**Module Location:** `app/engines/forecasting/`  
**Current Status:** **Implemented**  
**Core Classes:** `ForecastingService`, `BaselineForecaster`, `ScenarioGenerator`, `ForecastValidator`

### 1. Model Architecture (`BaselineForecaster`)
* Combines autoregressive modeling $AR(p)$ with ordinary least squares (OLS) linear trend projections.
* Enforces minimum data adequacy ($\ge 3$ historical periods) before modeling.

### 2. Walk-Forward Cross-Validation (`ForecastValidator`)
Evaluates model accuracy using chronological time-series splitting to prevent lookahead bias:
* **Mean Absolute Error (MAE):** $\frac{1}{n} \sum |y - \hat{y}|$
* **Root Mean Squared Error (RMSE):** $\sqrt{\frac{1}{n} \sum (y - \hat{y})^2}$
* **Mean Absolute Percentage Error (MAPE):** $\frac{1}{n} \sum |\frac{y - \hat{y}}{y}| \times 100$
* **Directional Accuracy:** Percentage of periods where predicted trend matches realized direction.

### 3. Multi-Scenario Projections (`ScenarioGenerator`)
* **Base Case:** Pure econometric model trajectory.
* **Bullish Scenario:** $+15\%$ to $+20\%$ expansion over baseline.
* **Bearish Scenario:** $-15\%$ contraction below baseline.
* **Parametric Confidence Bounds:**
  * $80\%$ Confidence Interval ($z = 1.28 \times \sigma$)
  * $95\%$ Confidence Interval ($z = 1.96 \times \sigma$)

### 4. Regulatory Disclaimer
Mandatory non-advisory disclaimer attached to all forecast records:
> *"Statistical forecasts are quantitative estimates based on historical financial filings and do not constitute investment advice or guaranteed future performance."*

---

## Engine G: AI Orchestration & LLM Routing Engine

**Module Location:** `app/engines/providers/`  
**Current Status:** **Implemented**  
**Core Classes:** `GeminiProvider`, `GroqProvider`, `EngineRegistry`

### 1. Dual-Provider Architecture
* **Primary LLM (Google Gemini):** Uses `gemini-3.5-flash` (with automatic graceful fallback from deprecated `gemini-1.5-flash`). Delivers institutional financial synthesis with structured citation formatting.
* **High-Speed Alternative (Groq):** Uses `qwen/qwen3.8-27b` (with auto-fallback from unprovisioned account tiers) to deliver sub-second inference latency (~390ms).

### 2. Dynamic Health Monitoring (`EngineRegistry`)
* Central registry monitoring all 11 engines on every health check.
* Tracks states: `Ready`, `Degraded`, `Disabled`, `Failed`.
* Transparently surfaces provider limitations to the API client without crashing application startup.

