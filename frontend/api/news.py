"""
EquiLens AI – News & Corporate Events API Module
================================================
Fetches real-time financial news, classified events, and corporate actions.
"""

from typing import Any, Dict, List, Optional
from api.client import api_client


def get_news(company_id: Optional[str] = None) -> List[Dict[str, Any]]:
    res = api_client.get("news")
    if isinstance(res, list):
        if company_id:
            return [n for n in res if str(n.get("company_id")) == str(company_id)]
        return res
    if isinstance(res, dict) and "error" not in res:
        items = res.get("items", [])
        if company_id:
            return [n for n in items if str(n.get("company_id")) == str(company_id)]
        return items
    return []


def get_corporate_actions(company_id: Optional[str] = None) -> List[Dict[str, Any]]:
    if company_id:
        res = api_client.get(f"corporate-actions/companies/{company_id}/corporate-actions")
    else:
        res = api_client.get("corporate-actions")
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and "error" not in res:
        return res.get("items", [])
    return []


def get_market_events(company_id: Optional[str] = None) -> List[Dict[str, Any]]:
    if company_id:
        res = api_client.get(f"market-events/companies/{company_id}/market-events")
    else:
        res = api_client.get("market-events")
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and "error" not in res:
        return res.get("items", [])
    return []

