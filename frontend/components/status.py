"""
EquiLens AI – Status Indicators Component
=========================================
Renders real-time engine health pills, latency badges, and system status banners.
"""

import streamlit as st
from typing import Dict, Any


def render_engine_health_badge(engine_name: str, status: str, latency_ms: float = 0.0):
    status_lower = status.lower()
    if "healthy" in status_lower or "connected" in status_lower or "live" in status_lower or "active" in status_lower:
        pill_cls = "status-active"
        dot = "🟢"
    elif "degraded" in status_lower or "fallback" in status_lower:
        pill_cls = "status-degraded"
        dot = "🟡"
    else:
        pill_cls = "status-error"
        dot = "🔴"

    latency_str = f" ({latency_ms:.0f}ms)" if latency_ms > 0 else ""
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0.6rem; background: #1e293b; border-radius: 6px; margin-bottom: 0.4rem;">
            <span style="font-size: 0.82rem; font-weight: 500; color: #cbd5e1;">{engine_name}</span>
            <span class="status-pill {pill_cls}">{dot} {status}{latency_str}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_route_pill(route_name: str, confidence: float = 1.0):
    st.markdown(
        f"""
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
            <span style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Orchestrated Route:</span>
            <span class="route-badge">⚡ {route_name.upper()}</span>
            <span style="font-size: 0.75rem; color: #64748b;">(Confidence: {confidence * 100:.0f}%)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

