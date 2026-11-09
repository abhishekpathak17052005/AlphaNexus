"""
EquiLens AI – Page 3: Document Intelligence & Upload
===================================================
Multi-format financial document ingestion, classification, and vector chunk inspector.
"""

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.metrics import render_kpi_card
from api.companies import get_companies
from api.documents import (
    get_documents,
    get_document,
    get_document_stats,
    upload_document,
    process_document,
    delete_document,
)

render_sidebar()

st.title("📄 Document Intelligence & Ingestion Hub")
st.markdown("Upload Indian corporate filings (PDF, DOCX, XLSX, CSV, TXT) for LangChain processing, chunking, and MongoDB vector indexing.")

tab_upload, tab_inspect, tab_library = st.tabs(["📤 Upload New Document", "🔍 Chunk & Page Inspector", "📚 All Documents"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: UPLOAD
# ─────────────────────────────────────────────────────────────────────────────
with tab_upload:
    st.subheader("Upload Financial Filing")
    
    col_file, col_meta = st.columns([1.2, 1])
    
    with col_file:
        uploaded_file = st.file_uploader(
            "Select filing document (PDF, DOCX, XLSX, CSV, TXT)",
            type=["pdf", "docx", "doc", "xlsx", "xls", "csv", "txt", "md"],
            help="Upload annual reports, quarterly filings, or earnings call transcripts up to 100MB.",
        )
        if uploaded_file:
            st.success(f"Selected: **{uploaded_file.name}** ({len(uploaded_file.getvalue()) / 1024:.1f} KB)")

    with col_meta:
        # Company selector
        companies = st.session_state.get("companies_list", [])
        if not companies:
            try:
                companies = get_companies()
                st.session_state["companies_list"] = companies
            except Exception:
                companies = []

        comp_options = {f"{c['symbol']} – {c['name']}": c["id"] for c in companies}
        current_cid = st.session_state.get("selected_company_id")
        def_idx = 0
        if current_cid:
            for idx, cid_val in enumerate(comp_options.values()):
                if str(cid_val) == str(current_cid):
                    def_idx = idx
                    break

        chosen_comp = st.selectbox("Company", list(comp_options.keys()), index=def_idx)
        selected_cid = comp_options[chosen_comp] if comp_options else None

        doc_type = st.selectbox(
            "Document Classification Hint",
            [
                "Annual Report",
                "Earnings Call Transcript",
                "Investor Presentation",
                "Financial Statement",
                "Quarterly Results",
                "Corporate Announcement",
                "Other",
            ],
            index=0,
        )

        c_fy, c_qtr = st.columns(2)
        with c_fy:
            fy = st.selectbox("Financial Year", ["FY25", "FY24", "FY23", "FY22", "FY21", "FY20"], index=1)
        with c_qtr:
            qtr = st.selectbox("Reporting Period", ["Full Year", "Q1", "Q2", "Q3", "Q4"], index=0)

    if st.button("🚀 Upload & Ingest with LangChain", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("Please choose a file to upload.")
        elif not selected_cid:
            st.error("Please choose a valid company.")
        else:
            with st.spinner("Uploading and indexing document via LangChain pipeline..."):
                file_bytes = uploaded_file.getvalue()
                res = upload_document(
                    file_bytes=file_bytes,
                    filename=uploaded_file.name,
                    company_id=selected_cid,
                    document_type=doc_type,
                    financial_year=fy,
                    quarter=None if qtr == "Full Year" else qtr,
                )

                if "error" in res:
                    st.error(f"Ingestion Error: {res['error']}")
                else:
                    st.balloons()
                    st.success(f"Document **{uploaded_file.name}** processed successfully!")
                    st.json(res)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: CHUNK & PAGE INSPECTOR
# ─────────────────────────────────────────────────────────────────────────────
with tab_inspect:
    st.subheader("Vector Chunk & Section Viewer")
    cid = st.session_state.get("selected_company_id")
    try:
        docs = get_documents(company_id=cid)
    except Exception:
        docs = []

    if docs:
        doc_map = {f"{d.get('filename')} ({d.get('document_type')}, {d.get('financial_year')})": d.get("id") for d in docs}
        sel_doc_label = st.selectbox("Select Processed Document to Inspect", list(doc_map.keys()))
        sel_doc_id = doc_map[sel_doc_label]

        # Fetch stats & chunks
        stats = get_document_stats(sel_doc_id)
        if stats and "error" not in stats:
            s1, s2, s3, s4 = st.columns(4)
            with s1:
                render_kpi_card("Total Pages", str(stats.get("total_pages", "N/A")))
            with s2:
                render_kpi_card("Vector Chunks", str(stats.get("total_chunks", "N/A")))
            with s3:
                render_kpi_card("Classified Type", stats.get("document_type", "Filing"))
            with s4:
                render_kpi_card("Status", stats.get("status", "PROCESSED"), is_positive=True)

            st.markdown("<br>", unsafe_allow_html=True)

            chunks = stats.get("chunks", [])
            if chunks:
                st.write(f"Showing **{len(chunks)}** vector chunks stored in database:")
                for c in chunks[:15]:
                    with st.expander(f"Chunk #{c.get('chunk_index')} — Page {c.get('page_number')} | Section: {c.get('section', 'General')}"):
                        st.caption(f"Tokens: {c.get('token_count', 'N/A')} • Chunk ID: {c.get('chunk_id')}")
                        st.text_area("Chunk Content", c.get("content", ""), height=150, disabled=True)
            else:
                st.info("No chunk previews returned for this document.")
        else:
            st.warning("Could not load chunk details for this document.")
    else:
        st.info("No documents found for this company.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: DOCUMENT LIBRARY
# ─────────────────────────────────────────────────────────────────────────────
with tab_library:
    st.subheader("All Registered Documents")
    all_docs = get_documents()
    if all_docs:
        df_all = pd.DataFrame(all_docs)
        cols = ["filename", "document_type", "financial_year", "total_pages", "total_chunks", "status"]
        valid_cols = [c for c in cols if c in df_all.columns]
        st.dataframe(df_all[valid_cols], use_container_width=True, hide_index=True)
    else:
        st.info("No documents currently stored in the system.")

