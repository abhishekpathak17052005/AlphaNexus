"""
Pytest configuration and shared fixtures for EquiLens AI backend tests.

The main concern: tests need the SQLite database to be created and seeded
before any test runs. We achieve this by running the FastAPI lifespan once
at session start using TestClient as a context manager.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.services.seed_service import seed_initial_market_data


@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    """
    Session-scoped fixture that:
    1. Creates all SQLAlchemy tables in the test SQLite database.
    2. Seeds demo market data (companies, financials, documents, etc.)
       so integration tests have data to work with.
    Runs once before any test in the session.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed data
    db = SessionLocal()
    try:
        seed_initial_market_data(db)
    except Exception as e:
        # Non-fatal: data may already exist from a previous run
        pass
    finally:
        db.close()

    yield

    # Teardown (optional): drop tables after full test session
    # Base.metadata.drop_all(bind=engine)
