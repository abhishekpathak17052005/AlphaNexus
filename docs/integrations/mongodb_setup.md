# ALPHANEXUS – MongoDB Atlas Vector Search Setup

## 1. Overview

MongoDB Atlas acts as the primary document database and vector similarity store for RAG document intelligence.

---

## 2. Atlas Vector Search Index Configuration

Create a vector search index on the `document_chunks` collection:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 768,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "company_id"
    },
    {
      "type": "filter",
      "path": "document_id"
    }
  ]
}
```

---

## 3. Environment Variable

```bash
MONGODB_URI="mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DATABASE="alphanexus"
```

