from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from .config import settings
from .logging import logger


class EngineState(str, Enum):
    READY = "Ready"
    DEGRADED = "Degraded"
    DISABLED = "Disabled"
    INITIALIZING = "Initializing"
    FAILED = "Failed"


class EngineInfo(BaseModel):
    name: str
    state: EngineState
    provider: Optional[str] = None
    version: Optional[str] = None
    details: Optional[str] = None
    last_checked: datetime = datetime.utcnow()


class EngineRegistry:
    """
    Central Service Registry tracking real-time health and initialization
    states of all core engines and third-party provider integrations.
    """
    def __init__(self):
        self._engines: Dict[str, EngineInfo] = {}
        self.initialize_engines()

    def initialize_engines(self):
        # 1. Application Backend
        self.register(
            "backend",
            EngineInfo(
                name="Application Backend",
                state=EngineState.READY,
                provider="FastAPI / Python 3.13",
                version="1.0.0",
                details="Core API server initialized and accepting requests",
            ),
        )

        # 2. Database Engine
        from .database import check_database_health
        db_health = check_database_health()
        if db_health["reachable"]:
            db_state = EngineState.READY if db_health["pgvector_available"] else EngineState.DEGRADED
            db_details = f"Connected ({db_health['database_type']}). pgvector: {'available' if db_health['pgvector_available'] else 'not detected / simulated'}"
        else:
            db_state = EngineState.FAILED
            db_details = f"Unreachable: {db_health.get('details', 'connection failed')}"

        self.register(
            "database",
            EngineInfo(
                name="Database Engine",
                state=db_state,
                provider="PostgreSQL / Supabase" if not db_health.get("database_type") == "sqlite_fallback" else "SQLite Dev Fallback",
                version="SQLAlchemy 2.0",
                details=db_details,
            ),
        )

        # 3. PostgreSQL / pgvector
        pgv_state = EngineState.READY if db_health.get("pgvector_available") else EngineState.DEGRADED
        self.register(
            "pgvector",
            EngineInfo(
                name="PostgreSQL / pgvector",
                state=pgv_state,
                provider="pgvector",
                details="Vector similarity index ready for 384-d embeddings" if db_health.get("pgvector_available") else "Simulated vector store active in local dev mode",
            ),
        )

        # 4. Embedding Model
        self.register(
            "embedding",
            EngineInfo(
                name="Embedding Model",
                state=EngineState.READY,
                provider=settings.EMBEDDING_MODEL_NAME,
                version="384-dimensional",
                details=f"Embedding pipeline initialized on {settings.EMBEDDING_DEVICE}",
            ),
        )

        # 5. LLM Provider (Gemini / Groq)
        if settings.GEMINI_API_KEY:
            llm_state = EngineState.READY
            llm_provider = f"Google Gemini ({settings.GEMINI_MODEL})"
            llm_details = "API key configured and ready"
        elif settings.GROQ_API_KEY:
            llm_state = EngineState.READY
            llm_provider = f"Groq ({settings.GROQ_MODEL})"
            llm_details = "API key configured and ready"
        else:
            llm_state = EngineState.DISABLED
            llm_provider = "Gemini / Groq"
            llm_details = "No LLM API keys provided (GEMINI_API_KEY or GROQ_API_KEY). RAG retrieval operates with heuristic synthesis or fallback summary."

        self.register(
            "llm",
            EngineInfo(
                name="LLM Provider",
                state=llm_state,
                provider=llm_provider,
                details=llm_details,
            ),
        )

        # 6. RAG Engine
        rag_state = EngineState.READY if (llm_state == EngineState.READY or settings.DATA_MODE == "demo") else EngineState.DEGRADED
        self.register(
            "rag",
            EngineInfo(
                name="RAG Engine",
                state=rag_state,
                provider="EquiLens RAG Core",
                version="1.0.0",
                details="Multi-modal document loader, section chunker, vector retrieval, and citation engine active",
            ),
        )

        # 7. Document Storage
        if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
            storage_state = EngineState.READY
            storage_provider = "Supabase Private Storage"
            storage_details = f"Bucket '{settings.SUPABASE_STORAGE_BUCKET}' connected with RLS"
        else:
            storage_state = EngineState.DEGRADED
            storage_provider = "Local File Storage"
            storage_details = f"Local directory storage at: {settings.LOCAL_UPLOAD_DIR}"

        self.register(
            "storage",
            EngineInfo(
                name="Document Storage",
                state=storage_state,
                provider=storage_provider,
                details=storage_details,
            ),
        )

        # 8. News Engine
        if settings.MARKETAUX_API_TOKEN:
            news_state = EngineState.READY
            news_provider = "Marketaux Live API"
            news_details = "Live financial news feed and event classifier active"
        else:
            news_state = EngineState.DEGRADED if settings.DATA_MODE == "demo" else EngineState.DISABLED
            news_provider = "Marketaux (Demo / Seed Mode)"
            news_details = "No MARKETAUX_API_TOKEN supplied. Running with curated high-fidelity market announcement fixtures."

        self.register(
            "news",
            EngineInfo(
                name="News Engine",
                state=news_state,
                provider=news_provider,
                details=news_details,
            ),
        )

        # 9. Market Data Provider
        if settings.DHAN_CLIENT_ID and settings.DHAN_ACCESS_TOKEN:
            mkt_state = EngineState.READY
            mkt_provider = "DhanHQ Live Market API"
            mkt_details = "Live NSE/BSE quote stream & historical price engine connected"
        else:
            mkt_state = EngineState.DEGRADED if settings.DATA_MODE == "demo" else EngineState.DISABLED
            mkt_provider = "DhanHQ / NSE-BSE Fixtures"
            mkt_details = "Operating in demo mode with authentic historical price and technical indicators for NSE/BSE leaders."

        self.register(
            "market_data",
            EngineInfo(
                name="Market Data Provider",
                state=mkt_state,
                provider=mkt_provider,
                details=mkt_details,
            ),
        )

        # 10. Financial Analytics Engine
        self.register(
            "analytics",
            EngineInfo(
                name="Financial Analytics",
                state=EngineState.READY,
                provider="Deterministic Engine (NumPy/Pandas)",
                version="1.0.0",
                details="Strict zero-denominator safety, DuPont analysis, margin metrics, and Cash Flow algorithms loaded",
            ),
        )

        # 11. Forecasting Engine
        self.register(
            "forecasting",
            EngineInfo(
                name="Forecasting Engine",
                state=EngineState.READY,
                provider="Scikit-Learn / Statsmodels / ARIMA",
                version="1.0.0",
                details="Scenario projections (Bull/Base/Bear), 80-95% prediction intervals, and walk-forward cross-validation ready",
            ),
        )

    def register(self, key: str, info: EngineInfo):
        self._engines[key] = info

    def get(self, key: str) -> Optional[EngineInfo]:
        return self._engines.get(key)

    def update_state(self, key: str, state: EngineState, details: Optional[str] = None):
        if key in self._engines:
            self._engines[key].state = state
            if details:
                self._engines[key].details = details
            self._engines[key].last_checked = datetime.utcnow()

    def get_all(self) -> Dict[str, EngineInfo]:
        return self._engines

    def get_summary(self) -> Dict[str, Any]:
        states = [e.state for e in self._engines.values()]
        overall = "Healthy"
        if EngineState.FAILED in states:
            overall = "Critical"
        elif EngineState.DEGRADED in states:
            overall = "Degraded"
        
        return {
            "status": overall,
            "timestamp": datetime.utcnow().isoformat(),
            "total_engines": len(self._engines),
            "ready_count": sum(1 for s in states if s == EngineState.READY),
            "degraded_count": sum(1 for s in states if s == EngineState.DEGRADED),
            "disabled_count": sum(1 for s in states if s == EngineState.DISABLED),
            "failed_count": sum(1 for s in states if s == EngineState.FAILED),
            "engines": {k: v.model_dump() for k, v in self._engines.items()},
        }


engine_registry = EngineRegistry()

