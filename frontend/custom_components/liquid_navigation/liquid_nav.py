"""
ALPHANEXUS – Custom Liquid Navigation Component
===============================================
Streamlit custom component wrapper providing fluid translucent animated navigation.
"""
import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "liquid_navigation",
        path=os.path.abspath(os.path.dirname(__file__)),
    )
else:
    _component_func = None


def liquid_navigation(items=None, active_item=None, key=None):
    """Render interactive Liquid Navigation bar."""
    if _component_func:
        return _component_func(items=items or [], active_item=active_item, key=key, default=active_item)
    return active_item

