"""
EquiLens AI – Page 8: RAG System Administration & Diagnostics
============================================================
MongoDB Atlas Vector Search validation, embedding telemetry, and live configuration editor.
"""

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.metrics import render_kpi_card
from components.status import render_engine_health_badge
from api.rag import (
    get_rag_health,
    get_rag_metrics,
    get_rag_config,
    update_rag_config,
    retrieve_chunks,
)

render_sidebar()

st.title("⚙️ RAG System Administration & Diagnostics")
st.markdown("Monitor MongoDB Atlas Vector Search indexes, embedding models, live API latency, and pipeline parameters.")

tab_health, tab_config, tab_test = st.tabs(["🛡️ Database & Engine Health", "🎛️ Pipeline Configuration", "🧪 Live Vector Retrieval Probe"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: HEALTH & TELEMETRY
# ─────────────────────────────────────────────────────────────────────────────
with tab_health:
    st.subheader("Database & Vector Infrastructure")
    try:
        health = get_rag_health()
    except Exception as exc:
        health = {"error": str(exc)}

    v_db = health.get("vector_database", {})
    m_db = health.get("mongodb", {})
    emb = health.get("embedding_engine", {})
    llm = health.get("llm_providers", {})

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        pg_ok = v_db.get("connected", False)
        render_kpi_card("PostgreSQL pgvector", "Connected" if pg_ok else "Degraded", diff=f"{v_db.get('embedding_dimension', 768)}d Index", is_positive=pg_ok)
    with c2:
        m_ok = m_db.get("connected", False)
        render_kpi_card("MongoDB Atlas", "Connected" if m_ok else "Hybrid Fallback", diff="ReplicaSet Live" if m_ok else "Local Simulation", is_positive=m_ok)
    with c3:
        render_kpi_card("Embedding Engine", emb.get("model", "BGE-Base v1.5").split("/")[-1], diff=f"dim={emb.get('dimension', 768)}", is_positive=True)
    with c4:
        render_kpi_card("LLM Synthesis", "Gemini + Groq", diff="Failover Router Active", is_positive=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Atlas & Document Storage Collections")
    
    col_mongo, col_stats = st.columns([1, 1])
    with col_mongo:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 1.25rem;">
                <div style="font-size: 1rem; font-weight: bold; color: #38bdf8; margin-bottom: 0.75rem;">MongoDB Connection Details</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Status:</b> {m_db.get('status', 'N/A')}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Deployment:</b> {m_db.get('deployment_type', 'N/A')}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Target Database:</b> {m_db.get('database', 'equilens_rag')}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Atlas Vector Search Supported:</b> {'Yes' if m_db.get('atlas_vector_search_supported') else 'No'}</div>
                {f'<div style="font-size: 0.75rem; color: #fbbf24; margin-top: 0.5rem;"><b>Notice:</b> {m_db.get("error")}</div>' if m_db.get("error") else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_stats:
        try:
            metrics_data = get_rag_metrics()
        except Exception:
            metrics_data = {}

        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 1.25rem;">
                <div style="font-size: 1rem; font-weight: bold; color: #818cf8; margin-bottom: 0.75rem;">Document & Vector Index Stats</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Total Filings Registered:</b> {metrics_data.get('total_documents', 'N/A')}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Total Vector Chunks:</b> {metrics_data.get('total_chunks', 'N/A')}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Total Research Sessions:</b> {metrics_data.get('total_sessions', 'N/A')}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.4rem;"><b>Active Embedding Dimension:</b> {metrics_data.get('embedding_dimension', 768)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
with tab_config:
    st.subheader("RAG Pipeline Hyperparameters")
    try:
        cfg = get_rag_config()
    except Exception:
        cfg = {}

    with st.form("rag_config_form"):
        cc1, cc2 = st.columns(2)
        with cc1:
            chunk_size = st.number_input("Chunk Size (Tokens)", min_value=100, max_value=2000, value=cfg.get("chunk_size", 600), step=50)
            chunk_overlap = st.number_input("Chunk Overlap (Tokens)", min_value=0, max_value=500, value=cfg.get("chunk_overlap", 100), step=25)
            top_k_val = st.number_input("Default Retrieval Top-K", min_value=1, max_value=30, value=cfg.get("retrieval_top_k", 8), step=1)

        with cc2:
            v_weight = st.slider("Vector Similarity Search Weight", 0.0, 1.0, float(cfg.get("vector_weight", 0.6)), 0.05)
            k_weight = round(1.0 - v_weight, 2)
            st.caption(f"Complementary Keyword Weight: **{k_weight}**")
            hybrid_on = st.checkbox("Enable Hybrid Dense/Sparse Retrieval", value=cfg.get("hybrid_enabled", True))
            rerank_on = st.checkbox("Enable Cross-Encoder Reranker", value=cfg.get("reranking_enabled", False))

        save_cfg = st.form_submit_button("💾 Save Pipeline Parameters", type="primary")

    if save_cfg:
        new_cfg = {
            "chunk_size": int(chunk_size),
            "chunk_overlap": int(chunk_overlap),
            "retrieval_top_k": int(top_k_val),
            "vector_weight": float(v_weight),
            "keyword_weight": float(k_weight),
            "hybrid_enabled": bool(hybrid_on),
            "reranking_enabled": bool(rerank_on),
        }
        res = update_rag_config(new_cfg)
        if "error" in res:
            st.error(f"Failed to save configuration: {res['error']}")
        else:
            st.success("Pipeline configuration saved and updated across backend engines!")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: RETRIEVAL PROBE
# ─────────────────────────────────────────────────────────────────────────────
with tab_test:
    st.subheader("🧪 Live Vector Search & Ranking Probe")
    st.write("Submit a test financial query to inspect similarity scores, token counts, and retrieved context chunks.")

    probe_q = st.text_input("Test Query", value="What are the main debt repayment obligations and credit ratings?")
    cid = st.session_state.get("selected_company_id")

    if st.button("🔍 Execute Test Retrieval", type="primary"):
        with st.spinner("Executing similarity search across vector store..."):
            probe_res = retrieve_chunks(query=probe_q, company_id=cid, top_k=6)
            if "error" in probe_res:
                st.error(f"Probe Error: {probe_res['error']}")
            else:
                chunks = probe_res.get("chunks", [])
                st.write(f"Retrieved **{len(chunks)}** relevant chunks:")
                for idx, c in enumerate(chunks, 1):
                    score = c.get("similarity_score") or c.get("rrf_score") or 0.0
                    with st.expander(f"Result #{idx} — Score: {score:.4f} | Page {c.get('page_number')} | Section: {c.get('section')}"):
                        st.caption(f"Doc ID: {c.get('document_id')} • Chunk ID: {c.get('chunk_id')}")
                        st.text_area("Chunk Content", c.get("content", ""), height=120, disabled=True)

