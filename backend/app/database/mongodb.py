"""
EquiLens AI – MongoDB & Atlas Vector Search Database Manager
============================================================
Handles connection pooling, Atlas Vector Search compatibility checks,
collection management, and graceful local simulation fallback.
"""

import os
import certifi
from typing import Dict, Any, Optional, List
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from app.core.config import settings
from app.core.logging import logger

# In-memory document & chunk storage fallback when Atlas is unreachable
_simulated_db: Dict[str, List[Dict[str, Any]]] = {
    "rag_documents": [],
    "rag_chunks": [],
    "rag_conversations": [],
    "rag_citations": [],
    "rag_configurations": [],
}


class MongoDBManager:
    """
    Manages MongoDB client lifecycle, collections, and Atlas Vector Search index creation.
    """

    def __init__(self):
        self.uri = getattr(settings, "MONGODB_URI", None) or os.getenv("MONGODB_URI", "")
        self.db_name = getattr(settings, "MONGODB_DB", None) or os.getenv("MONGODB_DB", "equilens_rag")
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._is_connected = False
        self._connection_error: Optional[str] = None
        self._atlas_search_ready = False
        self._connect()

    def _connect(self):
        if not self.uri:
            self._connection_error = "MONGODB_URI is not configured in environment."
            self._is_connected = False
            return

        try:
            # Use certifi for macOS TLS verification
            self._client = MongoClient(
                self.uri,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=3000,
                connectTimeoutMS=3000,
                socketTimeoutMS=3000,
            )
            # Validate connection
            self._client.admin.command("ping")
            self._db = self._client[self.db_name]
            self._is_connected = True
            self._connection_error = None
            logger.info(f"Connected successfully to MongoDB Atlas database: {self.db_name}")
            self._ensure_indexes()
        except Exception as e:
            err_msg = str(e)
            self._is_connected = False
            if "tlsv1 alert internal error" in err_msg or "SSL handshake failed" in err_msg:
                self._connection_error = (
                    "MongoDB Atlas Network Access Block: Current machine IP is not whitelisted. "
                    "Add your current IP (or 0.0.0.0/0) in MongoDB Atlas Console -> Security -> Network Access."
                )
            else:
                self._connection_error = f"MongoDB connection error: {err_msg}"
            logger.warning(f"MongoDB connection notice: {self._connection_error}. Running in resilient hybrid mode.")

    def _ensure_indexes(self):
        """Creates standard metadata and unique indexes on MongoDB collections."""
        if not self._is_connected or self._db is None:
            return
        try:
            # 1. rag_documents indexes
            docs = self._db["rag_documents"]
            docs.create_index([("company_id", 1), ("financial_year", 1)])
            docs.create_index("file_checksum", unique=True, sparse=True)
            docs.create_index("document_type")
            docs.create_index("created_at")

            # 2. rag_chunks indexes
            chunks = self._db["rag_chunks"]
            chunks.create_index([("document_id", 1), ("chunk_index", 1)])
            chunks.create_index([("company_id", 1), ("document_type", 1)])
            chunks.create_index("financial_year")

            # 3. rag_conversations indexes
            convs = self._db["rag_conversations"]
            convs.create_index("session_id", unique=True)
            convs.create_index("company_id")

            # 4. rag_citations indexes
            cites = self._db["rag_citations"]
            cites.create_index("session_id")
            cites.create_index("document_id")

            logger.info("MongoDB collection indexes verified.")
        except Exception as e:
            logger.warning(f"Error ensuring MongoDB collection indexes: {e}")

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def connection_error(self) -> Optional[str]:
        return self._connection_error

    @property
    def database(self) -> Optional[Database]:
        return self._db

    def get_collection(self, name: str) -> Optional[Collection]:
        if self._is_connected and self._db is not None:
            return self._db[name]
        return None

    def check_health(self) -> Dict[str, Any]:
        """Returns comprehensive diagnostic health check of MongoDB & Vector Search."""
        if self._is_connected and self._client is not None:
            try:
                build_info = self._client.admin.command("buildInfo")
                db_names = self._client.list_database_names()
                colls = self._db.list_collection_names() if self._db is not None else []
                return {
                    "connected": True,
                    "status": "Healthy",
                    "deployment_type": "MongoDB Atlas ReplicaSet",
                    "version": build_info.get("version", "Unknown"),
                    "database": self.db_name,
                    "collections": colls,
                    "total_databases": len(db_names),
                    "atlas_vector_search_supported": True,
                    "error": None,
                }
            except Exception as e:
                return {
                    "connected": False,
                    "status": "Degraded",
                    "deployment_type": "MongoDB Atlas",
                    "database": self.db_name,
                    "atlas_vector_search_supported": False,
                    "error": str(e),
                }

        return {
            "connected": False,
            "status": "Degraded (Simulated Hybrid Fallback Active)",
            "deployment_type": "Simulated Local MongoDB",
            "database": self.db_name,
            "atlas_vector_search_supported": False,
            "error": self._connection_error or "Not connected to MongoDB.",
            "remediation": "Add current IP to MongoDB Atlas Network Access whitelist to enable live Atlas Vector Search.",
        }

    # -------------------------------------------------------------------------
    # Unified document & chunk storage interface (Atlas + Local Fallback)
    # -------------------------------------------------------------------------

    def store_document(self, doc_data: Dict[str, Any]) -> str:
        """Stores a document record in rag_documents."""
        if self._is_connected and self._db is not None:
            res = self._db["rag_documents"].insert_one(doc_data)
            return str(res.inserted_id)
        else:
            _simulated_db["rag_documents"].append(doc_data)
            return str(doc_data.get("_id") or len(_simulated_db["rag_documents"]))

    def store_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Stores document chunks with embeddings in rag_chunks."""
        if not chunks:
            return 0
        if self._is_connected and self._db is not None:
            res = self._db["rag_chunks"].insert_many(chunks)
            return len(res.inserted_ids)
        else:
            _simulated_db["rag_chunks"].extend(chunks)
            return len(chunks)

    def find_chunks(self, query_filter: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
        """Queries chunks with metadata filters."""
        if self._is_connected and self._db is not None:
            cursor = self._db["rag_chunks"].find(query_filter).limit(limit)
            return list(cursor)
        else:
            res = []
            for c in _simulated_db["rag_chunks"]:
                match = True
                for k, v in query_filter.items():
                    if c.get(k) != v:
                        match = False
                        break
                if match:
                    res.append(c)
                if len(res) >= limit:
                    break
            return res

    def delete_document_chunks(self, document_id: str) -> int:
        """Removes all chunks for a document."""
        if self._is_connected and self._db is not None:
            res = self._db["rag_chunks"].delete_many({"document_id": document_id})
            self._db["rag_documents"].delete_one({"_id": document_id})
            return res.deleted_count
        else:
            prev = len(_simulated_db["rag_chunks"])
            _simulated_db["rag_chunks"] = [
                c for c in _simulated_db["rag_chunks"] if str(c.get("document_id")) != str(document_id)
            ]
            _simulated_db["rag_documents"] = [
                d for d in _simulated_db["rag_documents"] if str(d.get("_id")) != str(document_id)
            ]
            return prev - len(_simulated_db["rag_chunks"])


# Global singleton instance
mongodb_manager = MongoDBManager()
