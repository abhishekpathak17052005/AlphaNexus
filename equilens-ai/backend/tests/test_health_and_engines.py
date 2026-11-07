import pytest
from app.core.registry import engine_registry, EngineState
from app.core.database import check_database_health


def test_database_health_check():
    health = check_database_health()
    assert "reachable" in health
    assert "configured" in health
    assert health["reachable"] is True


def test_engine_registry_summary():
    summary = engine_registry.get_summary()
    assert "status" in summary
    assert "engines" in summary
    assert summary["total_engines"] >= 10

    # Ensure major engines are tracked
    assert "backend" in summary["engines"]
    assert "database" in summary["engines"]
    assert "rag" in summary["engines"]
    assert "analytics" in summary["engines"]
    assert "forecasting" in summary["engines"]

