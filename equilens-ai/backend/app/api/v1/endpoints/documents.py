import os
import uuid
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.document import Document
from app.models.company import Company
from app.engines.rag.service import rag_service
from app.schemas.document import DocumentResponse, DocumentUploadResponse, DocumentProcessResponse

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    company_id: str = Form(...),
    title: str = Form(...),
    financial_year: str = Form("FY24"),
    document_type: str = Form("Annual Report"),
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    auto_process: bool = Form(True),
    db: Session = Depends(get_db),
):
    """
    Uploads a financial document (PDF, DOCX, XLSX, CSV).
    Saves file to storage, creates Document record, and optionally queues processing.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Ensure upload directory exists
    os.makedirs(settings.LOCAL_UPLOAD_DIR, exist_ok=True)
    doc_id = uuid.uuid4()
    safe_filename = f"{doc_id}_{file.filename}"
    file_path = os.path.join(settings.LOCAL_UPLOAD_DIR, safe_filename)

    # Save file contents
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    doc = Document(
        id=doc_id,
        company_id=company.id,
        title=title,
        filename=file.filename,
        file_path=file_path,
        file_size_bytes=len(contents),
        mime_type=file.content_type or "application/octet-stream",
        financial_year=financial_year,
        document_type=document_type,
        status="UPLOADED",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Process immediately if auto_process is enabled
    if auto_process:
        try:
            rag_service.ingest_document(
                db=db,
                document_id=str(doc.id),
                file_path_or_bytes=file_path,
                filename=file.filename,
                mime_type=doc.mime_type,
            )
            message = "Document uploaded and processed successfully into vector store."
        except Exception as e:
            message = f"Document uploaded, but processing failed: {str(e)}"
    else:
        message = "Document uploaded successfully. Ready for processing."

    return DocumentUploadResponse(
        document_id=doc.id,
        title=doc.title,
        filename=doc.filename,
        status=doc.status,
        message=message,
    )


@router.get("", response_model=List[DocumentResponse])
def list_documents(
    company_id: Optional[str] = None,
    document_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Document)
    if company_id:
        query = query.filter(Document.company_id == company_id)
    if document_type:
        query = query.filter(Document.document_type == document_type)
    if status:
        query = query.filter(Document.status == status.upper())
    return query.order_by(Document.created_at.desc()).all()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/{document_id}/process", response_model=DocumentProcessResponse)
def process_document(document_id: str, db: Session = Depends(get_db)):
    """Triggers RAG extraction, chunking, and pgvector embeddings on an existing document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=400, detail="Stored file path does not exist on disk.")

    result = rag_service.ingest_document(
        db=db,
        document_id=str(doc.id),
        file_path_or_bytes=doc.file_path,
        filename=doc.filename,
        mime_type=doc.mime_type,
    )

    return DocumentProcessResponse(
        document_id=result["document_id"],
        status=result["status"],
        pages_extracted=result["pages_extracted"],
        chunks_stored=result["chunks_stored"],
    )


@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.file_path and os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            pass

    db.delete(doc)
    db.commit()
    return {"message": "Document and associated embeddings deleted successfully"}

