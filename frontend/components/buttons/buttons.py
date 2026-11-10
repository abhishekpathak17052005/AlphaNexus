"""
ALPHANEXUS – Button Components
"""
import streamlit as st


def render_action_button(label: str, key: str, on_click=None, help_text=None) -> bool:
    """Render a styled primary glass action button."""
    return st.button(label, key=key, on_click=on_click, help=help_text, type="primary")

