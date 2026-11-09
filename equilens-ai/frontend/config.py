"""
EquiLens AI – Streamlit Frontend Configuration
===============================================
Central configuration for API endpoints, UI themes, and Indian market settings.
"""

import os

# FastAPI Backend Configuration
BACKEND_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_V1_PREFIX = "/api/v1"
BACKEND_API_URL = f"{BACKEND_BASE_URL}{API_V1_PREFIX}"

# App Identity
APP_NAME = "EquiLens AI"
APP_TAGLINE = "See Beyond the Stock Price."
APP_VERSION = "2.0.0"

# Indian Market Defaults
BENCHMARK_INDICES = [
    {"symbol": "^NSEI", "name": "Nifty 50", "base_price": 24150.00, "change": 142.50, "pchange": 0.59},
    {"symbol": "^BSESN", "name": "BSE Sensex", "base_price": 79480.00, "change": 450.20, "pchange": 0.57},
    {"symbol": "^NSEBANK", "name": "Nifty Bank", "base_price": 51800.00, "change": -85.40, "pchange": -0.16},
    {"symbol": "^CNXIT", "name": "Nifty IT", "base_price": 42120.00, "change": 310.80, "pchange": 0.74},
]

# Supported Document Formats
ALLOWED_UPLOAD_EXTENSIONS = ["pdf", "docx", "doc", "xlsx", "xls", "csv", "txt", "md"]
MAX_UPLOAD_SIZE_MB = 100

# UI Settings
DEFAULT_PAGE_ICON = "📈"
DEFAULT_PAGE_LAYOUT = "wide"
DEFAULT_EXPAND_SIDEBAR = True

