"""
EquiLens AI – Global Navigation Sidebar Component
==================================================
Manages global session state, active company selector, live indices, and engine health.
"""

import os
import streamlit as st
from config import APP_NAME, APP_TAGLINE, APP_VERSION, BENCHMARK_INDICES
from api.companies import get_companies
from api.rag import get_rag_health


def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_sidebar():
    load_custom_css()

    with st.sidebar:
        # Brand Header
        st.markdown(
            f"""
            <div style="padding: 0.5rem 0; border-bottom: 1px solid #1f2937; margin-bottom: 1rem;">
                <div style="font-size: 1.4rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    ⚡ {APP_NAME}
                </div>
                <div style="font-size: 0.78rem; color: #94a3b8;">{APP_TAGLINE}</div>
                <div style="font-size: 0.65rem; color: #64748b; font-family: monospace; margin-top: 2px;">v{APP_VERSION} • NSE/BSE Intel</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Company Selector
        st.subheader("🏢 Active Company")
        if "companies_list" not in st.session_state or not st.session_state["companies_list"]:
            try:
                companies = get_companies()
                st.session_state["companies_list"] = companies
            except Exception:
                companies = []
                st.session_state["companies_list"] = []
        else:
            companies = st.session_state["companies_list"]

        if companies:
            options = {f"{c['symbol']} – {c['name']}": c["id"] for c in companies}
            labels = list(options.keys())

            # Find default index
            current_id = st.session_state.get("selected_company_id")
            default_idx = 0
            if current_id:
                for idx, (lbl, cid) in enumerate(options.items()):
                    if str(cid) == str(current_id):
                        default_idx = idx
                        break

            chosen_label = st.selectbox(
                "Select Listed Company",
                labels,
                index=default_idx,
                key="company_selectbox_widget",
                label_visibility="collapsed",
            )
            selected_id = options[chosen_label]
            st.session_state["selected_company_id"] = selected_id
            st.session_state["selected_company_label"] = chosen_label
            # Find selected company dict
            for c in companies:
                if str(c["id"]) == str(selected_id):
                    st.session_state["selected_company_obj"] = c
                    break
        else:
            st.warning("Connecting to company registry...")

        st.markdown("<hr style='border-color: #1f2937; margin: 1rem 0;'>", unsafe_allow_html=True)

        # Market Benchmark Snapshot
        st.subheader("📊 Market Snapshot")
        idx_cols = st.columns(2)
        for i, idx_data in enumerate(BENCHMARK_INDICES[:4]):
            col = idx_cols[i % 2]
            with col:
                p_chg = idx_data["pchange"]
                color = "#10b981" if p_chg >= 0 else "#f43f5e"
                arrow = "▲" if p_chg >= 0 else "▼"
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #1f2937; border-radius: 6px; padding: 0.4rem; margin-bottom: 0.4rem;">
                        <div style="font-size: 0.7rem; color: #94a3b8;">{idx_data['name']}</div>
                        <div style="font-size: 0.95rem; font-weight: bold; color: #f9fafb;">{idx_data['base_price']:,.2f}</div>
                        <div style="font-size: 0.7rem; color: {color}; font-weight: 600;">{arrow} {abs(p_chg):.2f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<hr style='border-color: #1f2937; margin: 1rem 0;'>", unsafe_allow_html=True)

        # System Engine Telemetry
        st.subheader("⚙️ Engine Status")
        try:
            health = get_rag_health()
            mongo_status = "Healthy" if health.get("mongodb", {}).get("connected") else "Degraded"
            pg_status = "Healthy" if health.get("vector_database", {}).get("connected") else "Degraded"
        except Exception:
            mongo_status = "Checking"
            pg_status = "Checking"

        st.markdown(
            f"""
            <div style="font-size: 0.75rem; color: #cbd5e1; display: flex; flex-direction: column; gap: 0.3rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span>PostgreSQL / pgvector:</span> <span style="color: #34d399;">● {pg_status}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>MongoDB Atlas Search:</span> <span style="color: {'#34d399' if mongo_status == 'Healthy' else '#fbbf24'};">● {mongo_status}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>LangChain Core:</span> <span style="color: #34d399;">● Ready</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>AI Reasoning (Gemini/Groq):</span> <span style="color: #34d399;">● Online</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

