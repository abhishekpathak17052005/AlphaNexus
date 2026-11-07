from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4, ConfigDict
from .company import CompanyResponse


class WatchlistAddRequest(BaseModel):
    company_id: str
    target_price: Optional[float] = None
    alert_threshold_percent: Optional[float] = None
    notes: Optional[str] = None


class WatchlistItemResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    company_id: UUID4
    target_price: Optional[float] = None
    alert_threshold_percent: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    company: Optional[CompanyResponse] = None

    model_config = ConfigDict(from_attributes=True)

