from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db, check_database_health
from app.core.registry import engine_registry
from app.schemas.health import HealthResponse, EnginesSummaryResponse
from app.services.audit_service import run_integrations_audit

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health(db: Session = Depends(get_db)):
    """Basic health probe indicating backend server is operational."""
    db_status = check_database_health()
    return HealthResponse(
        status="Healthy" if db_status["reachable"] else "Degraded",
        environment=settings.APP_ENV,
        data_mode=settings.DATA_MODE,
        timestamp=datetime.utcnow(),
        database_connected=db_status["reachable"],
        version="1.0.0",
    )


@router.get("/health/engines", response_model=EnginesSummaryResponse)
def get_engines_health():
    """
    Central Engine Registry status dashboard.
    Returns the real-time health and initialization state of all core engines
    (Database, pgvector, Embeddings, LLM, RAG, News, Analytics, Forecasting).
    """
    return engine_registry.get_summary()


@router.get("/health/integrations")
def get_integrations_audit():
    """
    Real-Time Administrative Integration Audit Dashboard.
    Performs dynamic connectivity, authentication, and latency probes across all configured
    external API providers (Gemini, Groq, PostgreSQL, pgvector, DhanHQ, Marketaux, FMP, Langfuse, Sentry).
    Redacts all secrets, tokens, and authorization headers.
    """
    return run_integrations_audit()

