#!/usr/bin/env python3
"""
ALPHANEXUS – Microservice & Engine Health Checker
"""
import sys
import os
import httpx

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def main():
    print(f"[ALPHANEXUS] Running health probe against {BACKEND_URL}...")
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{BACKEND_URL}/api/v1/health")
            if resp.status_code == 200:
                print(f"  [OK] Backend API is operational: {resp.json()}")
            else:
                print(f"  [WARNING] Received status code {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"  [OFFLINE] Could not connect to backend at {BACKEND_URL}: {e}")


if __name__ == "__main__":
    main()

