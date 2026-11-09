"""
EquiLens AI – Professional Financial Intelligence & Equity Research Platform
=============================================================================
Main Streamlit Application Entrypoint.
"""

import streamlit as st

st.set_page_config(
    page_title="EquiLens AI — See Beyond the Stock Price",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config import APP_NAME, APP_TAGLINE, APP_VERSION
from components.sidebar import render_sidebar
from components.metrics import render_kpi_card, format_inr
from api.companies import get_companies
from api.documents import get_documents
from api.rag import get_rag_health

# Initialize Sidebar & Styles
render_sidebar()

# Main Header Banner
st.markdown(
    f"""
    <div class="equilens-brand-header">
        <div>
            <span class="equilens-brand-title">⚡ {APP_NAME}</span>
            <span class="equilens-brand-tagline">| {APP_TAGLINE}</span>
        </div>
        <div style="font-family: monospace; font-size: 0.8rem; color: #38bdf8; background: #0f172a; padding: 0.3rem 0.8rem; border-radius: 9999px; border: 1px solid #1e293b;">
            NSE / BSE Financial Intelligence Hub
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Active Company Focus Banner
comp_obj = st.session_state.get("selected_company_obj")
if comp_obj:
    symbol = comp_obj.get("symbol", "NSE")
    name = comp_obj.get("name", "Selected Company")
    sector = comp_obj.get("sector") or "Diversified"
    industry = comp_obj.get("industry") or "Equity"
    mcap = comp_obj.get("market_cap")

    st.markdown(
        f"""
        <div style="background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 8px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 1.3rem; font-weight: 700; color: #f8fafc;">{name}</span>
                <span style="background: #3b82f6; color: white; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold; margin-left: 0.75rem;">{symbol}</span>
                <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">Sector: {sector} • Industry: {industry}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Market Capitalization</div>
                <div style="font-size: 1.25rem; font-weight: bold; color: #38bdf8; font-family: monospace;">{format_inr(mcap)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Quick Nav Tiles
st.subheader("🚀 Platform Workspaces")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="kpi-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="font-weight: bold; color: #f9fafb; font-size: 1rem;">AI Research Terminal</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin: 0.4rem 0 0.8rem 0;">Fact-grounded financial Q&A with LangChain & verified page-level citations.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch AI Chat →", use_container_width=True, key="btn_nav_chat"):
        st.switch_page("pages/4_🤖_AI_Research_Assistant.py")

with c2:
    st.markdown(
        """
        <div class="kpi-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📄</div>
            <div style="font-weight: bold; color: #f9fafb; font-size: 1rem;">Document Hub</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin: 0.4rem 0 0.8rem 0;">Upload annual reports, transcripts, and statements into MongoDB Vector Search.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Upload Filings →", use_container_width=True, key="btn_nav_docs"):
        st.switch_page("pages/3_📄_Document_Intelligence.py")

with c3:
    st.markdown(
        """
        <div class="kpi-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📈</div>
            <div style="font-weight: bold; color: #f9fafb; font-size: 1rem;">Fundamental Intelligence</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin: 0.4rem 0 0.8rem 0;">Deterministic financial ratios, DuPont analysis, and interactive statement tables.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Analyze Financials →", use_container_width=True, key="btn_nav_fin"):
        st.switch_page("pages/5_📈_Financial_Analysis.py")

with c4:
    st.markdown(
        """
        <div class="kpi-card">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔮</div>
            <div style="font-weight: bold; color: #f9fafb; font-size: 1rem;">Performance Forecasts</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin: 0.4rem 0 0.8rem 0;">Multi-scenario econometric modeling (Bull, Base, Bear) with confidence bands.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Generate Forecasts →", use_container_width=True, key="btn_nav_fore"):
        st.switch_page("pages/7_🔮_Performance_Forecasting.py")

st.markdown("<br>", unsafe_allow_html=True)

# Recent Activity & Telemetry Grid
col_docs, col_health = st.columns([2, 1])

with col_docs:
    st.subheader("📑 Indexed Financial Filings")
    cid = st.session_state.get("selected_company_id")
    try:
        docs = get_documents(company_id=cid)
    except Exception:
        docs = []

    if docs:
        doc_rows = []
        for d in docs[:6]:
            doc_rows.append({
                "Document Name": d.get("filename", "Filing"),
                "Type": d.get("document_type", "Annual Report"),
                "FY": d.get("financial_year", "FY24"),
                "Pages": d.get("total_pages", 0),
                "Chunks": d.get("total_chunks", 0),
                "Status": d.get("status", "PROCESSED"),
            })
        st.dataframe(doc_rows, use_container_width=True)
    else:
        st.info("No documents uploaded yet for this company. Visit Document Intelligence to upload an annual report or transcript.")

with col_health:
    st.subheader("🛡️ AI & Database Stack")
    try:
        health_data = get_rag_health()
        v_db = health_data.get("vector_database", {})
        m_db = health_data.get("mongodb", {})
        emb = health_data.get("embedding_engine", {})
        llm = health_data.get("llm_providers", {})

        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 1rem;">
                <div style="font-size: 0.85rem; margin-bottom: 0.6rem;">
                    <b>PostgreSQL / pgvector:</b> <span style="color: #34d399;">Connected ({v_db.get('embedding_dimension', 768)}d)</span>
                </div>
                <div style="font-size: 0.85rem; margin-bottom: 0.6rem;">
                    <b>MongoDB Atlas:</b> <span style="color: {'#34d399' if m_db.get('connected') else '#fbbf24'};">{m_db.get('status', 'Hybrid Mode')}</span>
                </div>
                <div style="font-size: 0.85rem; margin-bottom: 0.6rem;">
                    <b>Embedding Model:</b> <span style="color: #38bdf8;">{emb.get('model', 'BAAI/bge-base-en-v1.5')}</span>
                </div>
                <div style="font-size: 0.85rem; margin-bottom: 0.6rem;">
                    <b>Primary LLM:</b> <span style="color: #818cf8;">{llm.get('primary_provider', 'Google Gemini')}</span>
                </div>
                <div style="font-size: 0.85rem;">
                    <b>Fallback LLM:</b> <span style="color: #a78bfa;">{llm.get('fallback_provider', 'Groq')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.warning(f"Engine status probe: {e}")

