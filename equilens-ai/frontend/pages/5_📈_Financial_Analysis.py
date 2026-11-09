"""
EquiLens AI – Page 5: Financial Analysis & Fundamental Intelligence
===================================================================
Deterministic multi-year financial statements, DuPont ROE decomposition, and ratios.
"""

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.metrics import render_kpi_card, format_inr, format_percent
from components.charts import create_revenue_ebitda_trend_chart, DARK_THEME_LAYOUT
from api.financials import get_financials, get_statements, get_ratios

render_sidebar()

comp_obj = st.session_state.get("selected_company_obj")
if not comp_obj:
    st.warning("Please select a company from the sidebar to inspect its financial statements.")
    st.stop()

cid = comp_obj.get("id")
symbol = comp_obj.get("symbol", "N/A")
name = comp_obj.get("name", "N/A")

st.title(f"📈 Financial Analysis & Statements — {name} ({symbol})")
st.markdown("Strictly deterministic accounting statements and financial ratio calculations.")

# Key Ratio Cards
st.subheader("⚡ Core Performance & Efficiency Ratios")
try:
    ratios = get_ratios(cid)
except Exception:
    ratios = {}

if ratios and "error" not in ratios:
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        render_kpi_card("Return on Equity (ROE)", format_percent(ratios.get("roe")), is_positive=True)
    with r2:
        render_kpi_card("ROCE", format_percent(ratios.get("roce")), is_positive=True)
    with r3:
        render_kpi_card("Operating Margin", format_percent(ratios.get("operating_margin")), is_positive=True)
    with r4:
        render_kpi_card("Net Profit Margin", format_percent(ratios.get("net_profit_margin")), is_positive=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    r5, r6, r7, r8 = st.columns(4)
    with r5:
        de = ratios.get("debt_to_equity")
        render_kpi_card("Debt to Equity", f"{de:.2f}x" if de is not None else "N/A", is_positive=(de < 1.0 if de is not None else None))
    with r6:
        cr = ratios.get("current_ratio")
        render_kpi_card("Current Ratio", f"{cr:.2f}x" if cr is not None else "N/A", is_positive=(cr >= 1.2 if cr is not None else None))
    with r7:
        ic = ratios.get("interest_coverage")
        render_kpi_card("Interest Coverage", f"{ic:.2f}x" if ic is not None else "N/A", is_positive=(ic >= 3.0 if ic is not None else None))
    with r8:
        at = ratios.get("asset_turnover")
        render_kpi_card("Asset Turnover", f"{at:.2f}x" if at is not None else "N/A")
else:
    st.info("Loading deterministic ratio suite for this security...")

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Financial Charts
st.subheader("📊 Multi-Year Revenue, EBITDA & Profitability")
try:
    metrics = get_financials(cid)
except Exception:
    metrics = []

if metrics:
    fig_rev = create_revenue_ebitda_trend_chart(metrics)
    st.plotly_chart(fig_rev, use_container_width=True)
else:
    st.info("No multi-period metrics available to plot.")

st.markdown("<br>", unsafe_allow_html=True)

# Statements Tabs
st.subheader("📑 Financial Statements")
tab_income, tab_balance, tab_cash = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow Statement"])

with tab_income:
    try:
        inc_data = get_statements(cid, statement_type="INCOME_STATEMENT")
    except Exception:
        inc_data = []

    if inc_data:
        st.dataframe(pd.DataFrame(inc_data), use_container_width=True, hide_index=True)
    elif metrics:
        # Build tabular view from metrics
        inc_rows = []
        for m in sorted(metrics, key=lambda x: x.get("financial_year", "")):
            inc_rows.append({
                "Financial Year": m.get("financial_year"),
                "Revenue (₹ Cr)": format_inr(m.get("revenue")),
                "EBITDA (₹ Cr)": format_inr(m.get("ebitda")),
                "Operating Profit (₹ Cr)": format_inr(m.get("operating_profit")),
                "Net Profit (PAT) (₹ Cr)": format_inr(m.get("net_profit")),
                "EPS (₹)": f"₹{m.get('eps', 0):.2f}" if m.get("eps") else "N/A",
            })
        st.dataframe(pd.DataFrame(inc_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Income statement data currently unavailable for this company.")

with tab_balance:
    try:
        bal_data = get_statements(cid, statement_type="BALANCE_SHEET")
    except Exception:
        bal_data = []

    if bal_data:
        st.dataframe(pd.DataFrame(bal_data), use_container_width=True, hide_index=True)
    elif metrics:
        bal_rows = []
        for m in sorted(metrics, key=lambda x: x.get("financial_year", "")):
            bal_rows.append({
                "Financial Year": m.get("financial_year"),
                "Total Assets (₹ Cr)": format_inr(m.get("total_assets")),
                "Total Liabilities (₹ Cr)": format_inr(m.get("total_liabilities")),
                "Total Equity (₹ Cr)": format_inr(m.get("total_equity")),
                "Total Debt (₹ Cr)": format_inr(m.get("total_debt")),
                "Cash & Equivalents (₹ Cr)": format_inr(m.get("cash_and_equivalents")),
            })
        st.dataframe(pd.DataFrame(bal_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Balance sheet data currently unavailable.")

with tab_cash:
    try:
        cf_data = get_statements(cid, statement_type="CASH_FLOW")
    except Exception:
        cf_data = []

    if cf_data:
        st.dataframe(pd.DataFrame(cf_data), use_container_width=True, hide_index=True)
    elif metrics:
        cf_rows = []
        for m in sorted(metrics, key=lambda x: x.get("financial_year", "")):
            cf_rows.append({
                "Financial Year": m.get("financial_year"),
                "Operating Cash Flow (₹ Cr)": format_inr(m.get("operating_cash_flow")),
                "Free Cash Flow (₹ Cr)": format_inr(m.get("free_cash_flow")),
                "Capital Expenditures (₹ Cr)": format_inr(m.get("capital_expenditures")),
            })
        st.dataframe(pd.DataFrame(cf_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Cash flow data currently unavailable.")

