# EquiLens AI

**See Beyond the Stock Price.**

EquiLens AI is an AI-powered equity research and financial intelligence platform for NSE and BSE-listed Indian companies. It combines financial document intelligence (RAG), financial analytics, corporate action tracking, news intelligence, and evidence-backed research generation.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React 18, TypeScript, Vite 5, Tailwind CSS v4, shadcn/ui, Recharts, TanStack Query, Zustand, React Router v7 |
| Backend | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic |
| Database | PostgreSQL 16 + pgvector (Supabase or local Docker) |
| AI / RAG | Google Gemini 1.5, Groq (optional), BAAI/bge-small-en-v1.5 embeddings, semantic vector search |
| Infrastructure | Docker, Docker Compose, Redis, Celery (workers), Langfuse, Sentry |
| Deployment | Vercel (frontend), Render (backend) |

---

## Architecture Overview

```
equilens-ai/
├── frontend/           React + TypeScript single-page application
│   └── src/
│       ├── components/ Reusable UI components (layout, charts, ui primitives)
│       ├── pages/      Route-level page components (13 pages)
│       ├── services/   API client (axios)
│       ├── stores/     Zustand state (theme, auth)
│       └── types/      Shared TypeScript interfaces
│
├── backend/            FastAPI Python application
│   └── app/
│       ├── api/v1/     REST API endpoints
│       ├── core/       Config, database, logging, engine registry
│       ├── engines/    Business logic engines (RAG, analytics, forecasting, news)
│       ├── integrations/ External provider adapters (Gemini, Groq, DhanHQ, etc.)
│       ├── models/     SQLAlchemy ORM models
│       ├── schemas/    Pydantic request/response schemas
│       └── services/   Cross-cutting services (seed data)
│
├── database/           SQL init scripts, migrations, seeds
├── docker-compose.yml  Local infrastructure (PostgreSQL + Redis)
└── README.md
```

---

## Prerequisites

- Node.js 20+
- Python 3.11+
- Docker + Docker Compose (for local PostgreSQL/Redis)
- Git

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd equilens-ai
```

### 2. Frontend setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your Supabase public keys
```

### 3. Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # or edit backend/.env directly
```

---

## Environment Setup

### Backend (`backend/.env`)

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | Yes (or uses SQLite fallback) |
| `SUPABASE_URL` | Your Supabase project URL | Optional |
| `SUPABASE_ANON_KEY` | Supabase publishable anon key | Optional |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (server-only) | Optional |
| `GEMINI_API_KEY` | Google Gemini API key | For live AI research |
| `GROQ_API_KEY` | Groq API key (fallback LLM) | Optional |
| `DHAN_CLIENT_ID` + `DHAN_ACCESS_TOKEN` | DhanHQ market data | For live prices |
| `MARKETAUX_API_TOKEN` | Marketaux financial news | For live news |
| `FMP_API_KEY` | Financial Modeling Prep | Optional fundamentals |
| `SECRET_KEY` | JWT signing secret (32+ chars) | Yes — change in production |
| `DATA_MODE` | `demo` or `live` | Default: `demo` |

### Supabase PostgreSQL (recommended)

Your Supabase project is: `db.ceedxgiuppobapaypxnb.supabase.co`

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.ceedxgiuppobapaypxnb.supabase.co:5432/postgres
SUPABASE_URL=https://ceedxgiuppobapaypxnb.supabase.co
```

