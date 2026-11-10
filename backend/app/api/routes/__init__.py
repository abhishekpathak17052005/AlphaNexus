"""
ALPHANEXUS – API Routes Registry
"""
from fastapi import APIRouter
from . import (
    health,
    auth,
    companies,
    documents,
    rag,
    chat,
    financials,
    analytics,
    news,
    corporate_actions,
    forecasting,
    settings,
)

routes_router = APIRouter()
routes_router.include_router(health.router, tags=["Health"])
routes_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
routes_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
routes_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
routes_router.include_router(rag.router, prefix="/rag", tags=["RAG"])
routes_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
routes_router.include_router(financials.router, tags=["Financials"])
routes_router.include_router(analytics.router, tags=["Analytics"])
routes_router.include_router(news.router, prefix="/news", tags=["News"])
routes_router.include_router(corporate_actions.router, prefix="/corporate-actions", tags=["Corporate Actions"])
routes_router.include_router(forecasting.router, tags=["Forecasting"])
routes_router.include_router(settings.router, prefix="/settings", tags=["Settings"])

__all__ = ["routes_router"]

