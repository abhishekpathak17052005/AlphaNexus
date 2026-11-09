# ALPHANEXUS – Financial RAG Engine

## 1. Overview

The **Financial RAG Engine** is tailored specifically for financial document intelligence, quarterly earnings releases, investor presentations, and annual reports.

---

## 2. Pipeline Components

1. **Document Loaders (`loaders/`):**
   - PDF, DOCX, XLSX, and CSV loaders.
   - Extracts tabular data preserving row/column alignment.

2. **Chunking Engine (`chunking/`):**
   - Recursive character splitting with financial delimiter awareness.
   - Table chunking preserves Markdown table structures with headers retained across chunk boundaries.

3. **Embedding Engine (`embeddings/`):**
   - Default model: `BAAI/bge-base-en-v1.5` (768 dimensions).
   - Lightweight alternative: `BAAI/bge-small-en-v1.5` (384 dimensions).
   - Query prefix instruction: `"Represent this sentence for searching relevant passages: "`.
   - L2 normalisation enables high-speed cosine distance calculations.

4. **Vector Stores (`vector_store/`):**
   - Dual-store support: PostgreSQL (`pgvector`) with HNSW index and MongoDB Atlas Vector Search.

5. **Cross-Encoder Reranker (`rerankers/`):**
   - Uses `BAAI/bge-reranker-base` to rerank top candidates before context assembly.

6. **Source Attribution & Citations (`citations/`):**
   - Every generated sentence is mapped back to the origin document chunk, page number, and similarity score.
