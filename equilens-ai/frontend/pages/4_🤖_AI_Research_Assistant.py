"""
EquiLens AI – Page 4: AI Research Assistant (RAG Chat Terminal)
==============================================================
Multi-turn conversational equity research analyst with LangChain routing and verified citations.
"""

import uuid
import streamlit as st

from components.sidebar import render_sidebar
from components.status import render_route_pill
from components.citations import render_citations_expander, render_citation_modal
from api.rag import chat_rag, get_sessions, get_session

render_sidebar()

st.title("🤖 AI Research Assistant — Fact-Grounded Terminal")
st.markdown("Ask in-depth financial questions backed strictly by verified corporate filings, annual reports, and earnings transcripts.")

# Ensure Session State for Chat
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {
            "role": "assistant",
            "content": "Welcome to **EquiLens AI**. Ask me anything about the active company's financial performance, balance sheet health, management commentary, or risk factors. Every fact is cited directly from source documents.",
            "citations": [],
            "route": "RAG_FINANCIAL_QA",
        }
    ]

# Top RAG Configuration & Filter Bar
with st.expander("⚙️ Retrieval & AI Model Parameters", expanded=False):
    col_m, col_fy, col_dt, col_k = st.columns(4)
    with col_m:
        model_choice = st.selectbox("LLM Provider", ["Multi-Provider (Gemini + Groq Fallback)", "Google Gemini", "Groq Llama-3.3-70B"])
    with col_fy:
        fy_filter = st.selectbox("Filter FY", ["All Years", "FY25", "FY24", "FY23", "FY22"])
    with col_dt:
        dt_filter = st.selectbox("Document Type", ["All Types", "Annual Report", "Earnings Call Transcript", "Financial Statement"])
    with col_k:
        top_k = st.slider("Top-K Chunks", min_value=3, max_value=15, value=8)

    col_hyb, col_rerank, col_sim = st.columns(3)
    with col_hyb:
        hybrid_search = st.toggle("Hybrid Search (Dense + Sparse)", value=True)
    with col_rerank:
        reranking = st.toggle("BGE Cross-Encoder Reranking", value=False)
    with col_sim:
        min_sim = st.slider("Min Similarity Cutoff", 0.0, 0.8, 0.0, 0.05)

# Clear Conversation Action
col_title, col_btn = st.columns([4, 1])
with col_btn:
    if st.button("🔄 New Research Session", use_container_width=True):
        st.session_state["session_id"] = str(uuid.uuid4())
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Started a new research session. Ask any financial question.",
                "citations": [],
                "route": "RAG_FINANCIAL_QA",
            }
        ]
        st.rerun()

# Display Conversation History
for msg in st.session_state["chat_messages"]:
    role = msg.get("role", "assistant")
    with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🤖"):
        # If assistant has a routed category
        if role == "assistant" and msg.get("route"):
            render_route_pill(msg.get("route"), msg.get("confidence", 0.95))

        st.markdown(msg.get("content", ""))

        # Render Citations Expander if citations exist
        citations = msg.get("citations", [])
        if citations:
            render_citations_expander(citations)

# User Chat Input
user_query = st.chat_input("E.g. What were the key revenue drivers and EBITDA margins in FY24? Any debt covenants mentioned?")

if user_query:
    # 1. Add User Message
    st.session_state["chat_messages"].append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)

    # 2. Get active company
    cid = st.session_state.get("selected_company_id")
    fy_arg = None if fy_filter == "All Years" else fy_filter
    dt_arg = None if dt_filter == "All Types" else dt_filter

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing filings & synthesizing grounded response..."):
            response = chat_rag(
                session_id=st.session_state["session_id"],
                user_query=user_query,
                company_id=cid,
                financial_year=fy_arg,
                document_type=dt_arg,
                top_k=top_k,
                hybrid=hybrid_search,
                reranking=reranking,
            )

            if "error" in response:
                st.error(f"Error querying research engine: {response['error']}")
                assistant_text = f"Apologies, an error occurred during research synthesis: {response['error']}"
                citations = []
                route = "ERROR"
            else:
                assistant_text = response.get("content", "No response generated.")
                citations = response.get("citations", [])
                route = response.get("route", "RAG_FINANCIAL_QA")

                render_route_pill(route)
                st.markdown(assistant_text)

                if citations:
                    render_citations_expander(citations)

            # Persist in session state
            st.session_state["chat_messages"].append({
                "role": "assistant",
                "content": assistant_text,
                "citations": citations,
                "route": route,
            })

