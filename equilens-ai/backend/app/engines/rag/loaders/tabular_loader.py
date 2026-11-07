import io
from typing import List, Dict, Any
import pandas as pd
from app.core.logging import logger


class TabularDocumentLoader:
    """
    Extracts structured financial models, ratios, and spreadsheets from XLSX and CSV files.
    """

    def load_csv(self, file_path_or_bytes: Any) -> List[Dict[str, Any]]:
        try:
            if isinstance(file_path_or_bytes, bytes):
                df = pd.read_csv(io.BytesIO(file_path_or_bytes))
            else:
                df = pd.read_csv(file_path_or_bytes)

            csv_text = df.to_string(index=False)
            table_rows = [df.columns.tolist()] + df.values.tolist()

            return [{
                "page_number": 1,
                "text": f"CSV Dataset Summary:\nRows: {len(df)}, Columns: {len(df.columns)}\n\n{csv_text[:4000]}",
                "tables": [table_rows],
                "metadata": {"columns": list(df.columns), "row_count": len(df)},
            }]
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise e

    def load_excel(self, file_path_or_bytes: Any) -> List[Dict[str, Any]]:
        pages_data: List[Dict[str, Any]] = []
        try:
            if isinstance(file_path_or_bytes, bytes):
                excel_file = pd.ExcelFile(io.BytesIO(file_path_or_bytes))
            else:
                excel_file = pd.ExcelFile(file_path_or_bytes)

            for idx, sheet_name in enumerate(excel_file.sheet_names):
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                sheet_text = df.to_string(index=False)
                table_rows = [df.columns.tolist()] + df.values.tolist()

                pages_data.append({
                    "page_number": idx + 1,
                    "text": f"Sheet: {sheet_name}\nRows: {len(df)}, Columns: {len(df.columns)}\n\n{sheet_text[:4000]}",
                    "tables": [table_rows],
                    "metadata": {"sheet_name": sheet_name, "columns": list(df.columns), "row_count": len(df)},
                })
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            raise e

        return pages_data

