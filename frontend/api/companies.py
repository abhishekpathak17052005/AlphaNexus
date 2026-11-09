"""
EquiLens AI – Companies API Module
==================================
Interfaces with FastAPI /companies endpoints for Indian equities (NSE/BSE).
"""

from typing import Any, Dict, List, Optional
from api.client import api_client


def get_companies(query: Optional[str] = None, sector: Optional[str] = None) -> List[Dict[str, Any]]:
    params = {}
    if query:
        params["query"] = query
    if sector:
        params["sector"] = sector
    res = api_client.get("companies", params=params)
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and "error" not in res:
        return res.get("items", [])
    return []


def get_company(company_id: str) -> Optional[Dict[str, Any]]:
    res = api_client.get(f"companies/{company_id}")
    if isinstance(res, dict) and "error" not in res:
        return res
    return None


def get_company_price(company_id: str) -> Optional[Dict[str, Any]]:
    res = api_client.get(f"companies/{company_id}/price")
    if isinstance(res, dict) and "error" not in res:
        return res
    return None

