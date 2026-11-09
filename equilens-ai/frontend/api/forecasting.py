"""
EquiLens AI – Performance Forecasting API Module
================================================
Fetches and triggers multi-period econometric forecast simulations.
"""

from typing import Any, Dict, Optional
from api.client import api_client


def get_forecasts(company_id: str) -> Optional[Dict[str, Any]]:
    res = api_client.get(f"companies/{company_id}/forecasts")
    if isinstance(res, dict) and "error" not in res:
        return res
    return None


def generate_forecast(
    company_id: str,
    target_metric: str = "revenue",
    horizon_periods: int = 4,
    model_type: str = "ensemble",
) -> Optional[Dict[str, Any]]:
    payload = {
        "target_metric": target_metric,
        "horizon_periods": horizon_periods,
        "model_type": model_type,
    }
    res = api_client.post(f"companies/{company_id}/forecasts/generate", json_data=payload)
    if isinstance(res, dict) and "error" not in res:
        return res
    return None

