import re
import hashlib
from typing import List, Dict, Any, Tuple
from app.core.logging import logger


class DocumentPreprocessor:
    """
    Cleans raw document inputs, handles text normalization,
    identifies document types, and preserves tabular and section structure.
    """

    @staticmethod
    def compute_file_hash(content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    @staticmethod
    def normalize_text(text: str) -> str:
        """Removes abnormal whitespace while preserving paragraph and line structure."""
        if not text:
            return ""
        # Normalize non-breaking spaces and irregular characters
        text = text.replace("\u00a0", " ").replace("\r\n", "\n").replace("\r", "\n")
        # Collapse multi-spaces on a line
        text = re.sub(r"[ \t]+", " ", text)
        # Collapse more than 3 consecutive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def is_empty_page(text: str, tables: List[Any]) -> bool:
        clean = text.strip()
        has_tables = bool(tables and len(tables) > 0)
        return len(clean) < 20 and not has_tables

    @staticmethod
    def infer_document_type(title_or_filename: str, first_pages_text: str) -> str:
        combined = f"{title_or_filename} {first_pages_text}".lower()
        if any(k in combined for k in ["annual report", "integrated annual report", "form 10-k"]):
            return "Annual Report"
        if any(k in combined for k in ["investor presentation", "presentation to investors", "earnings deck"]):
            return "Investor Presentation"
        if any(k in combined for k in ["earnings conference call", "earnings call transcript", "concall"]):
            return "Earnings Call Transcript"
        if any(k in combined for k in ["financial results", "quarterly results", "q1", "q2", "q3", "q4"]):
            return "Quarterly Results"
        if any(k in combined for k in ["credit rating", "crisil", "icra", "care"]):
            return "Credit Rating"
        if any(k in combined for k in ["board meeting", "outcome of board meeting"]):
            return "Board Meeting Disclosure"
        return "Company Filing"

    @staticmethod
    def format_table_as_markdown(table_rows: List[List[str]]) -> str:
        """Converts extracted table rows to a readable Markdown table format."""
        if not table_rows:
            return ""
        try:
            # Header
            header = table_rows[0]
            header_line = "| " + " | ".join(str(c).replace("\n", " ").strip() for c in header) + " |"
            sep_line = "| " + " | ".join(["---"] * len(header)) + " |"
            data_lines = []
            for row in table_rows[1:]:
                # Pad row to match header length
                padded = list(row) + [""] * (len(header) - len(row))
                line = "| " + " | ".join(str(c).replace("\n", " ").strip() for c in padded[:len(header)]) + " |"
                data_lines.append(line)
            return "\n".join([header_line, sep_line] + data_lines)
        except Exception:
            return ""

