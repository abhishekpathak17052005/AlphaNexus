"""
ALPHANEXUS – Document Card Component
"""
from typing import Dict, Any
import streamlit as st


def render_document_card(doc: Dict[str, Any]):
    """Render a financial document ingestion metadata card."""
    title = doc.get("title") or doc.get("filename", "Untitled Filing")
    status = doc.get("status", "PENDING")
    chunks = doc.get("chunks_count", 0)
    doc_type = doc.get("document_type", "annual_report").replace("_", " ").title()

    status_badge_class = "badge-success" if status == "INDEXED" else ("badge-warning" if status == "PROCESSING" else "badge-error")

    st.markdown(
        f"""
        <div class="glass-card doc-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0;">📄 {title}</h4>
                <span class="badge {status_badge_class}">{status}</span>
            </div>
            <p style="margin: 8px 0 0 0; color: #94a3b8; font-size: 0.85rem;">
                Type: <strong>{doc_type}</strong> • Chunks Indexed: <strong>{chunks}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

