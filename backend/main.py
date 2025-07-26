# File: main.py
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import os
import shutil

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@localhost:5432/techrca")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
UPLOAD_DIR = "sample_logs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Models
class FlowLog(Base):
    __tablename__ = 'flow_logs'
    id = Column(Integer, primary_key=True, index=True)
    srcaddr = Column(String)
    dstaddr = Column(String)
    srcport = Column(Integer)
    dstport = Column(Integer)
    protocol = Column(String)
    action = Column(String)
    log_status = Column(String)
    version = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

class RCAReport(Base):
    __tablename__ = 'rca_reports'
    id = Column(Integer, primary_key=True, index=True)
    rca_event_id = Column(Integer)
    root_cause = Column(String)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# API endpoints
@app.get("/api/rca-events")
def get_rca_events():
    with SessionLocal() as db:
        events = db.execute(select(FlowLog)).scalars().all()
        return [
            {
                "id": e.id,
                "srcaddr": e.srcaddr,
                "dstaddr": e.dstaddr,
                "srcport": e.srcport,
                "dstport": e.dstport,
                "protocol": e.protocol,
                "action": e.action,
                "log_status": e.log_status,
                "start_time": e.start_time,
            }
            for e in events
        ]

@app.get("/api/rca-reports")
def get_rca_reports():
    with SessionLocal() as db:
        reports = db.execute(select(RCAReport)).scalars().all()
        return [
            {
                "id": r.id,
                "rca_event_id": r.rca_event_id,
                "root_cause": r.root_cause,
                "recommendation": r.recommendation,
                "created_at": r.created_at,
            }
            for r in reports
        ]

@app.get("/api/rca-reports/{report_id}")
def get_report_detail(report_id: int):
    with SessionLocal() as db:
        report = db.get(RCAReport, report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return {
            "id": r.id,
            "rca_event_id": r.rca_event_id,
            "root_cause": r.root_cause,
            "recommendation": r.recommendation,
            "created_at": r.created_at,
        }

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "message": "Upload successful.", "ok": "uploaded"}
    except Exception as e:
        return {"detail": str(e)}

@app.get("/api/dashboard-data")
async def get_dashboard_data():
    # Dummy example — replace with real logic
    return {
        "summary": {
            "total_logs": 14,
            "errors": 7,
            "warnings": 3,
            "info": 4,
        },
        "top_components": ["API Gateway", "Lambda", "S3"],
    }