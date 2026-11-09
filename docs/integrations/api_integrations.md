# ALPHANEXUS – External API Integrations

ALPHANEXUS integrates with high-reliability external financial and AI providers:

| Provider | Purpose | Status | Config Keys |
|---|---|---|---|
| **Google Gemini** | Primary LLM inference (Gemini 1.5 Flash / Pro) | Production Ready | `GEMINI_API_KEY`, `GEMINI_MODEL` |
| **Groq** | Ultra-low latency fallback (LLaMA-3.3 70B) | Production Ready | `GROQ_API_KEY`, `GROQ_MODEL` |
| **DhanHQ** | Live NSE / BSE market quotes and order book data | Configured | `DHAN_CLIENT_ID`, `DHAN_ACCESS_TOKEN` |
| **Marketaux** | Real-time financial news stream | Configured | `MARKETAUX_API_TOKEN` |
| **FMP** | Fundamentals and balance sheet history | Configured | `FMP_API_KEY` |
| **MongoDB Atlas** | Document and Atlas Vector Search database | Connected | `DATABASE_URL` / `MONGODB_URI` |
| **Supabase** | Relational data & pgvector embeddings | Connected | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |
