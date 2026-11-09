from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, UUID4, ConfigDict


class CompanyBase(BaseModel):
    symbol: str
    name: str
    exchange: str = "NSE"
    isin: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    current_price: Optional[float] = None
    day_change: Optional[float] = None
    day_change_percent: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe: Optional[float] = None
    roce: Optional[float] = None
    dividend_yield: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    currency: str = "INR"
    description: Optional[str] = None
    website: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: UUID4
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanyDetailResponse(CompanyResponse):
    pass

