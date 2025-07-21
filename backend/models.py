from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    incidents = relationship("Incident", back_populates="user")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    filename = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    summary = relationship("RCASummary", uselist=False, back_populates="incident")
    user = relationship("User", back_populates="incidents")


class RCASummary(Base):
    __tablename__ = "rca_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), unique=True)
    summary_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="summary")

class FlowLog(Base):
    __tablename__ = 'flow_logs'
    id = Column(Integer, primary_key=True, index=True)
    srcaddr = Column(String)
    dstaddr = Column(String)
    dstport = Column(Integer)
    action = Column(String)
    start_time = Column(DateTime)

class RCAEvent(Base):
    __tablename__ = 'rca_events'
    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String)
    severity = Column(String)
    detected_at = Column(DateTime)

class RCAReport(Base):
    __tablename__ = 'rca_reports'
    id = Column(Integer, primary_key=True, index=True)
    root_cause = Column(String)
    recommendation = Column(String)
