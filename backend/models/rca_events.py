    # models/flow_log.py
from sqlalchemy import Column, Integer, String, DateTime, select, Text
from datetime import datetime
from db_base import Base  # ✅ import Base from new location

class RCAEvents(Base):
    __tablename__ = 'rca_events'
    id = Column(Integer, primary_key=True, index=True)
    flow_log_id = Column(Integer, nullable=False)
    rca_type = Column(String, nullable=False)
    severity = Column(String)
    detected_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
