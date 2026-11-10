# ALPHANEXUS

### AI-Powered Financial Intelligence & Equity Research Platform

<p align="center">
  <strong>See Beyond the Stock Price.</strong>
</p>

<p align="center">
  An intelligent financial research platform combining AI, Retrieval-Augmented Generation, financial analytics, market intelligence and predictive modelling to help users understand companies beyond their market valuations.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-ALPHANEXUS-1558C9?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-LangChain-1C3C3C?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Database-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
</p>

---

## 1. Overview

**ALPHANEXUS** is an AI-powered financial intelligence and equity research platform designed to transform how users research, evaluate and understand publicly listed companies.

Traditional stock research often requires manually navigating annual reports, financial statements, corporate announcements, market news and historical financial data.

ALPHANEXUS aims to bring these information sources together through an integrated intelligence platform.

By combining Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), financial analytics, market data integrations and predictive modelling, the platform aims to provide contextual, evidence-based financial insights.

Initially focused on the Indian equity market, ALPHANEXUS is designed around companies listed on:

- National Stock Exchange (NSE).
- Bombay Stock Exchange (BSE).

### Core vision

Move beyond conventional stock-price tracking and provide deeper insights into:

- What is happening inside a company?
- How is its financial performance evolving?
- What does management communicate about future plans?
- What major developments could affect its business?
- What do its financial statements reveal?
- What risks and opportunities emerge from available information?

---

## 2. Project Identity

| Attribute | Description |
|---|---|
| Project | ALPHANEXUS |
| Category | Financial Intelligence / FinTech |
| Primary Domain | Equity Research and Financial Analytics |
| Initial Market | Indian Equity Market |
| Exchanges | NSE and BSE |
| Architecture | Modular Full-Stack Application |
| Frontend | React + TypeScript |
| Backend | Python + FastAPI |
| AI Framework | LangChain |
| Embedding Framework | Sentence Transformers |
| Vector Database | MongoDB Atlas Vector Search |
| Primary LLM | Google Gemini |
| Financial Analytics | Python, Pandas, NumPy, Scikit-learn |
| Visualization | TradingView Lightweight Charts / Plotly |
| Development | Modular Monorepo |

---

## 3. Brand Identity

ALPHANEXUS uses a distinctive visual identity inspired by premium financial technology interfaces.

| Colour | Hex Code | Usage |
|---|---|---|
| Midnight Black | `#030407` | Primary dark background |
| Electric Cobalt Blue | `#1558C9` | Primary brand colour |
| Acid Lime | `#D4FF24` | Highlights and active indicators |

### Design philosophy

- Premium financial-terminal aesthetics.
- Apple Liquid Glass-inspired navigation.
- Minimalist and information-focused layouts.
- Professional financial visualizations.
- Smooth animations and micro-interactions.
- Fully functional light and dark themes.
- Responsive desktop and mobile experiences.

---

## 4. Core Features

### 4.1 AI-Powered Document Intelligence

Upload and analyze company-related financial documents.

Supported document formats are intended to include:

- PDF
- DOCX
- TXT
- CSV
- XLSX

Document intelligence capabilities:

- Document extraction.
- Financial-year identification.
- Company and ticker metadata.
- Intelligent document chunking.
- Semantic embedding generation.
- Vector indexing.
- Contextual document retrieval.
- Source-grounded AI responses.

Potential document sources include annual reports, quarterly results, investor presentations, earnings call transcripts and corporate announcements.

### 4.2 Retrieval-Augmented Generation (RAG)

ALPHANEXUS uses a modular RAG architecture to retrieve relevant information from company documents before generating answers.

The intended pipeline:

```text
Document Upload
      |
      v
Document Extraction
      |
      v
Text Processing
      |
      v
Intelligent Chunking
      |
      v
Embedding Generation
      |
      v
MongoDB Vector Storage
      |
      v
Semantic / Hybrid Retrieval
      |
      v
Context Assembly
      |
      v
LLM Answer Generation
      |
      v
Grounded Answer + Citations
```

RAG capabilities:

- Company-specific document retrieval.
- Financial-year filtering.
- Semantic search.
- Metadata filtering.
- Hybrid retrieval.
- Context-aware question answering.
- Source and page references.
- Retrieval evaluation.

### 4.3 AI Research Assistant

An intelligent financial research assistant for interacting with company information.

Example questions:

- Summarize the company's latest annual report.
- What are the major risks highlighted by management?
- Compare revenue between FY2025 and FY2026.
- Explain the changes in operating margins.
- What are the company's expansion plans?
- Identify important capital expenditure announcements.
- What are the major challenges facing the business?

Answers should use available evidence and cite relevant documents.

### 4.4 Financial Analytics Engine

Analyze financial performance using structured financial data.

Key metrics:

