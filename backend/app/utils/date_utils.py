"""
ALPHANEXUS – Date & Financial Year Utilities
============================================
Handles Indian financial year quarters, calendar conversions, and period calculations.
"""

from datetime import datetime, date
from typing import Optional, Tuple


def get_indian_financial_year(d: Optional[date] = None) -> str:
    """Returns FY string for Indian financial year (April 1 to March 31)."""
    if d is None:
        d = date.today()
    if d.month >= 4:
        return f"FY{str(d.year + 1)[-2:]}"
    return f"FY{str(d.year)[-2:]}"


def parse_reporting_period(period_str: str) -> Tuple[Optional[str], Optional[str]]:
    """Extracts (financial_year, quarter) from strings like 'FY24 Q3' or 'Q2 FY23'."""
    fy = None
    quarter = None
    parts = period_str.upper().split()
    for p in parts:
        if p.startswith("FY"):
            fy = p
        elif p in ["Q1", "Q2", "Q3", "Q4"]:
            quarter = p
    return fy, quarter
