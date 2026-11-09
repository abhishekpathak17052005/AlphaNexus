import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Text, Numeric, ForeignKey, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class MarketEvent(Base):
    __tablename__ = "market_events"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)  # Major Contract, Order Win, Acquisition, Joint Venture, Capex, Regulatory
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    deal_value = Column(Numeric(18, 2), nullable=True)  # in specified currency
    deal_currency = Column(String(10), default="INR")
    counterparty = Column(String(255), nullable=True)
    strategic_implications = Column(Text, nullable=True)
    disclosed_date = Column(Date, nullable=False, index=True)
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="market_events")

    __table_args__ = (
        Index("idx_event_company_date", "company_id", "disclosed_date"),
    )

