"""
ALPHANEXUS – RAG Chat UI Component
"""
from typing import List, Dict, Any, Optional
import streamlit as st


def render_chat_message(role: str, content: str, citations: Optional[List[Dict[str, Any]]] = None):
    """Render an individual AI or user research chat bubble with evidence citations."""
    with st.chat_message(role):
        st.markdown(content)
        if citations:
            with st.expander(f"📚 Verified Sources & Evidentiary Citations ({len(citations)})", expanded=False):
                for i, c in enumerate(citations, 1):
                    doc_name = c.get("document_name", "Filing")
                    page_num = c.get("page_number", "N/A")
                    score = c.get("similarity_score", 0.0)
                    snippet = c.get("text_snippet", "")
                    st.markdown(
                        f"""
                        <div class="glass-card citation-card">
                            <strong>[{i}] {doc_name} (Page {page_num})</strong> • Relevancy: {score:.1%}
                            <p class="citation-text">"{snippet}"</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
