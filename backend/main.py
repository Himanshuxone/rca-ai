# File: main.py
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, DateTime, Select
from sqlalchemy.orm import declarative_base
from datetime import datetime
import os
import asyncio
import sys
import shutil

# Add project root to Python path

from db import get_db_connection  # your existing DB utility
from rca_report_stats import RCAReportStats

app = FastAPI()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
UPLOAD_DIR = "sample_logs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
Base = declarative_base()
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
    rca_type = Column(String)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# API endpoints
@app.get("/api/rca-events")
async def get_rca_events():
    async with async_session() as db:
        events = await db.execute(select(FlowLog)).scalars().all()
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
async def get_rca_reports():
    async with async_session() as db:
        reports = db.execute(select(RCAReport)).scalars().all()
        return [
            {
                "id": r.id,
                "rca_event_id": r.rca_event_id,
                "root_cause": r.root_cause,
                "rca_type" : r.rca_type,
                "recommendation": r.recommendation,
                "created_at": r.created_at,
            }
            for r in reports
        ]

@app.get("/api/rca-reports/{report_id}")
async def get_report_detail(report_id: int):
    async with async_session() as db:
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
        # 🔁 Trigger RCA analysis immediately
        analysis_result = analyze_log_file(file_location)
        return {"filename": file.filename, "message": "Upload successful.", "ok": "uploaded", "analysis": analysis_result}
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

def analyze_log_file(filepath):
    # Example logic (add actual logic based on error analysis)
    result = {
        "root_cause": "Database crash due to out-of-memory",
        "component": "MemoryManager",
        "recommendation": "Increase heap size or add memory monitoring",
        "severity": "critical"
    }

    if "crash" in result["root_cause"].lower():
        result["severity"] = "critical"
    elif "timeout" in result["root_cause"].lower():
        result["severity"] = "warning"
    else:
        result["severity"] = "info"
    return result

@app.get("/api/log-summary")
def get_log_summary():
    """ Retrieve data from the vendors table """
    try:
        conn = get_db_connection()
        stats = RCAReportStats(conn)
        # Execute and print RCA type counts
        rca_counts = stats.get_rca_type_counts()
        for risk, count in rca_counts.items():
            print(f"{risk}: {count}")
        conn.close()
        return rca_counts.items()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    # Dummy example — replace with real logic