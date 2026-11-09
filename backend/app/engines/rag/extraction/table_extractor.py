"""
ALPHANEXUS – Financial Table Extractor
======================================
Detects, parses, and converts balance sheet, income, and cash flow tables into markdown.
"""

from typing import List, Dict, Any


def format_table_as_markdown(table_rows: List[List[str]]) -> str:
    """Formats raw 2D string matrix into Markdown table with aligned headers."""
    if not table_rows or len(table_rows) < 1:
        return ""

    headers = [str(c).strip().replace("\n", " ") for c in table_rows[0]]
    hdr_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"

    body_lines = []
    for row in table_rows[1:]:
        # Pad row if incomplete
        cells = [str(c).strip().replace("\n", " ") for c in row]
        while len(cells) < len(headers):
            cells.append("")
        body_lines.append("| " + " | ".join(cells[:len(headers)]) + " |")

    return f"\n{hdr_line}\n{sep_line}\n" + "\n".join(body_lines) + "\n"
