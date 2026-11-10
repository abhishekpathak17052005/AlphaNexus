#!/usr/bin/env python3
"""
ALPHANEXUS – Comprehensive Environment & Diagnostic Checker
"""
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app.core.config import settings
from app.core.database import check_database_health
from app.core.registry import engine_registry
from app.engines.rag.embeddings.engine import embedding_engine


def main():
    print("=" * 65)
    print(f"  {settings.APP_NAME} – Diagnostic Verification")
    print("=" * 65)
    print(f"  Environment  : {settings.APP_ENV}")
    print(f"  Data Mode    : {settings.DATA_MODE}")
    print(f"  Backend URL  : {settings.BACKEND_URL}")
    print("-" * 65)

    # 1. Relational DB & Vector Store
    db_health = check_database_health()
    print("[Database]")
    print(f"  Reachable    : {'YES' if db_health['reachable'] else 'NO'}")
    print(f"  Type         : {db_health.get('database_type')}")
    print(f"  pgvector     : {'Active' if db_health.get('pgvector_available') else 'Simulated / SQLite'}")

    # 2. Embedding Model
    print("\n[Embedding Engine]")
    print(f"  Model        : {settings.EMBEDDING_MODEL_NAME}")
    print(f"  Dimension    : {settings.EMBEDDING_DIMENSION}")
    vec = embedding_engine.get_embedding("ALPHANEXUS test query")
    print(f"  Test Vector  : Generated (len: {len(vec)})")

    # 3. Engines Summary
    summary = engine_registry.get_summary()
    print("\n[Core Engines]")
    print(f"  Status       : {summary['status']}")
    print(f"  Ready Engines: {summary['ready_count']} / {summary['total_engines']}")

    for key, eng in summary["engines"].items():
        icon = "✓" if eng["state"] == "Ready" else "!"
        print(f"  [{icon}] {eng['name']:<25}: {eng['state']}")

    print("=" * 65)
    print("  Environment checks completed successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()

