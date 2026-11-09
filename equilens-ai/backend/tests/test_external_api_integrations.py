import pytest
from app.core.config import settings
from app.core.database import SessionLocal, check_database_health
from app.engines.providers.gemini import GeminiProvider
from app.engines.providers.groq import GroqProvider
from app.engines.providers.marketaux import MarketauxProvider
from app.engines.providers.dhan import DhanHQProvider
from app.engines.providers.fmp import FMPProvider
from app.services.audit_service import run_integrations_audit


@pytest.mark.external_api
def test_supabase_postgresql_and_pgvector():
    """Validates real PostgreSQL connectivity and pgvector extension on Supabase."""
    health = check_database_health()
    assert health["reachable"] is True
    assert health["configured"] is True
    assert health["database_type"] == "postgresql"
    assert health["pgvector_available"] is True


@pytest.mark.external_api
def test_gemini_api_inference():
    """Validates real Google Gemini API generation and token usage."""
    if not settings.GEMINI_API_KEY:
        pytest.skip("GEMINI_API_KEY not configured")
    provider = GeminiProvider()
    response = provider.generate("Say: EquiLens Gemini Test OK")
    assert response.is_live is True
    assert len(response.content) > 0
    assert response.tokens_used > 0
    assert response.error is None


@pytest.mark.external_api
def test_groq_api_inference():
    """Validates real Groq API high-speed chat completion."""
    if not settings.GROQ_API_KEY:
        pytest.skip("GROQ_API_KEY not configured")
    provider = GroqProvider()
    response = provider.generate("Say: EquiLens Groq Test OK")
    assert response.is_live is True
    assert len(response.content) > 0
    assert response.tokens_used > 0
    assert response.error is None


@pytest.mark.external_api
def test_marketaux_news_api():
    """Validates Marketaux financial news retrieval with authentic API token."""
    if not settings.MARKETAUX_API_TOKEN:
        pytest.skip("MARKETAUX_API_TOKEN not configured")
    provider = MarketauxProvider()
    assert provider.is_configured is True
    status = provider.check_availability()
    assert status["available"] is True
    assert status["status"] == "Ready"


@pytest.mark.external_api
def test_dhanhq_authentication_and_limits():
    """Validates DhanHQ client authentication and endpoint entitlement."""
    if not settings.DHAN_CLIENT_ID or not settings.DHAN_ACCESS_TOKEN:
        pytest.skip("DhanHQ credentials not configured")
    provider = DhanHQProvider()
    assert provider.is_configured is True
    status = provider.check_availability()
    assert status["available"] is True
    assert status["status"] == "Ready"


@pytest.mark.external_api
def test_fmp_global_and_tier_limits():
    """Validates FMP profile retrieval and handles Indian equities plan limitations."""
    if not settings.FMP_API_KEY:
        pytest.skip("FMP_API_KEY not configured")
    provider = FMPProvider()
    res = provider.get_company_profile("AAPL")
    assert res["is_live"] is True
    assert res["symbol"] == "AAPL"
    assert "companyName" in res["data"]


@pytest.mark.external_api
def test_integrations_audit_service_aggregate():
    """Validates the complete administrative integration audit aggregate."""
    audit = run_integrations_audit()
    assert audit["total_integrations"] >= 8
    assert audit["connected_count"] >= 5
    assert audit["failed_count"] == 0
    for item in audit["integrations"]:
        assert "provider" in item
        assert "status" in item
        assert item["status"] in ("Connected", "Degraded", "Failed", "Not Configured")
