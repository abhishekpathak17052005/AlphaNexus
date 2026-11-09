"""
EquiLens AI – HTTP API Client
==============================
Centralized HTTP client wrapping httpx with timeouts, error interceptors, and fallback handling.
"""

from typing import Any, Dict, Optional, Union
import httpx
from config import BACKEND_API_URL


class APIClient:
    """
    Robust HTTP client for FastAPI backend communication.
    """

    def __init__(self, base_url: str = BACKEND_API_URL, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}", "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                if files:
                    resp = client.post(url, params=params, files=files, data=data)
                else:
                    resp = client.post(url, params=params, json=json_data)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}", "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.put(url, json=json_data)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}", "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    def delete(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.delete(url)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}", "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e), "status_code": 500}


api_client = APIClient()

