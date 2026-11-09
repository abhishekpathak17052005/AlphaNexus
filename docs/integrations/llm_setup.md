# ALPHANEXUS – LLM Provider Setup Guide

## 1. Google Gemini (Primary)

- **Default Model:** `gemini-1.5-flash`
- **Alternative:** `gemini-1.5-pro` (higher context window & reasoning capability)
- **Configuration:** Set `GEMINI_API_KEY` in `.env`.

---

## 2. Groq (High-Speed Fallback)

- **Default Model:** `llama-3.3-70b-versatile`
- **Configuration:** Set `GROQ_API_KEY` in `.env`.
- When Gemini encounters rate limits (HTTP 429), the LLM adapter seamlessly switches to Groq to guarantee uninterrupted analyst workflows.
