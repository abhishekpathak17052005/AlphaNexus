"""
ALPHANEXUS – MongoDB Atlas Index Definitions & Management
==========================================================
Defines search indexes, metadata compound indexes, and vector search mappings.
"""

from typing import Dict, Any, List
from pymongo.database import Database
from app.core.logging import logger
from app.database.collections import (
    COLLECTION_DOCUMENTS,
    COLLECTION_CHUNKS,
    COLLECTION_CONVERSATIONS,
    COLLECTION_CITATIONS,
)


def ensure_all_indexes(db: Database) -> Dict[str, Any]:
    """Applies unique, compound, and sparse indexes to MongoDB collections."""
    report = {}
    try:
        # 1. Documents collection
        doc_col = db[COLLECTION_DOCUMENTS]
        doc_col.create_index([("company_id", 1), ("financial_year", 1)])
        doc_col.create_index("file_checksum", unique=True, sparse=True)
        doc_col.create_index("document_type")
        doc_col.create_index("created_at")
        report[COLLECTION_DOCUMENTS] = "OK"

        # 2. Chunks collection
        chk_col = db[COLLECTION_CHUNKS]
        chk_col.create_index([("document_id", 1), ("chunk_index", 1)])
        chk_col.create_index([("company_id", 1), ("document_type", 1)])
        chk_col.create_index("financial_year")
        report[COLLECTION_CHUNKS] = "OK"

        # 3. Conversations & Citations
        conv_col = db[COLLECTION_CONVERSATIONS]
        conv_col.create_index("session_id", unique=True)
        report[COLLECTION_CONVERSATIONS] = "OK"

        cite_col = db[COLLECTION_CITATIONS]
        cite_col.create_index("session_id")
        cite_col.create_index("document_id")
        report[COLLECTION_CITATIONS] = "OK"

        logger.info("[MongoDB] All collection indexes verified and applied.")
    except Exception as exc:
        logger.warning(f"[MongoDB] Error applying indexes: {exc}")
        report["error"] = str(exc)

    return report
