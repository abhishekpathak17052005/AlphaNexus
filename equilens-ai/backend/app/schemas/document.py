from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, UUID4, ConfigDict


class DocumentBase(BaseModel):
    title: str
    financial_year: Optional[str] = None
    document_type: str = "Annual Report"


class DocumentResponse(DocumentBase):
    id: UUID4
    company_id: UUID4
    user_id: Optional[UUID4] = None
    filename: str
    file_size_bytes: int
    mime_type: str
    status: str
    error_message: Optional[str] = None
    total_pages: int
    total_chunks: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentUploadResponse(BaseModel):
    document_id: UUID4
    title: str
    filename: str
    status: str
    message: str


class DocumentProcessResponse(BaseModel):
    document_id: str
    status: str
    pages_extracted: int
    chunks_stored: int

