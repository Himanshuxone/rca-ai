# models/flow_log.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db_base import Base  # ✅ import Base from new location

class RCAReports(Base):
    __tablename__ = 'rca_reports'
    id = Column(Integer, primary_key=True, index=True)
    rca_event_id = Column(Integer, nullable=False)
    root_cause = Column(String, nullable=False)
    rca_type = Column(String, nullable=False)
    evidence_json = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
