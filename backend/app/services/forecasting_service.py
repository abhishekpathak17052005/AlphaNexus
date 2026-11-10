"""
ALPHANEXUS – Forecasting Application Service
============================================
Delegates model training and scenario simulation requests to the ForecastingEngine.
"""

from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.engines.forecasting.service import forecasting_service


class ForecastingAppService:

    @staticmethod
    def get_or_generate_forecast(
        db: Session,
        company_id: UUID,
        target_metric: str = "revenue",
        horizon_periods: int = 4,
        model_type: str = "ensemble",
        force_recalculate: bool = False,
    ) -> Dict[str, Any]:
        return forecasting_service.generate_company_forecast(
            db=db,
            company_id=company_id,
            target_metric=target_metric,
            horizon_periods=horizon_periods,
            model_type=model_type,
            force_recalculate=force_recalculate,
        )


forecasting_app_service = ForecastingAppService()

