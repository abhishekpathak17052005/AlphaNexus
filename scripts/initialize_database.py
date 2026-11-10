#!/usr/bin/env python3
"""
ALPHANEXUS – Database Schema & Initial Data Seeder
"""
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

from app.core.database import Base, engine, SessionLocal
from app.services.seed_service import seed_initial_market_data


def main():
    print("[ALPHANEXUS] Verifying and applying database schemas...")
    Base.metadata.create_all(bind=engine)
    print("  [OK] Database tables verified.")

    print("[ALPHANEXUS] Checking seed data for Indian listed companies...")
    db = SessionLocal()
    try:
        seed_initial_market_data(db)
        print("  [OK] Seed data initialized.")
    finally:
        db.close()


if __name__ == "__main__":
    main()

