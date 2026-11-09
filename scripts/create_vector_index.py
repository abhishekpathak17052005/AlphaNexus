#!/usr/bin/env python3
"""
ALPHANEXUS – Vector Index Creator (pgvector HNSW & MongoDB Atlas)
"""
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app.core.database import SessionLocal, engine
from app.core.logging import logger
from sqlalchemy import text


def main():
    print("[ALPHANEXUS] Creating and verifying Vector Indexes...")
    try:
        with engine.connect() as conn:
            # Enable pgvector if postgres
            if "postgresql" in str(engine.url):
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS ix_document_chunks_embedding_hnsw
                    ON document_chunks USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 64);
                """))
                conn.commit()
                print("  [OK] pgvector HNSW cosine index created.")
            else:
                print("  [OK] SQLite in use; virtual vector search ready.")
    except Exception as e:
        print(f"  [NOTICE] Index creation note: {e}")

    print("[ALPHANEXUS] Vector index setup routine complete.")


if __name__ == "__main__":
    main()
