import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Numeric, ForeignKey, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    external_id = Column(String(255), unique=True, index=True, nullable=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String(1000), nullable=False)
    source = Column(String(100), default="Marketaux")
    publisher = Column(String(150), nullable=True)
    published_at = Column(DateTime, nullable=False, index=True)
    category = Column(String(50), default="General", index=True)  # Earnings, Deals, M&A, Regulatory, Capex, Management
    sentiment_label = Column(String(20), default="Neutral", index=True)  # Positive, Negative, Neutral
    sentiment_score = Column(Numeric(5, 4), nullable=True)  # -1.0 to 1.0
    ai_summary = Column(Text, nullable=True)
    financial_impact = Column(Text, nullable=True)
    is_duplicate = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="news_articles")

    __table_args__ = (
        Index("idx_news_company_published", "company_id", "published_at"),
    )

