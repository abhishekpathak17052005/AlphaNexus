"""
EquiLens AI – Documents API Module
==================================
Handles document upload, ingestion status tracking, and chunk inspection.
"""

from typing import Any, Dict, List, Optional
from api.client import api_client


def get_documents(company_id: Optional[str] = None) -> List[Dict[str, Any]]:
    params = {}
    if company_id:
        params["company_id"] = company_id
    res = api_client.get("rag/documents", params=params)
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and "error" not in res:
        return res.get("items", [])
    return []


def get_document(document_id: str) -> Optional[Dict[str, Any]]:
    res = api_client.get(f"rag/documents/{document_id}")
    if isinstance(res, dict) and "error" not in res:
        return res
    return None


def get_document_stats(document_id: str) -> Optional[Dict[str, Any]]:
    res = api_client.get(f"rag/documents/{document_id}/stats")
    if isinstance(res, dict) and "error" not in res:
        return res
    return None


def upload_document(
    file_bytes: bytes,
    filename: str,
    company_id: str,
    document_type: str = "Annual Report",
    financial_year: str = "FY24",
    quarter: Optional[str] = None,
) -> Dict[str, Any]:
    files = {"file": (filename, file_bytes)}
    data = {
        "company_id": str(company_id),
        "document_type": document_type,
        "financial_year": financial_year,
    }
    if quarter:
        data["quarter"] = quarter

    return api_client.post("rag/documents/upload", files=files, data=data)


def process_document(document_id: str) -> Dict[str, Any]:
    return api_client.post(f"rag/documents/{document_id}/process")


def delete_document(document_id: str) -> Dict[str, Any]:
    return api_client.delete(f"rag/documents/{document_id}")

