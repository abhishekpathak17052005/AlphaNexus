"""
ALPHANEXUS – Request Processing Middleware
==========================================
Instruments request duration, security headers, correlation IDs, and unhandled exception guards.
"""

import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Measures request latency and injects X-Process-Time and X-Request-ID headers."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.monotonic()

        try:
            response = await call_next(request)
            duration_ms = (time.monotonic() - start_time) * 1000
            response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            duration_ms = (time.monotonic() - start_time) * 1000
            logger.error(f"[Middleware] Unhandled exception on {request.method} {request.url.path}: {exc} (took {duration_ms:.2f}ms)")
            raise
