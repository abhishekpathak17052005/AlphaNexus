# ALPHANEXUS – Troubleshooting & Diagnostics

## 1. Database Connection Timeout
- **Symptom:** Remote Supabase / PostgreSQL database times out after 10 seconds.
- **Resolution:** ALPHANEXUS includes an automatic fallback to local SQLite (`database/equilens_dev.db`), allowing full offline development and testing.

## 2. Sentence Transformer Download Lag
- **Symptom:** First query or ingestion takes 10-15 seconds.
- **Explanation:** Hugging Face models are cached on first use in `~/.cache/huggingface/hub`. Subsequent calls load instantly from disk.

## 3. Port Collisions
- FastAPI defaults to port `8000`. If in use, start with `--port 8001` and update `BACKEND_URL` in `.env`.
- Streamlit defaults to port `8501`. Specify `--server.port 8502` if needed.

