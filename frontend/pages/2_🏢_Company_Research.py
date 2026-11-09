"""
EquiLens AI – Page 2: Company Research Hub
===========================================
Deep fundamental profiling, executive summary, and security documentation repository.
"""

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.metrics import render_kpi_card, format_inr, format_percent
from api.companies import get_companies, get_company, get_company_price
from api.financials import get_ratios
from api.documents import get_documents

render_sidebar()

comp_obj = st.session_state.get("selected_company_obj")
if not comp_obj:
    st.warning("Please select a company from the sidebar to inspect its research profile.")
    st.stop()

cid = comp_obj.get("id")
symbol = comp_obj.get("symbol", "N/A")
name = comp_obj.get("name", "N/A")

st.title(f"🏢 Company Research Hub — {name} ({symbol})")
st.markdown("Comprehensive fundamental profile, capital structure, and regulatory documentation repository.")

# Top Profile Card
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Exchange / Ticker", f"{comp_obj.get('exchange', 'NSE')} : {symbol}")
with c2:
    render_kpi_card("Market Capitalization", format_inr(comp_obj.get("market_cap")))
with c3:
    render_kpi_card("Sector", comp_obj.get("sector") or "Diversified")
with c4:
    render_kpi_card("Industry", comp_obj.get("industry") or "Financials")

st.markdown("<br>", unsafe_allow_html=True)

# Overview & Corporate Info
info_col1, info_col2 = st.columns([2, 1])

with info_col1:
    st.subheader("📖 Executive Description")
    st.write(comp_obj.get("description") or "No detailed profile description on record.")

    st.subheader("🏛️ Corporate Identity")
    meta_df = pd.DataFrame([
        {"Field": "ISIN", "Value": comp_obj.get("isin") or "INE" + symbol},
        {"Field": "Exchange", "Value": comp_obj.get("exchange", "NSE")},
        {"Field": "Sector", "Value": comp_obj.get("sector") or "Equity"},
        {"Field": "Industry", "Value": comp_obj.get("industry") or "Financial Markets"},
        {"Field": "Website", "Value": comp_obj.get("website") or f"https://www.{symbol.lower()}.com"},
    ])
    st.dataframe(meta_df, hide_index=True, use_container_width=True)

with info_col2:
    st.subheader("⚡ Valuation & Profitability")
    try:
        ratios = get_ratios(cid)
    except Exception:
        ratios = {}

    if ratios and "error" not in ratios:
        render_kpi_card("Return on Equity (ROE)", format_percent(ratios.get("roe")), is_positive=True)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        render_kpi_card("ROCE", format_percent(ratios.get("roce")), is_positive=True)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        render_kpi_card("Net Profit Margin", format_percent(ratios.get("net_profit_margin")), is_positive=True)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        render_kpi_card("Debt to Equity", f"{ratios.get('debt_to_equity', 0):.2f}x" if ratios.get("debt_to_equity") is not None else "N/A")
    else:
        st.info("Financial ratios computing for active period.")

st.markdown("<br>", unsafe_allow_html=True)

# Company Documents Repository
st.subheader("📄 Registered Filings & Financial Documents")
try:
    docs = get_documents(company_id=cid)
except Exception:
    docs = []

if docs:
    d_rows = []
    for d in docs:
        d_rows.append({
            "File Name": d.get("filename"),
            "Document Type": d.get("document_type"),
            "Financial Year": d.get("financial_year"),
            "Pages": d.get("total_pages"),
            "Vector Chunks": d.get("total_chunks"),
            "Status": d.get("status"),
            "Uploaded": str(d.get("created_at", ""))[:10],
        })
    st.dataframe(pd.DataFrame(d_rows), use_container_width=True, hide_index=True)
else:
    st.info(f"No regulatory documents or annual reports on file for {name}. Use the Document Intelligence module to upload one.")

