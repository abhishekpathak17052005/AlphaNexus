from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, UUID4, ConfigDict


class MarketEventResponse(BaseModel):
    id: UUID4
    company_id: UUID4
    event_type: str
    title: str
    description: str
    deal_value: Optional[float] = None
    deal_currency: str = "INR"
    counterparty: Optional[str] = None
    strategic_implications: Optional[str] = None
    disclosed_date: date
    source_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

