import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.research import ResearchSession, ResearchMessage, Citation
from app.models.company import Company
from app.engines.rag.service import rag_service
from app.schemas.research import (
    ResearchQueryRequest,
    ResearchMessageResponse,
    ResearchSessionResponse,
    CitationResponse,
)

router = APIRouter()


@router.post("/chat", response_model=ResearchMessageResponse)
def research_chat(payload: ResearchQueryRequest, db: Session = Depends(get_db)):
    """
    Submits a research query to the RAG engine.
    Retrieves semantic context, generates fact-grounded answer,
    and returns citations linked to exact source document pages.
    """
    # Parse company UUID
    comp_uuid = None
    if payload.company_id:
        try:
            comp_uuid = uuid.UUID(payload.company_id)
        except (ValueError, AttributeError):
            c = db.query(Company).filter(Company.symbol == payload.company_id.upper()).first()
            if c:
                comp_uuid = c.id

    # Create or get session
    sess_obj = None
    if payload.session_id:
        try:
            val_uuid = uuid.UUID(payload.session_id)
            sess_obj = db.query(ResearchSession).filter(ResearchSession.id == val_uuid).first()
        except (ValueError, AttributeError):
            pass

    if not sess_obj:
        title = payload.query[:60] + ("..." if len(payload.query) > 60 else "")
        sess_obj = ResearchSession(
            title=title,
            company_id=comp_uuid,
        )
        db.add(sess_obj)
        db.commit()
        db.refresh(sess_obj)

    result = rag_service.research_chat(
        db=db,
        session_id=str(sess_obj.id),
        user_query=payload.query,
        company_id=str(comp_uuid) if comp_uuid else None,
        financial_year=payload.financial_year,
        document_type=payload.document_type,
        top_k=payload.top_k,
    )

    msg_uuid = uuid.UUID(result["message_id"])
    msg = db.query(ResearchMessage).filter(ResearchMessage.id == msg_uuid).first()
    citations = [
        CitationResponse(
            id=str(c.id),
            document_id=str(c.document_id),
            document_chunk_id=str(c.document_chunk_id) if c.document_chunk_id else None,
            document_title=c.document.title if c.document else "Filing",
            page_number=c.page_number,
            section=c.section,
            excerpt=c.excerpt,
            source_url=c.source_url,
            confidence_score=float(c.confidence_score or 0.95),
        )
        for c in msg.citations
    ]

    return ResearchMessageResponse(
        id=str(msg.id),
        session_id=str(msg.session_id),
        role=msg.role,
        content=msg.content,
        message_type=msg.message_type,
        tokens_used=msg.token_count,
        citations=citations,
        created_at=msg.created_at,
    )


@router.get("/sessions", response_model=List[ResearchSessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ResearchSession).order_by(ResearchSession.updated_at.desc()).all()
    out = []
    for s in sessions:
        out.append(ResearchSessionResponse(
            id=str(s.id),
            title=s.title,
            company_id=str(s.company_id) if s.company_id else None,
            created_at=s.created_at,
            updated_at=s.updated_at,
            messages=[],
        ))
    return out


@router.get("/sessions/{session_id}", response_model=ResearchSessionResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    try:
        val_uuid = uuid.UUID(session_id)
        session = db.query(ResearchSession).filter(ResearchSession.id == val_uuid).first()
    except (ValueError, AttributeError):
        session = None

    if not session:
        raise HTTPException(status_code=404, detail="Research session not found")

    messages_out = []
    for msg in session.messages:
        citations = [
            CitationResponse(
                id=str(c.id),
                document_id=str(c.document_id),
                document_chunk_id=str(c.document_chunk_id) if c.document_chunk_id else None,
                document_title=c.document.title if c.document else "Filing",
                page_number=c.page_number,
                section=c.section,
                excerpt=c.excerpt,
                source_url=c.source_url,
                confidence_score=float(c.confidence_score or 0.95),
            )
            for c in msg.citations
        ]
        messages_out.append(ResearchMessageResponse(
            id=str(msg.id),
            session_id=str(msg.session_id),
            role=msg.role,
            content=msg.content,
            message_type=msg.message_type,
            tokens_used=msg.token_count,
            citations=citations,
            created_at=msg.created_at,
        ))

    return ResearchSessionResponse(
        id=str(session.id),
        title=session.title,
        company_id=str(session.company_id) if session.company_id else None,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=messages_out,
    )
