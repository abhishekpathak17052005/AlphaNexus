import io
from typing import List, Dict, Any, Optional
import pypdf
import pdfplumber
from app.core.logging import logger


class PDFDocumentLoader:
    """
    High-fidelity PDF document loader for equity research filings.
    Extracts text, preserves page numbers, separates financial tables,
    and captures document metadata.
    """

    def load(self, file_path_or_bytes: Any) -> List[Dict[str, Any]]:
        """
        Loads PDF from path or bytes and returns page-level parsed items.
        Each item contains: page_number, text, tables, metadata.
        """
        pages_data: List[Dict[str, Any]] = []

        try:
            # First pass: use pdfplumber for high-precision text and tabular layout extraction
            if isinstance(file_path_or_bytes, bytes):
                pdf_file = io.BytesIO(file_path_or_bytes)
            else:
                pdf_file = file_path_or_bytes

            with pdfplumber.open(pdf_file) as pdf:
                for idx, page in enumerate(pdf.pages):
                    page_num = idx + 1
                    raw_text = page.extract_text() or ""
                    
                    # Extract structured financial tables
                    raw_tables = page.extract_tables()
                    formatted_tables = []
                    for table in raw_tables:
                        if table and len(table) > 1:
                            # Clean table rows: filter out completely empty cells
                            cleaned_rows = [
                                [str(cell).strip() if cell is not None else "" for cell in row]
                                for row in table
                            ]
                            # Only keep tables with meaningful financial content
                            if any(any(c for c in r) for r in cleaned_rows):
                                formatted_tables.append(cleaned_rows)

                    pages_data.append({
                        "page_number": page_num,
                        "text": raw_text.strip(),
                        "tables": formatted_tables,
                        "width": page.width,
                        "height": page.height,
                    })

        except Exception as e:
            logger.warning(f"pdfplumber extraction failed, falling back to pypdf: {e}")
            # Fallback pass: pypdf reader
            try:
                if isinstance(file_path_or_bytes, bytes):
                    reader = pypdf.PdfReader(io.BytesIO(file_path_or_bytes))
                else:
                    reader = pypdf.PdfReader(file_path_or_bytes)

                pages_data = []
                for idx, page in enumerate(reader.pages):
                    page_num = idx + 1
                    raw_text = page.extract_text() or ""
                    pages_data.append({
                        "page_number": page_num,
                        "text": raw_text.strip(),
                        "tables": [],
                        "width": 0,
                        "height": 0,
                    })
            except Exception as fallback_err:
                logger.error(f"Failed to load PDF: {fallback_err}")
                raise fallback_err

        return pages_data

