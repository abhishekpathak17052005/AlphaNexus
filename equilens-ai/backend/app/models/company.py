import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Text, ForeignKey, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    symbol = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    exchange = Column(String(20), default="NSE", index=True)  # NSE, BSE
    isin = Column(String(50), index=True, nullable=True)
    sector = Column(String(100), index=True, nullable=True)
    industry = Column(String(100), index=True, nullable=True)
    market_cap = Column(Numeric(18, 2), nullable=True)  # in INR Crores
    current_price = Column(Numeric(12, 2), nullable=True)
    day_change = Column(Numeric(10, 2), nullable=True)
    day_change_percent = Column(Numeric(8, 2), nullable=True)
    pe_ratio = Column(Numeric(10, 2), nullable=True)
    pb_ratio = Column(Numeric(10, 2), nullable=True)
    roe = Column(Numeric(8, 2), nullable=True)  # in %
    roce = Column(Numeric(8, 2), nullable=True)  # in %
    dividend_yield = Column(Numeric(8, 2), nullable=True)  # in %
    week_52_high = Column(Numeric(12, 2), nullable=True)
    week_52_low = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(10), default="INR")
    description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    identifiers = relationship("CompanyIdentifier", back_populates="company", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="company", cascade="all, delete-orphan")
    document_chunks = relationship("DocumentChunk", back_populates="company", cascade="all, delete-orphan")
    financial_statements = relationship("FinancialStatement", back_populates="company", cascade="all, delete-orphan")
    financial_metrics = relationship("FinancialMetric", back_populates="company", cascade="all, delete-orphan")
    stock_prices = relationship("StockPrice", back_populates="company", cascade="all, delete-orphan")
    news_articles = relationship("NewsArticle", back_populates="company", cascade="all, delete-orphan")
    corporate_actions = relationship("CorporateAction", back_populates="company", cascade="all, delete-orphan")
    market_events = relationship("MarketEvent", back_populates="company", cascade="all, delete-orphan")
    forecasts = relationship("Forecast", back_populates="company", cascade="all, delete-orphan")
    forecast_evaluations = relationship("ForecastEvaluation", back_populates="company", cascade="all, delete-orphan")
    watchlists = relationship("Watchlist", back_populates="company", cascade="all, delete-orphan")


class CompanyIdentifier(Base):
    __tablename__ = "company_identifiers"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    identifier_type = Column(String(50), nullable=False)  # NSE_SYMBOL, BSE_SCRIP, CIN, ISIN, BLOOMBERG
    identifier_value = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="identifiers")

    __table_args__ = (
        Index("idx_identifier_type_value", "identifier_type", "identifier_value"),
    )

