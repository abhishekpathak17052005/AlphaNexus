"""
ALPHANEXUS – Text Processing Utilities
======================================
Cleaning, whitespace normalization, and tabular text formatting.
"""

import re


def clean_financial_text(text: str) -> str:
    """Normalizes whitespace and removes artifact characters while preserving table structures."""
    if not text:
        return ""
    # Normalize unicode spaces
    text = text.replace("\u00a0", " ").replace("\u200b", "")
    # Remove repeated blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_numerical_tokens(text: str) -> list[str]:
    """Finds currency figures, percentages, and numerical quantities in text."""
    pattern = r"(?:₹|\$|Rs\.?|INR)?\s*[-+]?\d{1,3}(?:,\d{2,3})*(?:\.\d+)?\s*(?:Cr|Crore|Lakh|M|B|%|bps)?"
    return [m.group(0).strip() for m in re.finditer(pattern, text) if any(c.isdigit() for c in m.group(0))]
