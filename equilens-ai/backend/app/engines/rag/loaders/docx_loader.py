import io
from typing import List, Dict, Any
import docx
from app.core.logging import logger


class DOCXDocumentLoader:
    """
    Extracts text, headings, and tables from DOCX research notes and reports.
    """

    def load(self, file_path_or_bytes: Any) -> List[Dict[str, Any]]:
        pages_data: List[Dict[str, Any]] = []

        try:
            if isinstance(file_path_or_bytes, bytes):
                doc = docx.Document(io.BytesIO(file_path_or_bytes))
            else:
                doc = docx.Document(file_path_or_bytes)

            full_paragraphs = []
            for p in doc.paragraphs:
                text = p.text.strip()
                if text:
                    full_paragraphs.append(text)

            tables_data = []
            for table in doc.tables:
                rows_data = []
                for row in table.rows:
                    row_cells = [cell.text.strip() for cell in row.cells]
                    rows_data.append(row_cells)
                if rows_data:
                    tables_data.append(rows_data)

            # DOCX does not have native page boundaries without rendering engine,
            # so we synthesize logical pages based on content chunks
            pages_data.append({
                "page_number": 1,
                "text": "\n\n".join(full_paragraphs),
                "tables": tables_data,
                "metadata": {"paragraph_count": len(full_paragraphs), "table_count": len(tables_data)},
            })

        except Exception as e:
            logger.error(f"Error loading DOCX: {e}")
            raise e

        return pages_data

