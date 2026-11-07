import re
from typing import List, Dict, Any, Optional
from .preprocessor import DocumentPreprocessor


class DocumentChunker:
    """
    Section-aware and metadata-preserving document chunker.
    Preserves financial tables as single cohesive blocks and maintains
    page numbers, headings, financial year, and company references.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(
        self,
        pages_data: List[Dict[str, Any]],
        company_id: str,
        document_id: str,
        company_symbol: str = "",
        financial_year: str = "",
        document_type: str = "",
    ) -> List[Dict[str, Any]]:
        chunks: List[Dict[str, Any]] = []
        chunk_idx = 0

        for page in pages_data:
            page_num = page.get("page_number", 1)
            raw_text = page.get("text", "")
            tables = page.get("tables", [])

            # Check for empty page
            if DocumentPreprocessor.is_empty_page(raw_text, tables):
                continue

            # 1. Process Financial Tables First (Keep tables as atomic chunks)
            for table in tables:
                md_table = DocumentPreprocessor.format_table_as_markdown(table)
                if md_table and len(md_table.strip()) > 30:
                    table_content = (
                        f"[{company_symbol} | {financial_year} | {document_type} | Page {page_num} - Financial Table]\n\n"
                        f"{md_table}"
                    )
                    chunks.append({
                        "document_id": document_id,
                        "company_id": company_id,
                        "chunk_index": chunk_idx,
                        "content": table_content,
                        "clean_text": md_table,
                        "section": "Financial Tables",
                        "page_number": page_num,
                        "token_count": len(table_content.split()),
                        "metadata_json": {
                            "type": "table",
                            "page": page_num,
                            "company_symbol": company_symbol,
                            "financial_year": financial_year,
                            "document_type": document_type,
                        },
                    })
                    chunk_idx += 1

            # 2. Process Narrative Paragraphs and Sections
            normalized_text = DocumentPreprocessor.normalize_text(raw_text)
            if not normalized_text:
                continue

            # Detect sections / headings
            paragraphs = normalized_text.split("\n\n")
            current_buffer = []
            current_len = 0
            current_section = "General Text"

            for p in paragraphs:
                p_clean = p.strip()
                if not p_clean:
                    continue

                # Heading detection heuristic: short line, capitalized or numbered
                if len(p_clean) < 100 and (p_clean.isupper() or re.match(r"^(\d+\.|\b(Note|Section|Item)\b)", p_clean)):
                    current_section = p_clean

                p_len = len(p_clean)
                if current_len + p_len > self.chunk_size and current_buffer:
                    chunk_text = " ".join(current_buffer)
                    header_prefix = f"[{company_symbol} | {financial_year} | {document_type} | Page {page_num} - {current_section}]\n\n"
                    full_content = header_prefix + chunk_text

                    chunks.append({
                        "document_id": document_id,
                        "company_id": company_id,
                        "chunk_index": chunk_idx,
                        "content": full_content,
                        "clean_text": chunk_text,
                        "section": current_section,
                        "page_number": page_num,
                        "token_count": len(full_content.split()),
                        "metadata_json": {
                            "type": "narrative",
                            "page": page_num,
                            "company_symbol": company_symbol,
                            "financial_year": financial_year,
                            "document_type": document_type,
                            "section": current_section,
                        },
                    })
                    chunk_idx += 1

                    # Retain overlap from end of buffer
                    overlap_chars = 0
                    new_buffer = []
                    for item in reversed(current_buffer):
                        if overlap_chars + len(item) < self.chunk_overlap:
                            new_buffer.insert(0, item)
                            overlap_chars += len(item)
                        else:
                            break
                    current_buffer = new_buffer + [p_clean]
                    current_len = sum(len(x) for x in current_buffer)
                else:
                    current_buffer.append(p_clean)
                    current_len += p_len

            # Flush remaining buffer for this page
            if current_buffer:
                chunk_text = " ".join(current_buffer)
                header_prefix = f"[{company_symbol} | {financial_year} | {document_type} | Page {page_num} - {current_section}]\n\n"
                full_content = header_prefix + chunk_text

                chunks.append({
                    "document_id": document_id,
                    "company_id": company_id,
                    "chunk_index": chunk_idx,
                    "content": full_content,
                    "clean_text": chunk_text,
                    "section": current_section,
                    "page_number": page_num,
                    "token_count": len(full_content.split()),
                    "metadata_json": {
                        "type": "narrative",
                        "page": page_num,
                        "company_symbol": company_symbol,
                        "financial_year": financial_year,
                        "document_type": document_type,
                        "section": current_section,
                    },
                })
                chunk_idx += 1

        return chunks

