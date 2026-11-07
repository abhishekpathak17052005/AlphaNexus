import pytest
import numpy as np
import pandas as pd
from app.engines.forecasting.validation import ForecastValidator
from app.engines.forecasting.scenarios import ScenarioGenerator
from app.engines.forecasting.models.baseline import BaselineForecaster


def test_chronological_split():
    df = pd.DataFrame({
        "date": pd.date_range("2021-01-01", periods=10, freq="YE"),
        "value": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
    })
    train, test = ForecastValidator.chronological_split(df, date_col="date", test_fraction=0.2)
    assert len(train) == 8
    assert len(test) == 2
    # Ensure strict chronological order (train max date < test min date)
    assert train["date"].max() < test["date"].min()


def test_forecast_metrics():
    actual = np.array([100.0, 120.0, 140.0])
    pred = np.array([105.0, 115.0, 142.0])

    metrics = ForecastValidator.compute_metrics(actual, pred)
    assert "mae" in metrics
    assert "rmse" in metrics
    assert "mape" in metrics
    assert "directional_accuracy" in metrics
    assert metrics["mae"] > 0
    assert metrics["directional_accuracy"] >= 0


def test_scenarios_monotonicity_and_confidence():
    scenarios = ScenarioGenerator.generate_scenarios(
        base_projection=100.0,
        residual_std=5.0,
        horizon_steps=1,
    )
    # Bullish >= Base >= Bearish
    assert scenarios["bullish"] > scenarios["base"]
    assert scenarios["base"] > scenarios["bearish"]
    # 95% Confidence Interval bounds
    ci = scenarios["confidence_intervals"]["ci_95"]
    assert ci["lower"] < scenarios["base"] < ci["upper"]


def test_baseline_forecaster():
    model = BaselineForecaster()
    history = [100.0, 110.0, 120.0, 130.0]
    preds, std = model.fit_predict(history, forecast_steps=3)
    assert len(preds) == 3
    # With clear linear trend, predictions should continue upward
    assert preds[0] > history[-1]
    assert preds[1] > preds[0]
    assert preds[2] > preds[1]
