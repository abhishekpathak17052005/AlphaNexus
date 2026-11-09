"""
Unit tests for ALPHANEXUS Econometric Forecasting Engine
"""
import pytest
from app.engines.forecasting.pipeline import ForecastingEngine
from app.engines.forecasting.scenarios import ScenarioGenerator


def test_scenario_generation():
    scenarios = ScenarioGenerator.generate_scenarios(
        base_projection=100.0,
        residual_std=5.0,
        horizon_steps=1,
    )
    assert "base" in scenarios
    assert "bullish" in scenarios
    assert "bearish" in scenarios
    assert scenarios["base"] == 100.0
    assert scenarios["bullish"] > scenarios["base"]
    assert scenarios["bearish"] < scenarios["base"]
