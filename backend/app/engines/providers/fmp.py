from typing import Dict, Any, Optional
from datetime import datetime
import httpx
from app.core.config import settings
from app.core.logging import logger


class FMPProvider:
    """
    Adapter for Financial Modeling Prep (FMP) fundamentals API.
    Uses the modern /stable endpoints with comprehensive error reporting
    and explicit detection of subscription tier limitations for Indian equities.
    """

    BASE_URL = "https://financialmodelingprep.com/stable"

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

    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieves company profile information.
        Distinguishes global equities (HTTP 200) from Indian exchange restrictions (HTTP 402).
        """
        if not self.is_configured:
            return {"is_live": False, "error": "FMP_API_KEY is not configured"}

        url = f"{self.BASE_URL}/profile"
        params = {"symbol": symbol, "apikey": self.api_key}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    if isinstance(data, list) and data:
                        return {"is_live": True, "symbol": symbol, "data": data[0]}
                    return {"is_live": False, "symbol": symbol, "error": "No profile data returned"}
                elif res.status_code == 402:
                    return {
                        "is_live": False,
                        "symbol": symbol,
                        "error": "HTTP 402: Indian Equities (.NS/.BO) are premium query parameters not included in current subscription tier.",
                    }
                else:
                    return {
                        "is_live": False,
                        "symbol": symbol,
                        "error": f"FMP API returned HTTP {res.status_code}: {res.text[:120]}",
                    }
        except Exception as e:
            logger.error(f"FMP profile request error for {symbol}: {e}")
            return {"is_live": False, "symbol": symbol, "error": str(e)}

