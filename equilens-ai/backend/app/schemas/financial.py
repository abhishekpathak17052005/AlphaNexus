from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, UUID4, ConfigDict


class FinancialMetricResponse(BaseModel):
    id: UUID4
    company_id: UUID4
    metric_name: str
    metric_category: str
    period_type: str
    financial_year: str
    quarter: Optional[str] = None
    period_end_date: date
    value: float
    unit: str
    currency: str
    yoy_growth: Optional[float] = None
    qoq_growth: Optional[float] = None
    is_consolidated: bool

    model_config = ConfigDict(from_attributes=True)


class FinancialStatementResponse(BaseModel):
    id: UUID4
    company_id: UUID4
    statement_type: str
    period_type: str
    financial_year: str
    quarter: Optional[str] = None
    period_end_date: date
    is_consolidated: bool
    currency: str
    unit: str
    raw_data: Dict[str, Any]
    is_audited: bool

    model_config = ConfigDict(from_attributes=True)


class RatiosResponse(BaseModel):
    company_symbol: str
    computed_metrics: Dict[str, Any]


class PeerCompareRequest(BaseModel):
    company_ids: List[str]


class PeerCompareResponse(BaseModel):
    peer_count: int
    benchmarks: Dict[str, Any]
    peers: List[Dict[str, Any]]