| Category | Metrics |
|---|---|
| Revenue | Revenue growth, CAGR |
| Profitability | EBITDA, EBIT, PAT |
| Margins | Gross margin, EBITDA margin, PAT margin |
| Returns | ROE, ROCE, ROA |
| Valuation | P/E, P/B, EPS |
| Leverage | Debt-to-equity |
| Cash Flow | Operating cash flow, free cash flow |
| Growth | YoY and QoQ comparisons |

Calculations should be performed using deterministic Python functions rather than relying on LLM-generated arithmetic.

### 4.5 News Intelligence

Aggregate and organize company-related financial news.

Potential categories:

- Business developments.
- Management updates.
- Industry developments.
- Financial results.
- Acquisitions.
- Mergers.
- Partnerships.
- Major contracts.
- Regulatory developments.

Each news item should retain its source, publication date and original link.

### 4.6 Corporate Actions and Events

Monitor significant corporate developments, including:

- Dividend declarations.
- Bonus issues.
- Stock splits.
- Buybacks.
- Fundraising.
- Mergers and acquisitions.
- Major order wins.
- Contract announcements.
- Regulatory disclosures.

Official exchange and company disclosures should be prioritized for verification.

### 4.7 Financial Forecasting

Develop data-driven financial forecasting capabilities.

Potential forecasting targets:

- Revenue.
- Net profit.
- EBITDA.
- EPS.
- Operating performance.

Potential models:

- Linear Regression.
- Random Forest.
- XGBoost.
- ARIMA.
- Other appropriate time-series models.

The forecasting engine should include:

- Historical data preparation.
- Time-based validation.
- Backtesting.
- Model evaluation.
- MAE and RMSE.
- Prediction intervals where statistically justified.

Forecasts represent model estimates, not guaranteed financial outcomes.

---

## 5. System Architecture

ALPHANEXUS follows a modular architecture that separates presentation, API services, AI orchestration, financial computation and data storage.

```text
                 USER
                  |
                  v
       REACT + TYPESCRIPT FRONTEND
                  |
          HTTP / HTTPS / SSE
                  |
                  v
            FASTAPI BACKEND
                  |
       +----------+-----------+
       |          |           |
       v          v           v
    AI/RAG    FINANCIAL     NEWS &
    ENGINE    ENGINE        EVENTS
       |          |           |
       v          v           v
   LANGCHAIN   PYTHON      PROVIDERS
       |
       v
  SENTENCE TRANSFORMERS
       |
       v
 MONGODB ATLAS VECTOR SEARCH
       |
       v
  DOCUMENTS / CHUNKS /
  EMBEDDINGS / METADATA
```

### Architectural responsibilities

| Layer | Responsibility |
|---|---|
| React frontend | User interface and interactions |
| FastAPI | API endpoints and backend orchestration |
| LangChain | Document processing and RAG workflows |
| Sentence Transformers | Embedding generation |
| MongoDB | Document metadata and vector storage |
| Financial engine | Financial calculations and analysis |
| News engine | News and corporate event aggregation |
| Forecasting engine | Model training and prediction |
| External providers | Market data and financial information |

---

## 6. Technology Stack

### Frontend

| Technology | Purpose |
|---|---|
| React | Component-based UI |
| TypeScript | Type safety |
| Vite | Development and build tooling |
| Tailwind CSS | Styling |
| shadcn/ui | Reusable UI primitives |
| Motion | Animations and transitions |
| Lucide React | Icons |
| Zustand | Client-side state |
| TanStack Query | Server state and API caching |
| React Hook Form | Forms |
| Zod | Schema validation |
| TradingView Lightweight Charts | Financial charts |
| Recharts / Plotly | Analytics visualization |

### Backend

| Technology | Purpose |
|---|---|
| Python | Core backend language |
| FastAPI | REST API framework |
| Pydantic | Data validation |
| Uvicorn | ASGI server |
| HTTPX | HTTP communication |
| SQLAlchemy | Relational database operations where required |

### AI and RAG

| Technology | Purpose |
|---|---|
| LangChain | RAG orchestration |
| LangGraph | Stateful AI workflows where needed |
| Sentence Transformers | Embedding generation |
| BGE Base EN v1.5 | Initial embedding model |
| Google Gemini | Primary LLM |
| Groq | Optional LLM provider |
| MongoDB Atlas Vector Search | Semantic retrieval |
| Ragas | RAG evaluation |

### Financial Analytics

| Technology | Purpose |
|---|---|
| Pandas | Data processing |
| NumPy | Numerical computing |
| Scikit-learn | Machine learning |
| XGBoost | Predictive modelling |
| Statsmodels | Statistical and time-series modelling |
| SciPy | Scientific computing |
| Plotly | Interactive visualizations |

---

## 7. Project Structure

The entire project is maintained inside the `ALPHANEXUS/` root directory.

