"""
EquiLens AI – LangChain Multi-Format Document Ingestion Loader
==============================================================
Standardizes document ingestion for PDF, DOCX, TXT, CSV, and XLSX
into LangChain Document objects with rich financial metadata.
"""

import io
import os
import hashlib
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document

from app.engines.rag.loaders.pdf_loader import PDFDocumentLoader
from app.engines.rag.loaders.docx_loader import DOCXDocumentLoader
from app.engines.rag.loaders.tabular_loader import TabularDocumentLoader
from app.core.logging import logger


class LangChainDocumentLoader:
    """
    Unified LangChain ingestion loader supporting PDF, DOCX, TXT, CSV, and XLSX
    with automatic metadata tagging and page-level preservation.
    """

    def __init__(self):
        self.pdf_loader = PDFDocumentLoader()
        self.docx_loader = DOCXDocumentLoader()
        self.tabular_loader = TabularDocumentLoader()

    @staticmethod
    def compute_checksum(content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    def load_as_langchain_documents(
        self,
        file_path_or_bytes: Any,
        filename: str,
        company_id: str,
        ticker: str = "",
        financial_year: str = "",
        document_type: str = "Annual Report",
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Loads document content and returns a list of LangChain Document objects
        with granular page-level metadata.
        """
        ext = os.path.splitext(filename)[1].lower()
        docs: List[Document] = []
        base_meta = {
            "company_id": str(company_id),
            "ticker": ticker.upper(),
            "financial_year": financial_year,
            "document_type": document_type,
            "filename": filename,
            **(extra_metadata or {}),
        }

        # Read bytes if needed for checksum
        if isinstance(file_path_or_bytes, bytes):
            checksum = self.compute_checksum(file_path_or_bytes)
        elif os.path.exists(str(file_path_or_bytes)):
            with open(file_path_or_bytes, "rb") as f:
                checksum = self.compute_checksum(f.read())
        else:
            checksum = ""
        base_meta["file_checksum"] = checksum

        # 1. PDF Documents
        if ext == ".pdf":
            pages_data = self.pdf_loader.load(file_path_or_bytes)
            for page in pages_data:
                page_text = page.get("text", "")
                tables = page.get("tables", [])
                meta = {
                    **base_meta,
                    "page_number": page.get("page_number", 1),
                    "has_tables": bool(tables),
                    "table_count": len(tables),
                }
                # Format tables as Markdown text blocks if present
                content_parts = []
                if page_text:
                    content_parts.append(page_text)
                for tbl in tables:
                    if len(tbl) > 1:
                        hdr = "| " + " | ".join(tbl[0]) + " |"
                        sep = "| " + " | ".join(["---"] * len(tbl[0])) + " |"
                        body = "\n".join("| " + " | ".join(row) + " |" for row in tbl[1:])
                        content_parts.append(f"\n{hdr}\n{sep}\n{body}\n")
                
                full_text = "\n\n".join(content_parts)
                if full_text.strip():
                    docs.append(Document(page_content=full_text, metadata=meta))

        # 2. Word Documents (DOCX)
        elif ext in [".docx", ".doc"]:
            pages_data = self.docx_loader.load(file_path_or_bytes)
            for page in pages_data:
                meta = {**base_meta, "page_number": page.get("page_number", 1)}
                text = page.get("text", "").strip()
                if text:
                    docs.append(Document(page_content=text, metadata=meta))

        # 3. Tabular Documents (XLSX, XLS, CSV)
        elif ext in [".xlsx", ".xls", ".csv"]:
            pages_data = self.tabular_loader.load(file_path_or_bytes, filename)
            for page in pages_data:
                meta = {
                    **base_meta,
                    "page_number": page.get("page_number", 1),
                    "sheet_name": page.get("metadata", {}).get("sheet_name", ""),
                    "is_tabular": True,
                }
                text = page.get("text", "").strip()
                if text:
                    docs.append(Document(page_content=text, metadata=meta))

        # 4. Plain Text Documents (TXT, MD)
        elif ext in [".txt", ".md"]:
            if isinstance(file_path_or_bytes, bytes):
                text_content = file_path_or_bytes.decode("utf-8", errors="replace")
            else:
                with open(file_path_or_bytes, "r", encoding="utf-8", errors="replace") as f:
                    text_content = f.read()
            docs.append(Document(page_content=text_content.strip(), metadata={**base_meta, "page_number": 1}))

        else:
            logger.warning(f"Unsupported file extension {ext} for {filename}")

        return docs

