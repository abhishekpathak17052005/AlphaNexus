import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    target_price = Column(Numeric(12, 2), nullable=True)
    alert_threshold_percent = Column(Numeric(5, 2), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="watchlists")
    company = relationship("Company", back_populates="watchlists")

    __table_args__ = (
        Index("idx_watchlist_user_company", "user_id", "company_id", unique=True),
    )

