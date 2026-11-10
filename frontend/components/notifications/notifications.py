"""
ALPHANEXUS – Notification Alerts Component
"""
import streamlit as st


def show_toast(message: str, icon: str = "⚡"):
    """Display an inline toast notification."""
    st.toast(f"{icon} {message}")


def render_banner(message: str, level: str = "info"):
    """Display a glass alert banner."""
    if level == "success":
        st.success(message)
    elif level == "warning":
        st.warning(message)
    elif level == "error":
        st.error(message)
    else:
        st.info(message)

