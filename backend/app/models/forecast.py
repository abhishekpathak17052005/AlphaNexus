import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Numeric, Integer, ForeignKey, JSON, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name = Column(String(50), nullable=False, index=True)  # revenue, net_profit, ebitda, eps, stock_price
    model_type = Column(String(50), nullable=False)  # ARIMA, Scikit_Linear, XGBoost_Ensemble, Trend_Baseline
    model_version = Column(String(20), default="1.0")
    forecast_period = Column(String(20), nullable=False)  # FY25, FY26, FY27, 30D, 90D
    target_date = Column(Date, nullable=False, index=True)
    predicted_value = Column(Numeric(18, 4), nullable=False)
    scenario = Column(String(20), default="Base", index=True)  # Bullish, Base, Bearish
    confidence_interval_lower = Column(Numeric(18, 4), nullable=True)
    confidence_interval_upper = Column(Numeric(18, 4), nullable=True)
    confidence_level = Column(Numeric(4, 2), default=0.95)
    assumptions = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="forecasts")

    __table_args__ = (
        Index("idx_forecast_company_metric_scenario", "company_id", "metric_name", "scenario"),
    )


class ForecastEvaluation(Base):
    __tablename__ = "forecast_evaluations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    model_type = Column(String(50), nullable=False)
    metric_name = Column(String(50), nullable=False)
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    train_start_date = Column(Date, nullable=False)
    train_end_date = Column(Date, nullable=False)
    test_start_date = Column(Date, nullable=False)
    test_end_date = Column(Date, nullable=False)
    mae = Column(Numeric(12, 4), nullable=False)  # Mean Absolute Error
    rmse = Column(Numeric(12, 4), nullable=False)  # Root Mean Squared Error
    mape = Column(Numeric(8, 4), nullable=True)  # Mean Absolute Percentage Error (%)
    directional_accuracy = Column(Numeric(6, 2), nullable=True)  # % of correct direction calls
    sample_count = Column(Integer, default=0)
    features_used = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    company = relationship("Company", back_populates="forecast_evaluations")

