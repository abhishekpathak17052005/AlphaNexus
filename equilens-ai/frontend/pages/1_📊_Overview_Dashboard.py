"""
EquiLens AI – Page 1: Overview Dashboard
========================================
Executive summary of Indian equities market, tracked watchlist, and system status.
"""

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.metrics import render_kpi_card, format_inr, format_percent
from components.charts import DARK_THEME_LAYOUT
from config import BENCHMARK_INDICES
from api.companies import get_companies, get_company_price
from api.documents import get_documents
from api.rag import get_rag_health

render_sidebar()

st.title("📊 Indian Equities Market & Platform Overview")
st.markdown("Live macro snapshot, tracked securities, and system health status.")

# Benchmark Indices Grid
st.subheader("🇮🇳 Benchmark Indices")
idx_cols = st.columns(len(BENCHMARK_INDICES))
for i, idx_data in enumerate(BENCHMARK_INDICES):
    with idx_cols[i]:
        p_chg = idx_data["pchange"]
        arrow = "+" if p_chg >= 0 else ""
        diff_str = f"{arrow}{idx_data['change']:.2f} ({arrow}{p_chg:.2f}%)"
        render_kpi_card(
            label=idx_data["name"],
            value=f"{idx_data['base_price']:,.2f}",
            diff=diff_str,
            is_positive=(p_chg >= 0),
        )

st.markdown("<br>", unsafe_allow_html=True)

# Active Selected Company Executive Snapshot
comp_obj = st.session_state.get("selected_company_obj")
if comp_obj:
    st.subheader(f"🏢 Featured Security: {comp_obj.get('name')} ({comp_obj.get('symbol')})")
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Exchange / Code", f"{comp_obj.get('exchange', 'NSE')} / {comp_obj.get('symbol')}")
    with k2:
        render_kpi_card("Market Capitalization", format_inr(comp_obj.get("market_cap")))
    with k3:
        render_kpi_card("Sector", comp_obj.get("sector") or "Diversified")
    with k4:
        render_kpi_card("Industry", comp_obj.get("industry") or "Financial Services")

    if comp_obj.get("description"):
        with st.expander("Company Business Profile & Operational Description", expanded=False):
            st.write(comp_obj.get("description"))

st.markdown("<br>", unsafe_allow_html=True)

# All Listed Equities Registry
st.subheader("📋 Tracked Indian Equities Registry")
companies = st.session_state.get("companies_list", [])
if not companies:
    try:
        companies = get_companies()
    except Exception:
        companies = []

if companies:
    df_comp = pd.DataFrame(companies)
    cols_to_show = ["symbol", "name", "exchange", "sector", "industry", "market_cap"]
    existing_cols = [c for c in cols_to_show if c in df_comp.columns]
    df_disp = df_comp[existing_cols].copy()
    if "market_cap" in df_disp.columns:
        df_disp["market_cap"] = df_disp["market_cap"].apply(lambda v: format_inr(v))
    df_disp.columns = [c.replace("_", " ").title() for c in df_disp.columns]
    st.dataframe(df_disp, use_container_width=True, hide_index=True)
else:
    st.info("Loading company registry...")

st.markdown("<br>", unsafe_allow_html=True)

# System Health Matrix
st.subheader("🛡️ Enterprise Intelligence Engines & Integrations")
try:
    h = get_rag_health()
    v_db = h.get("vector_database", {})
    m_db = h.get("mongodb", {})
    emb = h.get("embedding_engine", {})
    llm = h.get("llm_providers", {})

    h1, h2, h3, h4 = st.columns(4)
    with h1:
        render_kpi_card("Vector Search DB", "PostgreSQL pgvector", diff=f"{v_db.get('embedding_dimension', 768)}d Index", is_positive=True)
    with h2:
        mongo_ok = m_db.get("connected", False)
        render_kpi_card("Document Database", "MongoDB Atlas", diff="Atlas Search" if mongo_ok else "Hybrid Fallback", is_positive=mongo_ok)
    with h3:
        render_kpi_card("Embedding Model", "BGE-Base v1.5", diff="768 Dim / Normalized", is_positive=True)
    with h4:
        render_kpi_card("Reasoning Engine", "Gemini + Groq", diff="Multi-Provider Failover", is_positive=True)
except Exception as e:
    st.warning(f"Engine status check unavailable: {e}")

