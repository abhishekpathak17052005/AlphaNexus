"""
ALPHANEXUS – Table Components
"""
import streamlit as st
import pandas as pd


def render_glass_dataframe(df: pd.DataFrame, use_container_width: bool = True):
    """Render a clean DataFrame within the Liquid Glass theme."""
    st.dataframe(df, use_container_width=use_container_width)