Get your API keys from: [Supabase Dashboard → Settings → API](https://supabase.com/dashboard/project/ceedxgiuppobapaypxnb/settings/api)

### Frontend (`frontend/.env.local`)

```env
VITE_SUPABASE_URL=https://ceedxgiuppobapaypxnb.supabase.co
VITE_SUPABASE_ANON_KEY=<your-anon-key>
```

> Only the `anon` key goes in the frontend. Never put `service_role` keys in frontend code.

---

## Running the Application

### Backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

API available at: `http://localhost:8000`
Interactive docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm run dev
```

App available at: `http://localhost:5173`

The Vite dev server automatically proxies `/api/*` requests to `http://localhost:8000`.

---

## Database Setup

### Option A: Supabase (recommended)

1. Set `DATABASE_URL` in `backend/.env` with your Supabase connection string.
2. Run migrations:

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

3. Enable pgvector in Supabase SQL Editor:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Option B: Local Docker PostgreSQL

```bash
# Start PostgreSQL + Redis
docker compose up -d postgres redis

# Run migrations
cd backend
source .venv/bin/activate
DATABASE_URL=postgresql://postgres:equilens_local_dev@localhost:5432/equilens_ai alembic upgrade head
```

### Demo Mode (no database required)

Leave `DATABASE_URL` empty. The backend automatically falls back to a local SQLite database and seeds it with 5 Indian equity companies (RELIANCE, TCS, HDFCBANK, INFY, LT) with verified financial data, corporate actions, market events, and document chunks for RAG.

> **Demo data is clearly labelled throughout the UI and API responses. It does not represent real-time market prices or investment advice.**

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/health` | Backend status + DB connectivity |
| GET | `/api/v1/health/engines` | All engine statuses (DB, embeddings, LLM, RAG) |
| GET | `/api/v1/companies` | List companies (filters: exchange, sector, search) |
| GET | `/api/v1/companies/{id}` | Company detail |
| GET | `/api/v1/companies/search?q=` | Company search |
| GET | `/api/v1/companies/{id}/financials` | Financial metrics |
| GET | `/api/v1/companies/{id}/ratios` | Computed financial ratios |
| GET | `/api/v1/companies/{id}/forecasts` | Revenue/EPS forecasts |
| POST | `/api/v1/companies/{id}/forecasts/generate` | Generate new forecast |
| POST | `/api/v1/companies/compare` | Peer comparison |
| POST | `/api/v1/documents/upload` | Upload financial document |
| GET | `/api/v1/documents` | List uploaded documents |
| POST | `/api/v1/documents/{id}/process` | Trigger RAG ingestion |
| POST | `/api/v1/research/chat` | AI research chat (RAG) |
| GET | `/api/v1/research/sessions` | Research session history |
| GET | `/api/v1/news` | Financial news feed |
| GET | `/api/v1/corporate-actions` | Corporate actions |
| GET | `/api/v1/market-events` | Market events and deals |
| GET | `/api/v1/watchlist` | User watchlist |
| POST | `/api/v1/watchlist` | Add to watchlist |

---

## Testing

```bash
cd backend
source .venv/bin/activate
python -m pytest tests/ -v
```

20 integration tests covering: health endpoints, company CRUD, document upload, RAG chat, forecasting, corporate actions, news, peer comparison, and watchlist.

---

## Deployment

### Frontend → Vercel

```bash
cd frontend
npm run build
# Deploy dist/ to Vercel, or connect the GitHub repo directly
```

Set environment variables in Vercel dashboard:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

### Backend → Render

1. Connect GitHub repo to Render.
2. Set root directory: `equilens-ai/backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2`
5. Add all backend environment variables in the Render dashboard.

---

## Pending Integrations (requires credentials)

| Integration | Purpose | Status |
|---|---|---|
| Google Gemini API | Live AI research responses | Add `GEMINI_API_KEY` |
| Groq API | Fallback LLM provider | Add `GROQ_API_KEY` |
| DhanHQ API | Live NSE/BSE market data | Add `DHAN_CLIENT_ID` + `DHAN_ACCESS_TOKEN` |
| Marketaux API | Live financial news | Add `MARKETAUX_API_TOKEN` |
| Financial Modeling Prep | Fundamentals data | Add `FMP_API_KEY` |
| Langfuse | LLM observability | Add `LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY` |
| Sentry | Error monitoring | Add `SENTRY_DSN` |

All integration adapters are implemented and ready. They activate automatically when valid credentials are provided.

---

## Security Notes

- Never commit `.env` files or real API credentials.
- `SUPABASE_SERVICE_ROLE_KEY` is server-only — never expose it in the frontend.
- `SECRET_KEY` must be changed to a random 32+ character string in production.
- Document uploads are validated for file type and size before processing.
- The AI research engine cannot execute arbitrary SQL or code extracted from documents.
- Row-Level Security (RLS) policies are documented in `database/migrations/`.

---

## License

See `LICENSE`.
