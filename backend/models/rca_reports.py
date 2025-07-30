# models/flow_log.py
from sqlalchemy import Column, Integer, String
from init_db import Base

class FlowLog(Base):
    __tablename__ = 'rca_reports'
    id = Column(Integer, primary_key=True, index=True)
    rca_event_id = Column(Integer, nullable=False)
    root_cause = Column(String, nullable=False)
    rca_type = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
