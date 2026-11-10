# ALPHANEXUS – Installation Guide

## 1. Prerequisites
- Python 3.10+ (Python 3.11 or 3.12 recommended)
- PostgreSQL with `pgvector` extension OR SQLite (for local zero-setup dev)
- MongoDB Atlas account (optional for vector search)

---

## 2. Step-by-Step Setup

```bash
# 1. Clone repository & navigate to root
cd AlphaNexus

# 2. Set up virtual environment
python3 -m venv backend/.venv
source backend/.venv/bin/activate

# 3. Install core dependencies
pip install -r requirements.txt

# 4. Copy and configure environment variables
cp .env.example .env

# 5. Initialize directories and database
python scripts/setup.py
python scripts/initialize_database.py

# 6. Verify environment & engines
python scripts/check_environment.py
```

---

## 3. Running the Stack

```bash
# Terminal 1: Start Backend API
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Streamlit Frontend
streamlit run frontend/streamlit_app.py --server.port 8501
```

