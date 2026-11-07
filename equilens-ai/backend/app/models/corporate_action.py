import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Text, ForeignKey, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class CorporateAction(Base):
    __tablename__ = "corporate_actions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(50), nullable=False, index=True)  # Dividend, Bonus, Stock Split, Rights Issue, Buyback, Merger
    details = Column(Text, nullable=False)
    ratio_or_amount = Column(String(50), nullable=True)  # e.g., "₹10 per share", "1:1", "1:5"
    announcement_date = Column(Date, nullable=True)
    ex_date = Column(Date, nullable=True, index=True)
    record_date = Column(Date, nullable=True)
    payment_date = Column(Date, nullable=True)
    status = Column(String(30), default="Announced")  # Announced, Executed, Cancelled
    source = Column(String(100), default="NSE_EXCHANGE")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="corporate_actions")

    __table_args__ = (
        Index("idx_corp_action_company_exdate", "company_id", "ex_date"),
    )

