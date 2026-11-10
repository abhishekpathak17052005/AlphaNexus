"""
ALPHANEXUS – General Helper Functions
=====================================
Common hashing, UUID conversion, and dictionary serialization helpers.
"""

import hashlib
import uuid
from typing import Any, Union


def compute_sha256(content: Union[bytes, str]) -> str:
    """Computes SHA-256 hash string for byte buffers or text."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def ensure_uuid(val: Any) -> uuid.UUID:
    """Safely converts string or UUID object to a UUID instance."""
    if isinstance(val, uuid.UUID):
        return val
    return uuid.UUID(str(val))

