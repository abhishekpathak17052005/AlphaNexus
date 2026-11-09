#!/usr/bin/env python3
"""
ALPHANEXUS – Environment Setup & Workspace Initializer
"""
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DIRS_TO_CREATE = [
    "logs",
    "data/uploads",
    "data/processed",
    "data/datasets",
    "data/cache",
    "data/sample_documents",
    "models/embeddings",
    "models/forecasting",
]


def main():
    print("[ALPHANEXUS] Initializing project workspace directories...")
    for d in DIRS_TO_CREATE:
        path = os.path.join(BASE_DIR, d)
        os.makedirs(path, exist_ok=True)
        print(f"  [OK] Directory ready: {d}")

    env_path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(env_path):
        example_path = os.path.join(BASE_DIR, ".env.example")
        if os.path.exists(example_path):
            print("  [NOTICE] .env not found. Please copy .env.example to .env and configure secrets.")
    else:
        print("  [OK] .env configuration file detected.")

    print("[ALPHANEXUS] Workspace setup complete.")


if __name__ == "__main__":
    main()
