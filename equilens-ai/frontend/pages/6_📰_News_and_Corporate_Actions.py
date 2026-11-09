"""
EquiLens AI – Page 6: News & Corporate Actions Intelligence
===========================================================
Marketaux news feed, sentiment analytics, and corporate actions calendar.
"""

import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.metrics import render_kpi_card
from components.charts import create_sentiment_donut_chart
from api.news import get_news, get_corporate_actions, get_market_events

render_sidebar()

comp_obj = st.session_state.get("selected_company_obj")
cid = comp_obj.get("id") if comp_obj else None
symbol = comp_obj.get("symbol", "ALL") if comp_obj else "ALL"
name = comp_obj.get("name", "All Tracked Equities") if comp_obj else "All Tracked Equities"

st.title(f"📰 News & Corporate Actions Intelligence — {name} ({symbol})")
st.markdown("Automated financial news aggregation, sentiment NLP, and exchange corporate action filings.")

tab_news, tab_actions, tab_events = st.tabs(["🗞️ Market News & Sentiment", "📅 Corporate Actions Calendar", "🤝 Contracts & M&A Deals"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: NEWS & SENTIMENT
# ─────────────────────────────────────────────────────────────────────────────
with tab_news:
    try:
        articles = get_news(cid)
    except Exception:
        articles = []

    # Compute Sentiment Summary
    sent_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for a in articles:
        lbl = a.get("sentiment_label") or "Neutral"
        sent_counts[lbl.capitalize()] = sent_counts.get(lbl.capitalize(), 0) + 1

    col_chart, col_stats = st.columns([1, 1])
    with col_chart:
        if sum(sent_counts.values()) > 0:
            fig_sent = create_sentiment_donut_chart(sent_counts)
            st.plotly_chart(fig_sent, use_container_width=True)
        else:
            st.info("No sentiment metrics available for current filter.")

    with col_stats:
        st.subheader("Sentiment Summary")
        s1, s2, s3 = st.columns(3)
        with s1:
            render_kpi_card("Bullish / Positive", str(sent_counts.get("Positive", 0)), is_positive=True)
        with s2:
            render_kpi_card("Neutral", str(sent_counts.get("Neutral", 0)))
        with s3:
            render_kpi_card("Bearish / Negative", str(sent_counts.get("Negative", 0)), is_positive=False)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📰 Recent Headlines & Event Classifications")

    if articles:
        for art in articles[:10]:
            sent_lbl = art.get("sentiment_label", "Neutral").capitalize()
            sent_color = "#10b981" if sent_lbl == "Positive" else ("#f43f5e" if sent_lbl == "Negative" else "#94a3b8")
            evt_type = art.get("event_type", "General News")
            title = art.get("title", "News Announcement")
            desc = art.get("description") or art.get("snippet") or ""
            source = art.get("source", "Financial News")
            published = str(art.get("published_at", ""))[:16]

            st.markdown(
                f"""
                <div style="background: #111827; border: 1px solid #1f2937; border-left: 4px solid {sent_color}; border-radius: 6px; padding: 1rem; margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <span style="font-size: 0.75rem; color: #38bdf8; font-weight: bold; text-transform: uppercase;">{evt_type} • {source}</span>
                        <span style="font-size: 0.75rem; color: {sent_color}; font-weight: bold;">{sent_lbl}</span>
                    </div>
                    <div style="font-size: 1rem; font-weight: 600; color: #f9fafb; margin-bottom: 0.3rem;">{title}</div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.4;">{desc}</div>
                    <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.4rem;">Published: {published}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No recent news articles ingested for this company.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: CORPORATE ACTIONS
# ─────────────────────────────────────────────────────────────────────────────
with tab_actions:
    st.subheader("📅 Exchange Corporate Actions Filings")
    try:
        actions = get_corporate_actions(cid)
    except Exception:
        actions = []

    if actions:
        act_rows = []
        for a in actions:
            act_rows.append({
                "Action Type": a.get("action_type"),
                "Announcement Date": str(a.get("announcement_date", ""))[:10],
                "Ex-Date": str(a.get("ex_date", ""))[:10],
                "Record Date": str(a.get("record_date", ""))[:10],
                "Details / Value": a.get("details") or f"₹{a.get('dividend_amount', '')}",
            })
        st.dataframe(pd.DataFrame(act_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No upcoming or historical corporate actions on record for this company.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: CONTRACTS & DEALS
# ─────────────────────────────────────────────────────────────────────────────
with tab_events:
    st.subheader("🤝 Material Contracts, Mergers & Major Deals")
    try:
        events = get_market_events(cid)
    except Exception:
        events = []

    if events:
        evt_rows = []
        for e in events:
            evt_rows.append({
                "Event Type": e.get("event_type"),
                "Title": e.get("title"),
                "Deal Value": e.get("deal_value") or "Not Disclosed",
                "Date": str(e.get("event_date", ""))[:10],
                "Counterparty": e.get("counterparty") or "N/A",
            })
        st.dataframe(pd.DataFrame(evt_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No major contract or M&A filings on record for this security.")

