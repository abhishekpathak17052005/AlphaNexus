from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, UUID4, ConfigDict


class CorporateActionResponse(BaseModel):
    id: UUID4
    company_id: UUID4
    action_type: str
    details: str
    ratio_or_amount: Optional[str] = None
    announcement_date: Optional[date] = None
    ex_date: Optional[date] = None
    record_date: Optional[date] = None
    payment_date: Optional[date] = None
    status: str
    source: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

