"""
ALPHANEXUS – Liquid Glass Top Navbar Component
"""
import streamlit as st
from config.settings import APP_NAME, APP_TAGLINE, BENCHMARK_INDICES


def render_navbar():
    """Render the top Liquid Glass navigation header with live market ticker."""
    indices_html = "".join([
        f'<span class="ticker-item"><span class="ticker-name">{idx["name"]}</span> '
        f'<span class="ticker-price">{idx["base_price"]:,.2f}</span> '
        f'<span class="{"ticker-pos" if idx["change"] >= 0 else "ticker-neg"}">'
        f'{"▲" if idx["change"] >= 0 else "▼"} {abs(idx["change"]):.2f} ({idx["pchange"]}%)</span></span>'
        for idx in BENCHMARK_INDICES
    ])

    st.markdown(
        f"""
        <div class="glass-navbar">
            <div class="navbar-brand">
                <span class="brand-title">⚡ {APP_NAME}</span>
                <span class="brand-tagline">{APP_TAGLINE}</span>
            </div>
            <div class="navbar-ticker">
                {indices_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
