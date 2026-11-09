# ALPHANEXUS – Environment Variables Reference

| Variable | Description | Default / Example |
|---|---|---|
| `APP_NAME` | Name of the platform | `ALPHANEXUS` |
| `APP_ENV` | Application environment (`development` / `production`) | `development` |
| `DATABASE_URL` | SQLAlchemy PostgreSQL connection URL | `postgresql://user:pass@localhost:5432/alphanexus` |
| `MONGODB_URI` | MongoDB Atlas cluster connection URI | `mongodb+srv://...` |
| `GEMINI_API_KEY` | Google Gemini API Key | `AIzaSy...` |
| `GEMINI_MODEL` | Gemini inference model | `gemini-1.5-flash` |
| `GROQ_API_KEY` | Groq API Key | `gsk_...` |
| `GROQ_MODEL` | Groq LLaMA model | `llama-3.3-70b-versatile` |
| `EMBEDDING_MODEL_NAME` | Hugging Face dense embedding model | `BAAI/bge-base-en-v1.5` |
| `EMBEDDING_DIMENSION` | Vector embedding dimension | `768` |
| `DHAN_CLIENT_ID` | DhanHQ API client ID | `1000...` |
| `DHAN_ACCESS_TOKEN` | DhanHQ API access token | `eyJ...` |
| `MARKETAUX_API_TOKEN` | Marketaux API token | `...` |
| `FMP_API_KEY` | Financial Modeling Prep API token | `...` |
