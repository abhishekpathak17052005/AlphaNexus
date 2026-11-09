from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.models.company import Company
from app.models.financial import FinancialMetric, StockPrice
from app.models.forecast import Forecast, ForecastEvaluation
from app.engines.forecasting.models.baseline import BaselineForecaster
from app.engines.forecasting.scenarios import ScenarioGenerator
from app.engines.forecasting.validation import ForecastValidator
from app.core.logging import logger


class ForecastingService:
    """
    Forecasting Engine Orchestrator for EquiLens AI.
    Generates multi-period financial forecasts (Revenue, Net Profit, EBITDA, EPS)
    and stock price trend scenarios with walk-forward validation and clear disclaimers.
    """

    def __init__(self):
        self.baseline_model = BaselineForecaster()

    def generate_company_forecast(
        self,
        db: Session,
        company_id: str,
        metric_name: str = "revenue",
        forecast_horizon_years: int = 3,
    ) -> Dict[str, Any]:
        """
        Retrieves historical metrics for company, checks data adequacy,
        runs baseline model, generates Bull/Base/Bear scenarios, and persists forecast.
        """
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValueError(f"Company {company_id} not found")

        # Query historical annual metrics
        metrics = (
            db.query(FinancialMetric)
            .filter(
                FinancialMetric.company_id == company_id,
                FinancialMetric.metric_name == metric_name,
                FinancialMetric.period_type == "annual",
            )
            .order_by(FinancialMetric.period_end_date.asc())
            .all()
        )

        if len(metrics) < 2:
            return {
                "status": "INSUFFICIENT_DATA",
                "company_symbol": company.symbol,
                "metric_name": metric_name,
                "historical_points": len(metrics),
                "message": f"Insufficient historical data ({len(metrics)} annual points). Minimum 2 required for statistical forecasting.",
            }

        history_values = [float(m.value) for m in metrics]
        last_fy_str = metrics[-1].financial_year  # e.g., "FY24"

        # Fit model and predict
        future_preds, residual_std = self.baseline_model.fit_predict(
            history_values,
            forecast_steps=forecast_horizon_years,
        )

        # Parse future financial years
        try:
            curr_fy_num = int(last_fy_str.replace("FY", ""))
        except Exception:
            curr_fy_num = 24

        forecast_periods = []
        for i, pred in enumerate(future_preds):
            target_fy = f"FY{curr_fy_num + i + 1}"
            scenarios = ScenarioGenerator.generate_scenarios(
                base_projection=pred,
                residual_std=residual_std,
                horizon_steps=i + 1,
            )
            forecast_periods.append({
                "period": target_fy,
                "base": scenarios["base"],
                "bullish": scenarios["bullish"],
                "bearish": scenarios["bearish"],
                "confidence_intervals": scenarios["confidence_intervals"],
            })

            # Persist to database
            target_date = date(2020 + curr_fy_num + i + 1, 3, 31)
            for scen_name, val in [("Base", scenarios["base"]), ("Bullish", scenarios["bullish"]), ("Bearish", scenarios["bearish"])]:
                fc_record = Forecast(
                    company_id=company.id,
                    metric_name=metric_name,
                    model_type="Trend_Baseline_v1",
                    model_version="1.0",
                    forecast_period=target_fy,
                    target_date=target_date,
                    predicted_value=val,
                    scenario=scen_name,
                    confidence_interval_lower=scenarios["confidence_intervals"]["ci_95"]["lower"],
                    confidence_interval_upper=scenarios["confidence_intervals"]["ci_95"]["upper"],
                    assumptions={"residual_std": residual_std, "horizon_step": i + 1},
                )
                db.add(fc_record)

        db.commit()

        # Compute validation metrics if at least 4 historical points exist
        eval_metrics = None
        if len(history_values) >= 4:
            train_vals = history_values[:-1]
            test_val = history_values[-1]
            val_preds, _ = self.baseline_model.fit_predict(train_vals, forecast_steps=1)
            eval_metrics = ForecastValidator.compute_metrics(
                actual=[test_val],
                predicted=val_preds,
            )

        return {
            "status": "SUCCESS",
            "company_id": str(company.id),
            "company_symbol": company.symbol,
            "metric_name": metric_name,
            "historical": [
                {"period": m.financial_year, "value": float(m.value)} for m in metrics
            ],
            "forecasts": forecast_periods,
            "evaluation": eval_metrics,
            "disclaimer": ScenarioGenerator.DISCLAIMER,
        }


forecasting_service = ForecastingService()