```text
ALPHANEXUS/
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── app/
│       ├── assets/
│       ├── components/
│       ├── pages/
│       ├── features/
│       ├── hooks/
│       ├── services/
│       ├── stores/
│       ├── styles/
│       ├── types/
│       ├── App.tsx
│       └── main.tsx
│
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── schemas/
│       ├── services/
│       ├── engines/
│       │   ├── rag/
│       │   ├── financial/
│       │   ├── forecasting/
│       │   └── news/
│       ├── integrations/
│       ├── database/
│       ├── workers/
│       └── main.py
│
├── data/
├── models/
├── configs/
├── scripts/
├── tests/
├── docs/
├── logs/
│
├── .env.example
├── .gitignore
├── README.md
└── Makefile
```

The structure may evolve as implementation progresses. Refer to the actual repository for the current implementation.

---

## 8. Installation and Local Development

### Prerequisites

Install:

- Node.js and npm.
- Python compatible with the backend dependencies.
- Git.
- MongoDB Atlas account or a compatible MongoDB deployment.
- Required external API credentials.

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd ALPHANEXUS
```

### Step 2: Configure environment variables

Create the required environment configuration files using `.env.example`.

```bash
cp .env.example backend/.env
```

Adapt the file locations to the application's actual configuration loader.

Do not commit `.env` files or expose API secrets.

### Step 3: Backend setup

```bash
cd backend

python -m venv .venv
```

Activate the environment.

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If the existing application uses a different import path, follow the actual backend entry point.

Backend API documentation:

```text
http://127.0.0.1:8000/docs
```

### Step 4: Frontend setup

Open another terminal.

```bash
cd ALPHANEXUS/frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Open the Vite URL displayed in the terminal, commonly:

```text
http://localhost:5173
```

### Step 5: Verify integration

Check:

- Frontend starts successfully.
- FastAPI is reachable.
- MongoDB connection works.
- Required API keys are configured.
- AI provider connectivity works.
- RAG vector index is available.
- Document upload and processing work.

Do not consider an integration operational merely because its configuration exists.

---

## 9. Environment Variables

The following variables represent the expected configuration categories. Exact names should match the implemented settings classes.

| Variable | Purpose |
|---|---|
| `APP_ENV` | Application environment |
| `BACKEND_HOST` | Backend host |
| `BACKEND_PORT` | Backend port |
| `FRONTEND_API_URL` | Backend URL used by frontend |
| `MONGODB_URI` | MongoDB connection string |
| `MONGODB_DATABASE` | Database name |
| `GEMINI_API_KEY` | Gemini API authentication |
| `GROQ_API_KEY` | Optional Groq integration |
| `DHAN_CLIENT_ID` | Dhan API client ID |
| `DHAN_ACCESS_TOKEN` | Dhan access token |
| `MARKETAUX_API_TOKEN` | Marketaux API token |
| `FMP_API_KEY` | Optional financial data provider |

### Security requirements

- Store private credentials only in backend environment configuration.
- Never hardcode API keys.
- Never expose credentials through frontend environment variables.
- Never commit secrets to GitHub.
- Use environment-specific configuration.
- Validate provider connectivity at startup or through health endpoints.

---

## 10. API Architecture

The frontend communicates with the backend through FastAPI.

Expected API groups include:

| API Group | Responsibility |
|---|---|
| `/api/v1/health` | System health |
| `/api/v1/auth` | Authentication |
| `/api/v1/documents` | Document management |
| `/api/v1/rag` | Retrieval and question answering |
| `/api/v1/chat` | AI conversations |
| `/api/v1/companies` | Company information |
| `/api/v1/financials` | Financial statements and ratios |
| `/api/v1/news` | Financial news |
| `/api/v1/corporate-actions` | Corporate developments |
| `/api/v1/forecasting` | Financial forecasting |

Actual endpoints and response contracts should be verified against the implemented backend.

---

## 11. RAG Configuration

The initial RAG configuration is designed around:

| Component | Initial Choice |
|---|---|
| Embedding framework | Sentence Transformers |
| Embedding model | BAAI/bge-base-en-v1.5 |
| Embedding dimensions | 768 |
| Vector database | MongoDB Atlas Vector Search |
| Orchestration | LangChain |
| Primary LLM | Gemini |
| Retrieval | Dense / Hybrid |
| Chunking | Financial structure-aware |
| Evaluation | Ragas + custom metrics |

### Document chunking

Use document-aware chunking rather than applying a single splitting strategy to every financial document.

Examples:

- Annual reports: section-aware chunks.
- Management discussion: narrative-aware chunks.
- Earnings transcripts: speaker-aware chunks.
- Investor presentations: slide-aware chunks.
- Financial tables: table-aware processing.
- Corporate announcements: event-aware chunks.

