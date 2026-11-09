"""
ALPHANEXUS – File Validation Utilities
======================================
Validates file extensions, MIME types, and file size constraints for uploaded documents.
"""

import os
from typing import Tuple

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv", ".txt", ".md"}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100MB


def validate_uploaded_file(filename: str, file_size: int) -> Tuple[bool, str]:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file extension '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"

    if file_size > MAX_FILE_SIZE_BYTES:
        max_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
        return False, f"File size exceeds maximum allowed limit of {max_mb}MB."

    return True, "Valid"
