import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, Numeric, Integer, ForeignKey, JSON, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class FinancialStatement(Base):
    __tablename__ = "financial_statements"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    statement_type = Column(String(50), nullable=False, index=True)  # income_statement, balance_sheet, cash_flow
    period_type = Column(String(20), nullable=False)  # annual, quarterly
    financial_year = Column(String(20), nullable=False, index=True)  # FY24, FY25
    quarter = Column(String(10), nullable=True)  # Q1, Q2, Q3, Q4
    period_end_date = Column(Date, nullable=False)
    is_consolidated = Column(Boolean, default=True)
    currency = Column(String(10), default="INR")
    unit = Column(String(20), default="INR_CRORES")  # INR_CRORES, INR_LAKHS, USD_MILLIONS
    raw_data = Column(JSON, default=dict)
    is_audited = Column(Boolean, default=True)
    source = Column(String(100), default="NSE_FILING")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="financial_statements")

    __table_args__ = (
        Index("idx_statement_company_period", "company_id", "statement_type", "financial_year", "quarter"),
    )


class FinancialMetric(Base):
    __tablename__ = "financial_metrics"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False, index=True)  # revenue, ebitda, net_profit, eps, roe, roce, etc.
    metric_category = Column(String(50), nullable=False)  # growth, profitability, solvency, cash_flow, valuation
    period_type = Column(String(20), nullable=False)  # annual, quarterly
    financial_year = Column(String(20), nullable=False, index=True)
    quarter = Column(String(10), nullable=True)
    period_end_date = Column(Date, nullable=False)
    value = Column(Numeric(18, 4), nullable=False)
    unit = Column(String(20), default="INR_CRORES")
    currency = Column(String(10), default="INR")
    yoy_growth = Column(Numeric(8, 2), nullable=True)  # YoY %
    qoq_growth = Column(Numeric(8, 2), nullable=True)  # QoQ %
    is_consolidated = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="financial_metrics")

    __table_args__ = (
        Index("idx_metric_company_name_fy", "company_id", "metric_name", "financial_year"),
    )


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open = Column(Numeric(12, 2), nullable=False)
    high = Column(Numeric(12, 2), nullable=False)
    low = Column(Numeric(12, 2), nullable=False)
    close = Column(Numeric(12, 2), nullable=False)
    adjusted_close = Column(Numeric(12, 2), nullable=True)
    volume = Column(Numeric(18, 0), nullable=False)
    vwap = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(10), default="INR")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="stock_prices")

    __table_args__ = (
        Index("idx_price_company_date", "company_id", "date"),
    )

