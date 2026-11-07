import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Numeric, ForeignKey, Index
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
from ..core.database import Base


class ResearchSession(Base):
    __tablename__ = "research_sessions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id = Column(Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="research_sessions")
    messages = relationship("ResearchMessage", back_populates="session", cascade="all, delete-orphan")


class ResearchMessage(Base):
    __tablename__ = "research_messages"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(Uuid(as_uuid=True), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    message_type = Column(String(30), default="synthesis")  # fact_grounded, calculated, synthesis
    token_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ResearchSession", back_populates="messages")
    citations = relationship("Citation", back_populates="message", cascade="all, delete-orphan")


class Citation(Base):
    __tablename__ = "citations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    message_id = Column(Uuid(as_uuid=True), ForeignKey("research_messages.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(Uuid(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    document_chunk_id = Column(Uuid(as_uuid=True), ForeignKey("document_chunks.id", ondelete="SET NULL"), nullable=True)
    chunk_index = Column(Integer, nullable=True)
    page_number = Column(Integer, nullable=True)
    section = Column(String(100), nullable=True)
    excerpt = Column(Text, nullable=False)
    source_url = Column(String(500), nullable=True)
    confidence_score = Column(Numeric(5, 4), default=0.9500)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    message = relationship("ResearchMessage", back_populates="citations")
    document = relationship("Document", back_populates="citations")
    chunk = relationship("DocumentChunk", back_populates="citations")

