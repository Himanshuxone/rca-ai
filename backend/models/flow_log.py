# models/flow_log.py
from sqlalchemy import Column, Integer, String, DateTime, select, Text
from datetime import datetime
from db_base import Base  # ✅ import Base from new location

class FlowLog(Base):
    __tablename__ = 'flow_logs'
    id = Column(Integer, primary_key=True, index=True)
    srcaddr = Column(String, nullable=False)
    dstaddr = Column(String, nullable=False)
    srcport = Column(Integer, nullable=False)
    dstport = Column(Integer, nullable=False)
    protocol = Column(String, nullable=False)
    action = Column(String, nullable=False)
    log_status = Column(String, nullable=False)
    version = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
