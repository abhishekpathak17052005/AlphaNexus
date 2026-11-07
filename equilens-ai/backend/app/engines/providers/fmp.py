from typing import Dict, Any, Optional
from datetime import datetime
import httpx
from app.core.config import settings
from app.core.logging import logger


class FMPProvider:
    """
    Adapter for Financial Modeling Prep (FMP) fundamentals API.
    Provides income statements, balance sheets, and cash flow data.
    """

    BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self):
        self.api_key = settings.FMP_API_KEY
        self.timeout = 10.0

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def check_availability(self) -> Dict[str, Any]:
        if not self.is_configured:
            return {
                "available": False,
                "provider": "Financial Modeling Prep (FMP)",
                "status": "Disabled",
                "reason": "FMP_API_KEY is not configured.",
            }
        return {
            "available": True,
            "provider": "Financial Modeling Prep (FMP)",
            "status": "Ready",
            "last_checked": datetime.utcnow().isoformat(),
        }

