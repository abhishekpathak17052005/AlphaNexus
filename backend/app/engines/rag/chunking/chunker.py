"""
EquiLens AI – Financial-Domain Hierarchical Chunking Engine
===========================================================
Implements 7 document-type-specific chunking strategies:

  A. Annual Reports     – section-aware + semantic (500-700 tokens)
  B. Financial Stmts   – statement-aware (preserve headers/periods/units)
  C. Management Disc.  – heading-based semantic (600-800 tokens)
  D. Earnings Calls    – speaker-aware, Q&A boundaries (400-600 tokens)
  E. Investor Pres.    – slide-aware with key metrics (400-600 tokens)
  F. Corporate Announcements – event-aware, compact (200-400 tokens)
  G. Financial Tables  – always atomic, never split

Parent-child relationship:
  Parent = full section / page
  Children = overlapping sub-chunks for fine retrieval

All chunks carry rich financial metadata:
  company, ticker, financial_year, quarter, document_type,
  section_hierarchy, page_number, currency, unit,
  consolidated/standalone, chunk_type, statement_type
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

from app.engines.rag.preprocessor import DocumentPreprocessor


# ---------------------------------------------------------------------------
# Chunking configuration
# ---------------------------------------------------------------------------

@dataclass
class ChunkingConfig:
    """Per-document-type chunking parameters."""
    target_tokens: int = 600
    min_tokens: int = 80
    max_tokens: int = 1200
    overlap_tokens: int = 100
    # Strategy flags
    section_aware: bool = True
    semantic_split: bool = True
    table_aware: bool = True
    parent_child: bool = True
    speaker_aware: bool = False
    slide_aware: bool = False
    statement_aware: bool = False
    event_aware: bool = False
    dedup: bool = True


# Strategy presets by document type
_STRATEGY_MAP: Dict[str, ChunkingConfig] = {
    "annual report":              ChunkingConfig(600, 80, 1200, 100, section_aware=True,  semantic_split=True,  table_aware=True,  parent_child=True),
    "annual_report":              ChunkingConfig(600, 80, 1200, 100, section_aware=True,  semantic_split=True,  table_aware=True,  parent_child=True),
    "quarterly result":           ChunkingConfig(400, 60, 900,  80,  section_aware=True,  statement_aware=True, table_aware=True,  parent_child=False),
    "financial statement":        ChunkingConfig(400, 60, 900,  80,  statement_aware=True, table_aware=True,    section_aware=False),
    "balance sheet":              ChunkingConfig(350, 40, 800,  60,  statement_aware=True, table_aware=True),
    "management discussion":      ChunkingConfig(700, 100, 1200, 100, section_aware=True,  semantic_split=True,  parent_child=True),
    "earnings call transcript":   ChunkingConfig(500, 80, 1000, 80,  speaker_aware=True,  section_aware=True),
    "investor presentation":      ChunkingConfig(500, 60, 1000, 80,  slide_aware=True,    table_aware=True),
    "corporate announcement":     ChunkingConfig(300, 40, 700,  50,  event_aware=True,    section_aware=False),
    "research report":            ChunkingConfig(600, 80, 1200, 100, section_aware=True,  semantic_split=True),
    "regulatory disclosure":      ChunkingConfig(400, 60, 900,  80,  section_aware=True),
    "default":                    ChunkingConfig(600, 80, 1200, 100),
}

# Financial statement section identifiers
_STATEMENT_KEYWORDS = {
    "income_statement": [
        "profit and loss", "income statement", "statement of operations",
        "p&l", "revenue", "total income", "net profit", "earnings before",
        "ebitda", "operating profit",
    ],
    "balance_sheet": [
        "balance sheet", "statement of financial position", "assets",
        "liabilities", "shareholders equity", "net worth",
    ],
    "cash_flow": [
        "cash flow", "statement of cash flows", "operating activities",
        "investing activities", "financing activities",
    ],
    "segment": [
        "segment report", "segment information", "business segment",
        "geographic segment",
    ],
    "notes": [
        "notes to", "note no", "accounting policies", "significant accounting",
        "contingent liabilities",
    ],
}

# Annual report section patterns
_ANNUAL_REPORT_SECTIONS = [
    "company overview", "business model", "business segments",
    "management discussion", "management's discussion", "financial highlights",
    "risk factors", "risk management", "corporate governance",
    "auditor's report", "independent auditor", "directors' report",
    "future outlook", "outlook", "esg", "sustainability",
    "chairman", "managing director", "subsidiaries",
    "consolidated financial", "standalone financial",
]

# Heading detection regex
_HEADING_RE = re.compile(
    r"""^(
        (?:\d+[\.\)]\s+)|        # 1. or 1)
        (?:[A-Z][A-Z\s\-&/]{4,})|  # ALL CAPS title
        (?:(?:Note|Section|Item|Part|Chapter|Schedule)\s+[\dA-Z])   # Note 5
    )""",
    re.VERBOSE,
)

# Speaker pattern for earnings calls
_SPEAKER_RE = re.compile(
    r"^(?P<name>[A-Z][a-z]+ [A-Z][a-z]+)"
    r"(?:\s*[–—-]\s*(?P<role>[A-Za-z &]+))?\s*:?\s*$",
    re.MULTILINE,
)

# Slide/page heading pattern
_SLIDE_RE = re.compile(
    r"^(?:Slide|Page)\s+\d+[\.:]\s+",
    re.IGNORECASE | re.MULTILINE,
)


# ---------------------------------------------------------------------------
# Main chunker class
# ---------------------------------------------------------------------------

class FinancialDocumentChunker:
    """
    Replaces the original flat DocumentChunker with a document-type-aware
    hierarchical chunking engine.
    Backwards-compatible: call chunk_document() with the same signature.
    """

    def __init__(
        self,
        chunk_size: int = 900,          # kept for compatibility; overridden by strategy
        chunk_overlap: int = 120,
    ):
        self._default_size = chunk_size
        self._default_overlap = chunk_overlap

    # ------------------------------------------------------------------
    # Public entry point (backwards-compatible signature)
    # ------------------------------------------------------------------

    def chunk_document(
        self,
        pages_data: List[Dict[str, Any]],
        company_id: str,
        document_id: str,
        company_symbol: str = "",
        financial_year: str = "",
        document_type: str = "",
        quarter: Optional[str] = None,
        ticker: Optional[str] = None,
        exchange: Optional[str] = None,
        currency: str = "INR",
        unit: str = "Crores",
        is_consolidated: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Dispatch to the appropriate strategy based on document_type.
        Returns a flat list of chunk dicts compatible with VectorStore.store_chunks().
        """
        doc_type_key = (document_type or "default").lower().strip()
        config = _STRATEGY_MAP.get(doc_type_key, _STRATEGY_MAP["default"])

        # Common metadata carried in every chunk
        base_meta = {
            "company_symbol": company_symbol or ticker,
            "ticker": ticker or company_symbol,
            "exchange": exchange,
            "financial_year": financial_year,
            "quarter": quarter,
            "document_type": document_type,
            "currency": currency,
            "unit": unit,
            "is_consolidated": is_consolidated,
        }

        # Route to strategy
        if config.statement_aware or doc_type_key in ("financial statement", "balance sheet", "quarterly result"):
            raw_chunks = self._chunk_financial_statements(
                pages_data, config, base_meta, document_id, company_id
            )
        elif config.speaker_aware:
            raw_chunks = self._chunk_earnings_call(
                pages_data, config, base_meta, document_id, company_id
            )
        elif config.slide_aware:
            raw_chunks = self._chunk_investor_presentation(
                pages_data, config, base_meta, document_id, company_id
            )
        elif config.event_aware:
            raw_chunks = self._chunk_corporate_announcement(
                pages_data, config, base_meta, document_id, company_id
            )
        else:
            # Generic section-aware strategy (Annual Report, MDA, Research)
            raw_chunks = self._chunk_section_aware(
                pages_data, config, base_meta, document_id, company_id
            )

        # Add table chunks (always atomic, regardless of strategy)
        table_chunks = self._extract_table_chunks(
            pages_data, base_meta, document_id, company_id
        )

        all_chunks = table_chunks + raw_chunks

        # Re-index and optionally dedup
        if config.dedup:
            all_chunks = self._deduplicate(all_chunks)

        for i, c in enumerate(all_chunks):
            c["chunk_index"] = i

        return all_chunks

    # ------------------------------------------------------------------
    # Strategy A/C/H – Section-aware (Annual Reports, MDA, Research)
    # ------------------------------------------------------------------

    def _chunk_section_aware(
        self,
        pages_data: List[Dict[str, Any]],
        config: ChunkingConfig,
        base_meta: Dict[str, Any],
        document_id: str,
        company_id: str,
    ) -> List[Dict[str, Any]]:
        chunks: List[Dict[str, Any]] = []
        section_hierarchy: List[str] = ["Document Start"]
        buffer_tokens: List[str] = []
        buf_len = 0
        current_page = 1
        section_start_page = 1

        def flush(section_path: List[str], page: int) -> None:
            nonlocal buffer_tokens, buf_len
            if not buffer_tokens:
                return
            text = " ".join(buffer_tokens)
            # Only skip if genuinely too short (noise/headers)
            if len(text.strip()) < 20:
                return
            section_label = " > ".join(section_path[-3:])
            header = self._header(base_meta, page, section_label)
            chunks.append(self._make_chunk(
                document_id, company_id, text, header,
                section_label, page, "narrative",
                base_meta, config, section_hierarchy=list(section_path),
            ))

        for page in pages_data:
            page_num = page.get("page_number", 1)
            raw_text = page.get("text", "")
            if DocumentPreprocessor.is_empty_page(raw_text, page.get("tables", [])):
                continue

            normalized = DocumentPreprocessor.normalize_text(raw_text)
            paragraphs = normalized.split("\n\n")

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                para_len = len(para.split())

                # Heading detection
                if self._is_heading(para):
                    # Flush current buffer before starting a new section
                    flush(section_hierarchy, current_page)
                    buffer_tokens = []
                    buf_len = 0
                    # Update section hierarchy
                    depth = self._heading_depth(para)
                    if depth <= len(section_hierarchy):
                        section_hierarchy = section_hierarchy[:max(1, depth - 1)] + [para]
                    else:
                        section_hierarchy = section_hierarchy + [para]
                    section_start_page = page_num
                    current_page = page_num
                    continue

                if buf_len + para_len > config.target_tokens and buffer_tokens:
                    flush(section_hierarchy, current_page)
                    # Overlap: keep last overlap_tokens worth of text
                    overlap_words = []
                    wcount = 0
                    for word in reversed(" ".join(buffer_tokens).split()):
                        if wcount >= config.overlap_tokens:
                            break
                        overlap_words.insert(0, word)
                        wcount += 1
                    buffer_tokens = overlap_words + [para]
                    buf_len = len(buffer_tokens)
                else:
                    buffer_tokens.append(para)
                    buf_len += para_len

                current_page = page_num

        flush(section_hierarchy, current_page)
        return chunks

    # ------------------------------------------------------------------
    # Strategy B – Financial Statements (income, balance, cash-flow)
    # ------------------------------------------------------------------

    def _chunk_financial_statements(
        self,
        pages_data: List[Dict[str, Any]],
        config: ChunkingConfig,
        base_meta: Dict[str, Any],
        document_id: str,
        company_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Identify P&L / Balance Sheet / Cash Flow statement sections and
        keep each statement as a single chunk (never split across periods/columns).
        Narrative notes use the generic section-aware strategy.
        """
        chunks: List[Dict[str, Any]] = []
        full_text_pages: List[Tuple[int, str]] = []

        for page in pages_data:
            text = DocumentPreprocessor.normalize_text(page.get("text", ""))
            if text:
                full_text_pages.append((page.get("page_number", 1), text))

        # Build combined text with page markers
        combined = ""
        page_offsets: List[Tuple[int, int]] = []  # (char_offset, page_num)
        for pnum, pt in full_text_pages:
            page_offsets.append((len(combined), pnum))
            combined += pt + "\n\n"

        # Find statement boundaries
        statement_blocks = self._detect_statement_blocks(combined, page_offsets)

        for block in statement_blocks:
            header = self._header(base_meta, block["page"], block["statement_type"])
            meta = dict(base_meta)
            meta["statement_type"] = block["statement_type"]
            chunks.append(self._make_chunk(
                document_id, company_id,
                block["text"], header,
                block["statement_type"], block["page"],
                "statement_block", meta, config,
            ))

        # Also add narrative text chunks (notes, MD&A within financials)
        narrative = self._chunk_section_aware(pages_data, config, base_meta, document_id, company_id)
        chunks.extend(narrative)
        return chunks

    def _detect_statement_blocks(
        self, text: str, page_offsets: List[Tuple[int, int]]
    ) -> List[Dict[str, Any]]:
        blocks = []
        for stmt_type, keywords in _STATEMENT_KEYWORDS.items():
            for kw in keywords:
                idx = text.lower().find(kw)
                if idx == -1:
                    continue
                # Find the page number for this block
                page_num = 1
                for offset, pnum in reversed(page_offsets):
                    if idx >= offset:
                        page_num = pnum
                        break
                # Extract up to 1200 chars around the keyword
                start = max(0, idx - 100)
                end = min(len(text), idx + 1200)
                block_text = text[start:end].strip()
                if len(block_text.split()) >= 30:
                    blocks.append({
                        "statement_type": stmt_type,
                        "page": page_num,
                        "text": block_text,
                    })
                    break  # one block per statement type is enough
        return blocks

    # ------------------------------------------------------------------
    # Strategy D – Earnings Call Transcripts
    # ------------------------------------------------------------------

    def _chunk_earnings_call(
        self,
        pages_data: List[Dict[str, Any]],
        config: ChunkingConfig,
        base_meta: Dict[str, Any],
        document_id: str,
        company_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Split at speaker boundaries.  Each speaker turn becomes one chunk.
        Very long turns are further split with overlap.
        """
        full_text = "\n".join(
            DocumentPreprocessor.normalize_text(p.get("text", ""))
            for p in pages_data
        )
        # Split at speaker boundaries
        parts = re.split(r"(?=^[A-Z][a-z]+ [A-Z][a-z]+\s*[–—-])", full_text, flags=re.MULTILINE)
        chunks: List[Dict[str, Any]] = []
        page_num = 1

        for part in parts:
            part = part.strip()
            if len(part.split()) < config.min_tokens:
                continue
            # Extract speaker info
            speaker = "Unknown"
            role = ""
            m = re.match(r"^([A-Z][a-z]+ [A-Z][a-z]+)\s*[–—-]\s*([^\n]+)?", part)
            if m:
                speaker = m.group(1).strip()
                role = (m.group(2) or "").strip()

            meta = dict(base_meta)
            meta["speaker"] = speaker
            meta["speaker_role"] = role

            # Sub-split long turns
            sub_chunks = self._sliding_window(part, config.target_tokens, config.overlap_tokens)
            for i, sub in enumerate(sub_chunks):
                header = self._header(base_meta, page_num, f"Speaker: {speaker}")
                chunks.append(self._make_chunk(
                    document_id, company_id, sub, header,
                    f"Speaker: {speaker}", page_num, "earnings_turn",
                    meta, config,
                ))
        return chunks

    # ------------------------------------------------------------------
    # Strategy E – Investor Presentations
    # ------------------------------------------------------------------

    def _chunk_investor_presentation(
        self,
        pages_data: List[Dict[str, Any]],
        config: ChunkingConfig,
        base_meta: Dict[str, Any],
        document_id: str,
        company_id: str,
    ) -> List[Dict[str, Any]]:
        """Each page = one slide; chunk by page, sub-split if very long."""
        chunks: List[Dict[str, Any]] = []
        for page in pages_data:
            page_num = page.get("page_number", 1)
            text = DocumentPreprocessor.normalize_text(page.get("text", ""))
            if len(text.split()) < config.min_tokens:
                continue

            slide_title = f"Slide {page_num}"
            first_line = text.split("\n")[0].strip()
            if first_line and len(first_line) < 80:
                slide_title = first_line

            meta = dict(base_meta)
            meta["slide_number"] = page_num
            meta["slide_title"] = slide_title

            for sub in self._sliding_window(text, config.target_tokens, config.overlap_tokens):
                header = self._header(base_meta, page_num, slide_title)
                chunks.append(self._make_chunk(
                    document_id, company_id, sub, header,
                    slide_title, page_num, "slide", meta, config,
                ))
        return chunks

    # ------------------------------------------------------------------
    # Strategy F – Corporate Announcements
    # ------------------------------------------------------------------

    def _chunk_corporate_announcement(
        self,
        pages_data: List[Dict[str, Any]],
        config: ChunkingConfig,
        base_meta: Dict[str, Any],
        document_id: str,
        company_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Corporate announcements are typically short (<2 pages).
        Treat the full document as one chunk; sub-split if >max_tokens.
        Extract structured event fields into metadata.
        """
        full_text = " ".join(
            DocumentPreprocessor.normalize_text(p.get("text", ""))
            for p in pages_data
        ).strip()

        # Extract event metadata from text
        meta = dict(base_meta)
        meta["announcement_date"] = self._extract_date(full_text)
        meta["deal_value"] = self._extract_deal_value(full_text)
        meta["counterparty"] = self._extract_counterparty(full_text)

        chunks: List[Dict[str, Any]] = []
        for i, sub in enumerate(self._sliding_window(full_text, config.target_tokens, config.overlap_tokens)):
            header = self._header(base_meta, 1, "Corporate Announcement")
            chunks.append(self._make_chunk(
                document_id, company_id, sub, header,
                "Corporate Announcement", 1, "announcement", meta, config,
            ))
        return chunks

    # ------------------------------------------------------------------
    # Strategy G – Financial Tables (always atomic)
    # ------------------------------------------------------------------

    def _extract_table_chunks(
        self,
        pages_data: List[Dict[str, Any]],
        base_meta: Dict[str, Any],
        document_id: str,
        company_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Extract financial tables as atomic chunks.
        Tables are NEVER split – each table = one chunk.
        """
        chunks: List[Dict[str, Any]] = []
        for page in pages_data:
            page_num = page.get("page_number", 1)
            for table in page.get("tables", []):
                md = DocumentPreprocessor.format_table_as_markdown(table)
                if not md or len(md.strip()) < 30:
                    continue
                # Detect statement type from table headers
                stmt_type = self._classify_table(md)
                meta = dict(base_meta)
                meta["chunk_type"] = "table"
                meta["statement_type"] = stmt_type
                meta["page"] = page_num

                header = self._header(base_meta, page_num, f"Financial Table – {stmt_type}")
                full_content = f"{header}\n\n{md}"
                chunks.append({
                    "document_id": document_id,
                    "company_id": company_id,
                    "chunk_index": 0,  # re-indexed later
                    "content": full_content,
                    "clean_text": md,
                    "section": "Financial Tables",
                    "section_hierarchy": [f"Financial Table – {stmt_type}"],
                    "page_number": page_num,
                    "token_count": len(full_content.split()),
                    "metadata_json": meta,
                    "chunk_type": "table",
                    "parent_chunk_id": None,
                })
        return chunks

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _header(self, meta: Dict[str, Any], page: int, section: str) -> str:
        sym = meta.get("company_symbol") or meta.get("ticker") or "STOCK"
        fy = meta.get("financial_year") or "FY"
        dt = meta.get("document_type") or "Filing"
        return f"[{sym} | {fy} | {dt} | Page {page} – {section}]"

    def _make_chunk(
        self,
        document_id: str,
        company_id: str,
        text: str,
        header: str,
        section: str,
        page_num: int,
        chunk_type: str,
        meta: Dict[str, Any],
        config: ChunkingConfig,
        section_hierarchy: Optional[List[str]] = None,
        parent_chunk_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        full_content = f"{header}\n\n{text}"
        m = dict(meta)
        m["chunk_type"] = chunk_type
        m["page"] = page_num
        if section_hierarchy:
            m["section_hierarchy"] = section_hierarchy
        return {
            "document_id": document_id,
            "company_id": company_id,
            "chunk_index": 0,  # re-indexed after collection
            "content": full_content,
            "clean_text": text,
            "section": section,
            "page_number": page_num,
            "token_count": len(full_content.split()),
            "metadata_json": m,
            "chunk_type": chunk_type,
            "parent_chunk_id": parent_chunk_id,
        }

    def _is_heading(self, text: str) -> bool:
        stripped = text.strip()
        if len(stripped) > 150:
            return False
        words = stripped.split()
        # Need at least 2 words to count as a real heading
        if len(words) < 2:
            return False
        if stripped.isupper() and len(words) >= 2:
            return True
        if _HEADING_RE.match(stripped):
            return True
        text_lower = stripped.lower()
        # Only match if the text IS predominantly the section name (short enough)
        if len(stripped) < 80:
            for section in _ANNUAL_REPORT_SECTIONS:
                if text_lower.startswith(section) or text_lower == section:
                    return True
        return False

    def _heading_depth(self, heading: str) -> int:
        """Estimate hierarchy depth from heading format."""
        if re.match(r"^\d+\.\d+\.", heading):
            return 3
        if re.match(r"^\d+\.", heading):
            return 2
        if heading.isupper():
            return 1
        return 2

    def _sliding_window(
        self, text: str, target_tokens: int, overlap_tokens: int
    ) -> List[str]:
        """Split text into overlapping windows by word count."""
        words = text.split()
        if len(words) <= target_tokens:
            return [text]
        chunks = []
        step = max(1, target_tokens - overlap_tokens)
        i = 0
        while i < len(words):
            chunk_words = words[i: i + target_tokens]
            chunks.append(" ".join(chunk_words))
            i += step
        return chunks

    def _classify_table(self, md_text: str) -> str:
        md_lower = md_text.lower()
        for stmt_type, keywords in _STATEMENT_KEYWORDS.items():
            for kw in keywords:
                if kw in md_lower:
                    return stmt_type.replace("_", " ").title()
        return "Financial Data"

    def _extract_date(self, text: str) -> Optional[str]:
        m = re.search(
            r"\b(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}|\d{4}[./\-]\d{1,2}[./\-]\d{1,2})\b",
            text,
        )
        return m.group(1) if m else None

    def _extract_deal_value(self, text: str) -> Optional[str]:
        m = re.search(
            r"(?:₹|Rs\.?|INR|USD|EUR)?\s*(\d[\d,\.]+\s*(?:crore|cr|lakh|million|billion|mn|bn)?)",
            text, re.IGNORECASE,
        )
        return m.group(0) if m else None

    def _extract_counterparty(self, text: str) -> Optional[str]:
        patterns = [
            r"(?:with|from|to|by)\s+([A-Z][a-z]+ (?:[A-Z][a-z]+ )?(?:Limited|Ltd|Inc|Corp|Group|Pvt))",
            r"(?:Joint Venture|JV|acquisition of|merge with|partner[ed ]+with)\s+([A-Z][^\n,;]{3,40})",
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                return m.group(1).strip()
        return None

    def _deduplicate(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove near-duplicate chunks based on first 150 chars of clean_text."""
        seen: set = set()
        unique = []
        for c in chunks:
            key = (c.get("clean_text") or c.get("content") or "")[:150].strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(c)
            elif not key:
                unique.append(c)
        return unique


# ---------------------------------------------------------------------------
# Backwards-compatible alias so existing code doesn't break
# ---------------------------------------------------------------------------
DocumentChunker = FinancialDocumentChunker
