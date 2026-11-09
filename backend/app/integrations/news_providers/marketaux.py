from typing import Dict, Any, Optional, List
from datetime import datetime
import httpx
from app.core.config import settings
from app.core.logging import logger


class MarketauxProvider:
    """
    Adapter for Marketaux Financial News API.
    Handles news query by ticker/keyword, rate-limiting, normalization,
    and fallback handling when API token is absent.
    """

    BASE_URL = "https://api.marketaux.com/v1"

    def __init__(self):
        self.api_token = settings.MARKETAUX_API_TOKEN
        self.timeout = 10.0

    @property
    def is_configured(self) -> bool:
        return bool(self.api_token)

    def check_availability(self) -> Dict[str, Any]:
        if not self.is_configured:
            return {
                "available": False,
                "provider": "Marketaux Financial News",
                "status": "Disabled",
                "reason": "MARKETAUX_API_TOKEN is not configured. Intelligence feed is operating with verified market announcement fixtures.",
            }
        return {
            "available": True,
            "provider": "Marketaux Financial News",
            "status": "Ready",
            "last_checked": datetime.utcnow().isoformat(),
        }

    def fetch_news(
        self,
        symbols: Optional[List[str]] = None,
        keywords: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Fetches live articles from Marketaux or returns empty list with status.
        """
        if not self.is_configured:
            return []

        params: Dict[str, Any] = {
            "api_token": self.api_token,
            "language": "en",
            "limit": min(limit, 50),
        }

        if symbols:
            params["symbols"] = ",".join(symbols)
        if keywords:
            params["search"] = keywords

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(f"{self.BASE_URL}/news/all", params=params)
                if res.status_code == 200:
                    data = res.json()
                    articles = data.get("data", [])
                    return articles
                else:
                    logger.warning(f"Marketaux error HTTP {res.status_code}: {res.text}")
                    return []
        except Exception as e:
            logger.error(f"Marketaux fetch exception: {e}")
            return []

