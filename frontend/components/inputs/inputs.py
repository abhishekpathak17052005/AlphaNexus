"""
ALPHANEXUS – Input Components
"""
import streamlit as st


def render_search_input(placeholder: str = "Search companies by NSE symbol or name...", key: str = "global_search") -> str:
    """Render a search input field with glass styling."""
    return st.text_input("", placeholder=placeholder, key=key, label_visibility="collapsed")
