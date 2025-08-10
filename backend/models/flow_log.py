# models/flow_log.py
from sqlalchemy import Column, Integer, String, DateTime, select, Text, BigInteger
from datetime import datetime
from db_base import Base  # ✅ import Base from new location

class FlowLog(Base):
    __tablename__ = 'flow_logs'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(BigInteger, nullable=False)
    vpc_id = Column(String, nullable=False)
    interface_id = Column(String, nullable=False)
    srcaddr = Column(String, nullable=False)
    dstaddr = Column(String, nullable=False)
    srcport = Column(Integer, nullable=False)
    dstport = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    log_status = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
