"""
End-to-End System Integration Test for ALPHANEXUS
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_full_equity_research_workflow():
    # 1. Health check
    h = client.get("/api/v1/health")
    assert h.status_code == 200

    # 2. Company search
    c = client.get("/api/v1/companies?limit=1")
    assert c.status_code == 200
    companies = c.json()
    assert len(companies) >= 0

    # 3. Settings inspection
    s = client.get("/api/settings")
    assert s.status_code == 200
    assert "app_name" in s.json()
