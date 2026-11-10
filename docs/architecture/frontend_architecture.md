# ALPHANEXUS – Frontend Architecture

## 1. Overview

The ALPHANEXUS frontend is built as a stateful, interactive workspace using **Streamlit** styled with **Liquid Glass UI design tokens** and augmented with custom React components.

---

## 2. Page Organization

The workspace is organized into eight dedicated pages:

| Page | Script | Responsibility |
|---|---|---|
| **1. Overview Dashboard** | `1_📊_Overview_Dashboard.py` | Macro market indices (Nifty, Sensex), watchlist KPI metrics, and system status. |
| **2. Company Research** | `2_🏢_Company_Research.py` | In-depth company profile, key financial ratios, valuation multiples, and historical prices. |
| **3. Document Intelligence** | `3_📄_Document_Intelligence.py` | Multi-format file ingestion (PDF, DOCX, XLSX), parsing progress, and chunk preview. |
| **4. AI Research Assistant** | `4_🤖_AI_Research_Assistant.py` | Grounded conversational QA with source citations, page references, and similarity scores. |
| **5. Financial Analysis** | `5_📈_Financial_Analysis.py` | Balance sheet, P&L, DuPont decomposition, and peer benchmark comparison charts. |
| **6. News & Corporate Actions** | `6_📰_News_and_Corporate_Actions.py` | Sentiment categorization, dividend/split tracker, and block deal feeds. |
| **7. Performance Forecasting** | `7_🔮_Performance_Forecasting.py` | Monte Carlo revenue and EPS projections under Bull, Base, and Bear scenarios. |
| **8. RAG Administration** | `8_⚙️_RAG_Administration.py` | Vector store diagnostics, chunk inspection, and retrieval latency benchmarks. |

---

## 3. UI Component System

Component modules in `frontend/components/`:
- `navbar/`: Displays sticky top bar with active market indices.
- `sidebar/`: Company selector with NSE/BSE ticker auto-complete.
- `cards/`: Metric cards with glassmorphic backdrop filters and colored delta badges.
- `chat/`: Chat message bubbles with expandable source attribution cards.
- `charts/`: Reusable Plotly chart constructors.

