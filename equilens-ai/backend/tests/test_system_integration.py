import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.company import Company
from app.models.document import Document
from app.engines.rag.service import rag_service

client = TestClient(app)


def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "EquiLens AI"
    assert data["tagline"] == "See Beyond the Stock Price."


def test_health_and_engines_endpoints():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] in ["Healthy", "Degraded"]

    engines_res = client.get("/api/v1/health/engines")
    assert engines_res.status_code == 200
    data = engines_res.json()
    assert data["total_engines"] >= 10
    assert "rag" in data["engines"]


def test_companies_listing_and_detail():
    res = client.get("/api/v1/companies")
    assert res.status_code == 200
    comps = res.json()
    assert len(comps) > 0
    symbols = [c["symbol"] for c in comps]
    assert "RELIANCE" in symbols or "TCS" in symbols

    # Search endpoint
    search_res = client.get("/api/v1/companies/search?q=TCS")
    assert search_res.status_code == 200
    assert len(search_res.json()) > 0

    # Detail endpoint
    detail_res = client.get(f"/api/v1/companies/RELIANCE")
    assert detail_res.status_code == 200
    assert detail_res.json()["symbol"] == "RELIANCE"


def test_rag_end_to_end_research_chat():
    db = SessionLocal()
    try:
        comp = db.query(Company).filter(Company.symbol == "RELIANCE").first()
        assert comp is not None

        # Execute chat research
        chat_payload = {
            "company_id": str(comp.id),
            "query": "What are the consolidated revenues and EBITDA for Reliance in FY24?",
        }
        res = client.post("/api/v1/research/chat", json=chat_payload)
        assert res.status_code == 200
        data = res.json()
        assert data["role"] == "assistant"
        assert len(data["content"]) > 0
        assert len(data["citations"]) > 0
        # Ensure citations point to exact pages
        cit = data["citations"][0]
        assert "document_title" in cit
        assert cit["confidence_score"] > 0
    finally:
        db.close()

