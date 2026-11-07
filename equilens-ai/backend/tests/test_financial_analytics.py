import pytest
from app.engines.analytics.formulas import FinancialCalculator


def test_growth_rate_standard():
    # Normal positive growth
    assert FinancialCalculator.calculate_growth_rate(120.0, 100.0) == 20.0
    # Normal negative growth
    assert FinancialCalculator.calculate_growth_rate(80.0, 100.0) == -20.0


def test_growth_rate_edge_cases():
    # Zero denominator must return None, never raise ZeroDivisionError
    assert FinancialCalculator.calculate_growth_rate(100.0, 0.0) is None
    # None values
    assert FinancialCalculator.calculate_growth_rate(None, 100.0) is None
    assert FinancialCalculator.calculate_growth_rate(100.0, None) is None


def test_ebitda_and_pat_margins():
    # EBITDA Margin
    assert FinancialCalculator.calculate_ebitda_margin(25.0, 100.0) == 25.0
    # Net Profit Margin
    assert FinancialCalculator.calculate_net_profit_margin(15.0, 100.0) == 15.0
    # Zero revenue
    assert FinancialCalculator.calculate_ebitda_margin(25.0, 0.0) is None
    assert FinancialCalculator.calculate_net_profit_margin(15.0, 0.0) is None


def test_roe_and_roce():
    # ROE
    assert FinancialCalculator.calculate_roe(15.0, 100.0) == 15.0
    # Negative/Zero equity returns None
    assert FinancialCalculator.calculate_roe(15.0, 0.0) is None
    assert FinancialCalculator.calculate_roe(15.0, -10.0) is None

    # ROCE = EBIT / (Total Assets - Current Liabilities)
    # Total Assets = 200, Current Liab = 50 -> Capital Employed = 150
    # EBIT = 30 -> 30/150 = 20%
    assert FinancialCalculator.calculate_roce(30.0, 200.0, 50.0) == 20.0
    # Zero capital employed
    assert FinancialCalculator.calculate_roce(30.0, 100.0, 100.0) is None


def test_solvency_and_cash_flow():
    # Debt to Equity
    assert FinancialCalculator.calculate_debt_to_equity(50.0, 100.0) == 0.50
    assert FinancialCalculator.calculate_debt_to_equity(50.0, 0.0) is None

    # Current ratio
    assert FinancialCalculator.calculate_current_ratio(150.0, 100.0) == 1.50
    assert FinancialCalculator.calculate_current_ratio(150.0, 0.0) is None

    # Free Cash Flow = Operating Cash Flow - Capex
    assert FinancialCalculator.calculate_free_cash_flow(100.0, 30.0) == 70.0
    # When capex is negative in input, abs() handles it
    assert FinancialCalculator.calculate_free_cash_flow(100.0, -30.0) == 70.0

