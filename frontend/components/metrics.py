"""
EquiLens AI – Financial Metrics & KPI Cards Component
=====================================================
Renders high-contrast financial KPI cards with diff badges and currency formatting.
"""

import streamlit as st
from typing import Optional, Union


def format_inr(value: Optional[Union[float, int]], is_crores: bool = True) -> str:
    if value is None:
        return "N/A"
    try:
        val = float(value)
        if is_crores:
            return f"₹{val:,.2f} Cr"
        return f"₹{val:,.2f}"
    except (ValueError, TypeError):
        return str(value)


def format_percent(value: Optional[Union[float, int]]) -> str:
    if value is None:
        return "N/A"
    try:
        val = float(value)
        # If fraction e.g. 0.18 -> 18%
        if abs(val) < 1.0 and val != 0:
            val = val * 100
        return f"{val:.2f}%"
    except (ValueError, TypeError):
        return str(value)


def render_kpi_card(
    label: str,
    value: str,
    diff: Optional[str] = None,
    is_positive: Optional[bool] = None,
    help_text: Optional[str] = None,
):
    diff_html = ""
    if diff:
        cls = "kpi-diff-up" if is_positive else ("kpi-diff-down" if is_positive is False else "")
        arrow = "▲ " if is_positive else ("▼ " if is_positive is False else "")
        diff_html = f'<div class="{cls}">{arrow}{diff}</div>'

    help_attr = f'title="{help_text}"' if help_text else ""

    st.markdown(
        f"""
        <div class="kpi-card" {help_attr}>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {diff_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

