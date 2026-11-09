"""
ALPHANEXUS – Pytest Fixtures and Global Configuration
======================================================
Provides test database sessions, mocked LLM responses, and sample financial payloads.
"""

import sys
import os
import pytest

# Ensure backend app is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.core.config import settings
from app.core.database import SessionLocal, Base, engine


@pytest.fixture(scope="session")
def test_db():
    """Create test tables and yield session."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_financial_metrics():
    """Standardized financial balance sheet and income items."""
    return {
        "revenue": 100000000.0,
        "net_income": 15000000.0,
        "operating_income": 20000000.0,
        "total_assets": 120000000.0,
        "total_equity": 60000000.0,
        "total_debt": 30000000.0,
        "cash_flow_operating": 22000000.0,
        "capex": 5000000.0,
    }


@pytest.fixture
def sample_query():
    return "What was the operating profit margin of Reliance Industries in FY24?"
