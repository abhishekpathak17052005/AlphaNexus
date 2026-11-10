"""
Integration tests for ALPHANEXUS FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Operational"


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_companies_list_endpoint():
    response = client.get("/api/v1/companies?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

