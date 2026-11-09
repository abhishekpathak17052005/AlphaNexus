"""
ALPHANEXUS – Deterministic Financial Analysis Engine
====================================================
Computes DuPont ROE, profitability ratios, working capital, and solvency metrics.
"""

from typing import Optional, Dict, Any
from app.engines.analytics.formulas import FinancialCalculator
from app.engines.analytics.peer_analyzer import peer_analyzer


def calculate_roe(net_profit: Optional[float], total_equity: Optional[float]) -> Optional[float]:
    return FinancialCalculator.calculate_roe(net_profit, total_equity)


def calculate_roce(ebit: Optional[float], total_assets: Optional[float], current_liabilities: Optional[float]) -> Optional[float]:
    return FinancialCalculator.calculate_roce(ebit, total_assets, current_liabilities)


def calculate_ebitda_margin(ebitda: Optional[float], revenue: Optional[float]) -> Optional[float]:
    return FinancialCalculator.calculate_ebitda_margin(ebitda, revenue)


def calculate_net_profit_margin(net_profit: Optional[float], revenue: Optional[float]) -> Optional[float]:
    return FinancialCalculator.calculate_net_profit_margin(net_profit, revenue)


def calculate_debt_to_equity(total_debt: Optional[float], total_equity: Optional[float]) -> Optional[float]:
    return FinancialCalculator.calculate_debt_to_equity(total_debt, total_equity)


def calculate_current_ratio(current_assets: Optional[float], current_liabilities: Optional[float]) -> Optional[float]:
    return FinancialCalculator.calculate_current_ratio(current_assets, current_liabilities)


def calculate_free_cash_flow(operating_cash_flow: Optional[float], capital_expenditures: Optional[float]) -> Optional[float]:
    return FinancialCalculator.calculate_free_cash_flow(operating_cash_flow, capital_expenditures)


def calculate_dupont_roe(
    net_profit: Optional[float],
    revenue: Optional[float],
    total_assets: Optional[float],
    total_equity: Optional[float],
) -> Dict[str, Any]:
    npm = calculate_net_profit_margin(net_profit, revenue)
    at = round(revenue / total_assets, 2) if revenue and total_assets and total_assets > 0 else None
    em = round(total_assets / total_equity, 2) if total_assets and total_equity and total_equity > 0 else None
    roe = calculate_roe(net_profit, total_equity)
    return {
        "roe": roe,
        "net_profit_margin": npm,
        "asset_turnover": at,
        "equity_multiplier": em,
    }


__all__ = [
    "FinancialCalculator",
    "calculate_roe",
    "calculate_roce",
    "calculate_dupont_roe",
    "calculate_ebitda_margin",
    "calculate_net_profit_margin",
    "calculate_debt_to_equity",
    "calculate_current_ratio",
    "calculate_free_cash_flow",
    "peer_analyzer",
]
