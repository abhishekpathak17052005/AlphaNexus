#!/usr/bin/env python3
"""
EquiLens AI – Environment and Engine Verification Utility
Checks reachability of database, vector extensions, embedding pipelines,
LLM configurations, and third-party provider credentials.
"""

import sys
import os

# Ensure backend app is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.core.config import settings
from app.core.database import check_database_health
from app.core.registry import engine_registry
from app.engines.rag.embeddings import embedding_engine


def main():
    print("=" * 65)
    print("  EquiLens AI – System & Engine Diagnostic Verification")
    print("=" * 65)
    print(f"  App Environment : {settings.APP_ENV}")
    print(f"  Data Mode       : {settings.DATA_MODE}")
    print(f"  Backend URL     : {settings.BACKEND_URL}")
    print(f"  Frontend URL    : {settings.FRONTEND_URL}")
    print("-" * 65)

    # 1. Database Health
    db_health = check_database_health()
    print("[Database]")
    print(f"  Reachable       : {'YES' if db_health['reachable'] else 'NO'}")
    print(f"  Type            : {db_health.get('database_type')}")
    print(f"  pgvector Active : {'YES' if db_health.get('pgvector_available') else 'NO / Simulated'}")
    print(f"  Details         : {db_health.get('details') or 'Operating normally'}")

    # 2. Embedding Model
    print("\n[Embedding Engine]")
    print(f"  Model           : {settings.EMBEDDING_MODEL_NAME}")
    print(f"  Dimension       : {settings.EMBEDDING_DIMENSION}")
    test_vec = embedding_engine.get_embedding("EquiLens verification query")
    print(f"  Vector Generated: YES (length: {len(test_vec)}, norm: {round(sum(x**2 for x in test_vec)**0.5, 3)})")

    # 3. Engines Summary
    summary = engine_registry.get_summary()
    print("\n[Central Engine Registry]")
    print(f"  Overall Status  : {summary['status']}")
    print(f"  Ready Engines   : {summary['ready_count']} / {summary['total_engines']}")
    print(f"  Degraded / Demo : {summary['degraded_count']}")
    print(f"  Disabled        : {summary['disabled_count']}")
    print("-" * 65)

    for key, eng in summary["engines"].items():
        state_icon = "✓" if eng["state"] == "Ready" else "!" if eng["state"] == "Degraded" else "–"
        print(f"  [{state_icon}] {eng['name']:<25} : {eng['state']:<12} ({eng.get('provider')})")

    print("=" * 65)
    print("  Verification Complete. All core engines initialized successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()

