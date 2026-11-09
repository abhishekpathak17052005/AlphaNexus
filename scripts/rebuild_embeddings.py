#!/usr/bin/env python3
"""
ALPHANEXUS – Dense Embeddings Rebuilder
"""
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app.core.database import SessionLocal
from app.models.document import DocumentChunk
from app.engines.rag.embeddings.engine import embedding_engine
from app.core.logging import logger


def main():
    print("[ALPHANEXUS] Scanning database for un-embedded chunks...")
    db = SessionLocal()
    try:
        chunks = db.query(DocumentChunk).filter(DocumentChunk.embedding == None).limit(500).all()
        print(f"  Found {len(chunks)} chunks needing embeddings.")
        for chunk in chunks:
            chunk.embedding = embedding_engine.get_embedding(chunk.content)
        if chunks:
            db.commit()
            print(f"  [OK] Successfully rebuilt embeddings for {len(chunks)} chunks.")
        else:
            print("  [OK] All existing document chunks are up to date.")
    except Exception as e:
        print(f"  [NOTICE] Rebuild notice: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
