"""
EquiLens AI – Citations Component
==================================
Renders verified source citations with page numbers, document links, and exact verbatim excerpts.
"""

import streamlit as st
from typing import List, Dict, Any


def render_citations_expander(citations: List[Dict[str, Any]], title: str = "Verified Sources & Citations"):
    if not citations:
        st.info("No specific document citations found for this query.")
        return

    with st.expander(f"📚 {title} ({len(citations)} sources)", expanded=False):
        for idx, cit in enumerate(citations, 1):
            doc_name = cit.get("document_name") or cit.get("filename") or f"Doc #{str(cit.get('document_id', ''))[:8]}"
            page = cit.get("page_number", "N/A")
            sec = cit.get("section") or "General"
            conf = cit.get("confidence_score", 0.95)
            excerpt = cit.get("excerpt", "").strip()

            st.markdown(
                f"""
                <div class="citation-box">
                    <div class="citation-header">
                        <span>[Source {idx}] {doc_name} • Page {page}</span>
                        <span>Confidence: {conf * 100:.1f}%</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #94a3b8; margin-bottom: 0.25rem;">Section: <b>{sec}</b></div>
                    <div class="citation-excerpt">"{excerpt}"</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_citation_modal(cit: Dict[str, Any]):
    """Renders a single focused citation modal card."""
    doc_name = cit.get("document_name") or cit.get("filename") or "Filing Document"
    page = cit.get("page_number", 1)
    excerpt = cit.get("excerpt", "")
    st.markdown(
        f"""
        <div style="background: #111827; border: 1px solid #38bdf8; border-radius: 8px; padding: 1.25rem; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #38bdf8; font-weight: bold;">📄 {doc_name}</span>
                <span style="background: #1e293b; color: #f8fafc; padding: 0.1rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">Page {page}</span>
            </div>
            <div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; font-style: italic;">
                "{excerpt}"
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

