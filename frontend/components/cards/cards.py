"""
ALPHANEXUS – Liquid Glass Card Components
"""
from typing import Optional
import streamlit as st


def render_metric_card(
    title: str,
    value: str,
    subtitle: Optional[str] = None,
    delta: Optional[str] = None,
    delta_type: str = "positive",
):
    """Render a modern translucent metric card with glassmorphic depth."""
    delta_class = "metric-delta-pos" if delta_type == "positive" else "metric-delta-neg"
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    sub_html = f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ""

    st.markdown(
        f"""
        <div class="glass-card metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