The exact chunk sizes and retrieval parameters should be calibrated using a representative financial question-answer evaluation dataset.

---

## 12. Data Sources and Integrations

Potential data providers and information sources:

| Source | Intended Usage |
|---|---|
| NSE | Official exchange disclosures |
| BSE | Official exchange disclosures |
| SEBI | Regulatory information |
| Company investor relations | Annual reports and financial documents |
| DhanHQ | Authorized market data |
| Marketaux | Financial news |
| Financial Modeling Prep | Optional financial fundamentals |
| Google Gemini | LLM capabilities |
| Groq | Optional LLM inference |

Provider availability, API coverage, subscription limits and licensing must be verified before production use.

Official exchange disclosures and company-published information should be prioritized for material corporate developments.

---

## 13. Security and Reliability

Security is a core requirement.

The platform should implement:

- Authentication and authorization.
- User-specific document access.
- Secure API credentials.
- File validation.
- Request validation.
- Rate limiting.
- Secure error handling.
- Structured logging.
- Database access controls.
- Audit trails for sensitive operations.
- Prompt-injection protection.
- Retrieval authorization filters.

Uploaded documents must be treated as untrusted input.

Financial calculations must be performed through validated backend functions.

AI-generated answers must distinguish source-backed facts from estimates and interpretations.

---

## 14. Testing

Testing should cover the complete application.

### Frontend

- Component tests.
- Theme switching.
- Navigation.
- Form validation.
- API error handling.
- Responsive layouts.
- Chart rendering.

### Backend

- API route tests.
- Database connection.
- Document processing.
- Embedding generation.
- Vector retrieval.
- RAG response generation.
- Financial calculations.
- Forecast evaluation.

### End-to-end

Test the complete workflow:

1. Open ALPHANEXUS.
2. Search for a company.
3. Upload its annual report.
4. Process and index the document.
5. Ask a question through the AI research assistant.
6. Verify the retrieved evidence.
7. Verify the answer and citations.
8. Review financial analytics.
9. Verify the application handles missing data correctly.

---

## 15. Development Roadmap

| Phase | Focus | Objective |
|---|---|---|
| Phase 1 | Foundation | Project architecture, configuration and environment |
| Phase 2 | Frontend | React UI, design system and responsive layouts |
| Phase 3 | Backend | FastAPI services and API integration |
| Phase 4 | RAG | Document ingestion, embeddings and retrieval |
| Phase 5 | Intelligence | AI research assistant and financial analytics |
| Phase 6 | Market Intelligence | News and corporate actions |
| Phase 7 | Forecasting | Financial prediction and model evaluation |
| Phase 8 | Quality | Testing, optimization and security |
| Phase 9 | Deployment | Production infrastructure and monitoring |

Implementation status should be updated as features are completed and verified.

---

## 16. Project Principles

ALPHANEXUS follows these engineering principles:

1. **Evidence over assumptions:** Financial insights should be supported by verifiable information.
2. **Modular architecture:** Keep individual engines independent and maintainable.
3. **Separation of concerns:** Frontend, backend, AI orchestration and data access must remain separated.
4. **Data integrity:** Never fabricate market prices, financial results or corporate events.
5. **Explainability:** Provide supporting documents and citations for AI-generated research.
6. **Security first:** Protect financial data, credentials and uploaded documents.
7. **Scalability:** Build reusable services and well-defined API contracts.
8. **Continuous evaluation:** Measure retrieval quality, forecasting performance and system reliability.

---

## 17. Disclaimer

ALPHANEXUS is intended as a financial research and intelligence platform.

Its analytical outputs, AI-generated summaries and model forecasts are informational in nature.

They should not be interpreted as guaranteed investment returns or personalized investment advice.

Users should independently verify important financial information using official disclosures and appropriate professional sources.

---

## 18. Contributing

Contributions and improvements should follow the existing project architecture.

Recommended workflow:

1. Create a feature branch.
2. Implement changes within the appropriate module.
3. Follow established coding conventions.
4. Add or update tests.
5. Verify frontend and backend integration.
6. Submit a pull request with a clear description.

Do not commit API keys, private documents, generated datasets or sensitive credentials.

---

## 19. Future Vision

ALPHANEXUS aims to evolve into a comprehensive financial intelligence ecosystem.

Potential future capabilities include:

- Multi-company comparative intelligence.
- Automated financial report monitoring.
- Intelligent portfolio research.
- Advanced financial anomaly detection.
- Management sentiment analysis.
- Industry and sector intelligence.
- Multi-agent financial research workflows.
- Personalized research workspaces.
- Advanced event-impact analysis.
- Automated research report generation.

---

<p align="center">
  <strong>ALPHANEXUS</strong>
  <br/>
  <em>See Beyond the Stock Price.</em>
  <br/><br/>
  Built to bring intelligence, context and clarity to financial research.
</p>
