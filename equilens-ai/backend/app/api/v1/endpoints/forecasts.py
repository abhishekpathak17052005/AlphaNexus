from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db, parse_uuid
from app.models.company import Company
from app.models.forecast import Forecast
from app.engines.forecasting.service import forecasting_service
from app.schemas.forecast import ForecastResponse, ForecastGenerateRequest

router = APIRouter()


@router.get("/companies/{company_id}/forecasts", response_model=ForecastResponse)
def get_company_forecasts(
    company_id: str,
    metric_name: str = Query("revenue", description="revenue, net_profit, ebitda, eps"),
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.id == parse_uuid(company_id)).first()
    if not company:
        company = db.query(Company).filter(Company.symbol == company_id.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    res = forecasting_service.generate_company_forecast(
        db=db,
        company_id=str(company.id),
        metric_name=metric_name,
        forecast_horizon_years=3,
    )
    return res


@router.post("/companies/{company_id}/forecasts/generate", response_model=ForecastResponse)
def generate_forecast(
    company_id: str,
    payload: ForecastGenerateRequest,
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.id == parse_uuid(company_id)).first()
    if not company:
        company = db.query(Company).filter(Company.symbol == company_id.upper()).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    res = forecasting_service.generate_company_forecast(
        db=db,
        company_id=str(company.id),
        metric_name=payload.metric_name,
        forecast_horizon_years=payload.forecast_horizon_years,
    )
    return res

