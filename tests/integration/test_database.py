"""
Integration tests for Database Connection and Repositories
"""
import pytest
from app.core.database import check_database_health
from app.database.mongodb import mongodb_manager


def test_database_connectivity():
    health = check_database_health()
    assert "reachable" in health
    assert health["reachable"] is True


def test_mongodb_instance():
    assert mongodb_manager is not None
