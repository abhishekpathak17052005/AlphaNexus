"""
Unit tests for ALPHANEXUS Financial Analytics Engine
"""
import pytest
from app.engines.financial.ratios.formulas import FinancialCalculator
from app.engines.financial.analysis import calculate_roe, calculate_ebitda_margin, calculate_free_cash_flow


def test_roe_calculation():
    net_income = 15000000.0
    equity = 60000000.0
    roe = calculate_roe(net_income, equity)
    assert roe == 25.0


def test_ebitda_margin_calculation():
    ebitda = 20000000.0
    revenue = 100000000.0
    margin = calculate_ebitda_margin(ebitda, revenue)
    assert margin == 20.0


def test_free_cash_flow():
    operating_cf = 25000000.0
    capex = 5000000.0
    fcf = calculate_free_cash_flow(operating_cf, capex)
    assert fcf == 20000000.0

