import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy import Uuid
from ..core.database import Base


class EngineStatusLog(Base):
    __tablename__ = "engine_status_logs"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    engine_name = Column(String(50), nullable=False, index=True)
    state = Column(String(30), nullable=False)  # Ready, Degraded, Disabled, Initializing, Failed
    provider = Column(String(100), nullable=True)
    version = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)

