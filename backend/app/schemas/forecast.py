from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, UUID4, ConfigDict


class ForecastGenerateRequest(BaseModel):
    metric_name: str = "revenue"
    forecast_horizon_years: int = 3


class ForecastPeriodItem(BaseModel):
    period: str
    base: float
    bullish: float
    bearish: float
    confidence_intervals: Dict[str, Any]


class ForecastResponse(BaseModel):
    status: str
    company_id: str
    company_symbol: str
    metric_name: str
    historical: List[Dict[str, Any]]
    forecasts: List[ForecastPeriodItem]
    evaluation: Optional[Dict[str, Any]] = None
    disclaimer: str

