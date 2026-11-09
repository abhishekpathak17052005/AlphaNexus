# EquiLens AI – Technical Architecture Specification

## 1. System Vision & Design Philosophy

EquiLens AI is architected as an institutional-grade financial intelligence research terminal combining:
1. Retrieval-Augmented Generation (RAG) with page-level citations.
2. Deterministic Financial Analytics (zero-tolerance for hallucinated mathematical metrics).
3. Statistical Performance Forecasting (scenario bands with explicit parametric confidence intervals).
4. News & Corporate Deals Intelligence (deduplication, event classification, sentiment).
5. Central Engine Registry (dynamic health introspection and graceful degradation).

---

## 2. Engine Pipelines

### 2.1 RAG & Document Intelligence Pipeline

```text
[Document Upload] (PDF / DOCX / XLSX / CSV)
       │
       ▼
[File Validation & Normalization] ──> SHA-256 Hash Deduplication
       │
       ▼
[Multi-Modal Extractor]
  ├── PDF: pdfplumber & pypdf (Text + Tables)
  ├── DOCX: python-docx (Headings + Paragraphs)
  └── Tabular: pandas & openpyxl (Spreadsheets & Models)
       │
       ▼
[Section-Aware Chunker]
  ├── Preserves Financial Tables as Atomic Blocks
  └── Injects Metadata: [Company | FY | Type | Page | Section]
       │
       ▼
[Embedding Engine: BAAI/bge-small-en-v1.5]
  └── Dense 384-dimensional unit-normalized embeddings (L2 Norm = 1.0)
       │
       ▼
[pgvector / PostgreSQL] ──> Cosine Distance Indexing
       │
       ▼
[Query Semantic Retrieval] ──> Top-K relevant chunks filtered by metadata
       │
       ▼
[Citation Engine] ──> Extracts exact document, page number, section, and confidence
       │
       ▼
[LLM Provider Adapter] (Gemini 1.5 Flash / Groq)
       │
       ▼
[Evidence-Grounded Output] ──> Fact Grounded | Calculated | Synthesis
```

---

### 2.2 Financial Analytics Engine

All fundamental accounting formulas are implemented deterministically using Pandas and NumPy:

- **Revenue / Profit Growth:**
  $$\text{Growth YoY} = \frac{\text{Value}_t - \text{Value}_{t-1}}{|\text{Value}_{t-1}|} \times 100$$
  *Safety:* Evaluates zero and negative denominators, returning explicit `None`.

- **DuPont Return on Equity (ROE):**
  $$\text{ROE} = \frac{\text{Net Profit}}{\text{Shareholders' Equity}} \times 100$$

- **Return on Capital Employed (ROCE):**
  $$\text{ROCE} = \frac{\text{EBIT}}{\text{Total Assets} - \text{Current Liabilities}} \times 100$$

- **Free Cash Flow (FCF):**
  $$\text{FCF} = \text{Operating Cash Flow} - |\text{Capital Expenditures}|$$

- **Debt-to-Equity & Current Ratio:**
  $$\text{D/E} = \frac{\text{Total Debt}}{\text{Shareholders' Equity}}, \quad \text{Current Ratio} = \frac{\text{Current Assets}}{\text{Current Liabilities}}$$

---

### 2.3 Performance Forecasting Engine

- **Model Hierarchy:**
  * Baseline Trend & Autoregressive ($AR(p)$ + Linear OLS)
  * Walk-forward cross-validation (chronological train/test split)
  * Out-of-sample error computation (MAE, RMSE, MAPE, Directional Accuracy)
- **Multi-Scenario Generation:**
  * Base Case: Modeled time-series trajectory
  * Bullish Scenario: $+15\%$ to $+20\%$ expansion
  * Bearish Scenario: $-15\%$ contraction
  * Confidence Intervals: $80\%$ ($z=1.28$) and $95\%$ ($z=1.96$) parametric bounds
- **Mandatory Compliance Disclaimer:**
  Statistical forecasts are quantitative estimates based on historical filings and do not constitute guaranteed stock performance or investment advice.

---

### 2.4 News & Corporate Deals Engine

- **Multi-Source Fetcher:** Marketaux official API adapter + curated Indian equity announcement fixtures.
- **Precision Entity Matcher:** RegEx word boundaries and ticker validation protecting against false entity collisions (e.g., words like "it", "reliance").
- **Event Classifier:** Classifies announcements into Earnings, Contracts, Acquisitions, Mergers, Regulatory, Partnerships, and Dividends.
- **Tone Analyzer:** Lexicon-weighted sentiment scoring ($-1.0$ to $+1.0$) with confidence scores.
- **Deduplication:** Content & URL hashing preventing redundant feed entries.

