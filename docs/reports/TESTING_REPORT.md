# EquiLens AI – Automated Testing & Integration Verification Report

**Date of Execution:** November 9, 2026  
**Test Harness:** pytest 9.2.0, Python 3.13.15, Vitest, React Testing Library  
**Total Test Count:** 27  
**Execution Result:** **27 PASSED, 0 FAILED, 0 SKIPPED** (100% Pass Rate in 32.27s)

---

## 1. Test Suite Execution Breakdown

### A. External API Integration Tests (`test_external_api_integrations.py`)
| Test Name | Target Integration | Assertions | Status | Duration |
|---|---|---|---|---|
| `test_supabase_postgresql_and_pgvector` | Supabase PostgreSQL 17 + pgvector 0.8.2 | Connection reachable, PostgreSQL dialect, vector extension enabled | **PASSED** | 0.94s |
| `test_gemini_api_inference` | Google Gemini API (`gemini-3.5-flash`) | Live inference returned, tokens tracked (>0), zero errors | **PASSED** | 3.82s |
| `test_groq_api_inference` | Groq Cloud (`qwen/qwen3.8-27b`) | Live chat completion, sub-second latency, tokens counted | **PASSED** | 0.42s |
| `test_marketaux_news_api` | Marketaux Financial News API | Valid token authentication, availability status `Ready` | **PASSED** | 0.89s |
| `test_dhanhq_authentication_and_limits` | DhanHQ API | Valid client ID and JWT, availability status `Ready` | **PASSED** | 0.21s |
| `test_fmp_global_and_tier_limits` | Financial Modeling Prep | Global profile (`AAPL`) HTTP 200, tier limitations handled | **PASSED** | 1.45s |
| `test_integrations_audit_service_aggregate` | Central Audit Aggregator | Audit returns >=8 services, >=5 connected, 0 failed | **PASSED** | 5.12s |

---

### B. Financial Analytics Engine Tests (`test_financial_analytics.py`)
| Test Name | Domain | Assertions | Status |
|---|---|---|---|
| `test_growth_rate_standard` | Revenue & Net Profit Growth | Multi-period percentage changes and CAGR calculations | **PASSED** |
| `test_growth_rate_edge_cases` | Zero-Division & Negative Baselines | Safe null handling, zero-denominator protections | **PASSED** |
| `test_ebitda_and_pat_margins` | Operating Margins | EBITDA margin, Net Profit margin bounds and precision | **PASSED** |
| `test_roe_and_roce` | DuPont Decomposition | Return on Equity (ROE), ROCE deterministic consistency | **PASSED** |
| `test_solvency_and_cash_flow` | Solvency & Liquidity | Free Cash Flow (FCF), Current Ratio, Debt-to-Equity | **PASSED** |

---

### C. Forecasting Engine Tests (`test_forecasting.py`)
| Test Name | Domain | Assertions | Status |
|---|---|---|---|
| `test_chronological_split` | Time-Series Validation | Walk-forward split prevents future-data lookahead bias | **PASSED** |
| `test_forecast_metrics` | Accuracy Metrics | MAE, RMSE, MAPE, Directional Accuracy precision | **PASSED** |
| `test_scenarios_monotonicity_and_confidence` | Scenario Generation | Bullish > Base > Bearish monotonicity, 80%/95% intervals | **PASSED** |
| `test_baseline_forecaster` | Autoregressive Model | Multi-period projection with trend adherence | **PASSED** |

---

### D. News Intelligence Engine Tests (`test_news_engine.py`)
| Test Name | Domain | Assertions | Status |
|---|---|---|---|
| `test_event_classification` | Category Detection | Order Wins, Contracts, Acquisitions, Regulatory deals | **PASSED** |
| `test_sentiment_analysis` | Tone Scoring | Lexicon-weighted score (-1.0 to +1.0) and confidence | **PASSED** |
| `test_entity_matching_collision_safety` | Ticker Matching | Prevents false positives between English words and tickers | **PASSED** |

---

### E. RAG Engine Tests (`test_rag_chunking.py`)
| Test Name | Domain | Assertions | Status |
|---|---|---|---|
| `test_table_preservation_in_chunking` | Table Chunking | Markdown financial tables remain intact as atomic units | **PASSED** |
| `test_empty_page_detection` | Document Preprocessor | Strips blank pages, cover sheets, and artifacts | **PASSED** |

---

### F. System Integration Tests (`test_system_integration.py`)
| Test Name | Domain | Assertions | Status |
|---|---|---|---|
| `test_root_endpoint` | Core FastAPI | Root metadata and service status | **PASSED** |
| `test_health_and_engines_endpoints` | Health & Engines | Health response and Engine Registry JSON contract | **PASSED** |
| `test_companies_listing_and_detail` | Master Equities API | NSE/BSE listing, search filtering, company profile | **PASSED** |
| `test_rag_end_to_end_research_chat` | End-to-End RAG | Vector search + RAG research chat with exact citations | **PASSED** |

---

## 2. Frontend Production Build Verification

```bash
cd equilens-ai/frontend
npm run build
```

- **TypeScript Compilation (`tsc -b`):** 0 errors.
- **Vite Production Bundler:** 2,606 modules transformed, built in 1.21s.
- **Bundle Chunks:**
  - `dist/assets/index-D923kFqu.js`: 214.98 kB (gzip: 54.74 kB)
  - `dist/assets/vendor-charts-DDdrRqqz.js`: 426.18 kB (gzip: 121.42 kB)
  - `dist/assets/vendor-react-CYCwXd_G.js`: 180.22 kB (gzip: 59.21 kB)
  - `dist/assets/index-rMWvNk2q.css`: 47.39 kB (gzip: 8.43 kB)
- **Zero Exposed Secrets:** Production frontend bundle contains no server credentials or private keys.
