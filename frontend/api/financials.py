"""
EquiLens AI – Financial Analytics API Module
============================================
Fetches structured financial statements, deterministic ratios, and metrics.
"""

from typing import Any, Dict, List, Optional
from api.client import api_client


def get_financials(company_id: str) -> List[Dict[str, Any]]:
    res = api_client.get(f"companies/{company_id}/financials")
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and "error" not in res:
        return res.get("items", [])
    return []


def get_statements(company_id: str, statement_type: Optional[str] = None) -> List[Dict[str, Any]]:
    params = {}
    if statement_type:
        params["statement_type"] = statement_type
    res = api_client.get(f"companies/{company_id}/statements", params=params)
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and "error" not in res:
        return res.get("items", [])
    return []


def get_ratios(company_id: str) -> Optional[Dict[str, Any]]:
    res = api_client.get(f"companies/{company_id}/ratios")
    if isinstance(res, dict) and "error" not in res:
        return res
    return None


def compare_companies(company_ids: List[str]) -> Optional[Dict[str, Any]]:
    payload = {"company_ids": company_ids}
    res = api_client.post("companies/compare", json_data=payload)
    if isinstance(res, dict) and "error" not in res:
        return res
    return None

