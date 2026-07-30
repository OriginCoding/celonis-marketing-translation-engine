from sqlalchemy import Column, String, Float, Integer, Text, DateTime
from datetime import datetime
from app.db.database import Base

class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(String, primary_key=True, index=True)
    job_id = Column(String, index=True)
    asset_name = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String)
    reviewer = Column(String)
    reviewer_notes = Column(Text)
    overall_score = Column(Float)
    dnt_violations_count = Column(Integer, default=0)
    destination = Column(String)

class TMSegmentDB(Base):
    __tablename__ = "translation_memory"

    id = Column(String, primary_key=True, index=True)
    source_en = Column(Text, index=True)
    target_es = Column(Text)
    domain = Column(String, default="marketing")
    quality_score = Column(Float, default=1.0)
    last_used = Column(DateTime, default=datetime.utcnow)
