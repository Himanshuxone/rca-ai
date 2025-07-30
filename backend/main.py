# File: main.py
from fastapi import FastAPI, HTTPException, File, UploadFile, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, DateTime, select, Text
from init_db import init_db, async_session, Base  # ✅ Correct import
from datetime import datetime
from rca_report_stats import RCAReportStats
from models.flow_log import FlowLog  # ✅ make sure this file contains your SQLAlchemy models
from models.rca_reports import RCAReports  # ✅ make sure this file contains your SQLAlchemy models
import os
import sys
import shutil

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

UPLOAD_DIR = "sample_logs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    await init_db(5,3)  # ✅ Ensure DB tables are created at startup
    print("Initialising all the tables")

# API endpoints
@app.get("/api/rca-events")
async def get_rca_events():
    try:
        async with async_session() as db:
            result = await db.execute(select(FlowLog))
            events = result.scalars().all()
            print(events)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rca-reports")
async def get_rca_reports():
    try:
        async with async_session() as db:
            result = await db.execute(select(RCAReport))
            reports = result.scalars().all()
            return {"events": [e.__dict__ for e in reports]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rca-reports/{report_id}")
async def get_report_detail(report_id: int):
    try:
        async with async_session() as db:
            report = await db.get(RCAReport, report_id)
            if not report:
                raise HTTPException(status_code=404, detail="Report not found")
            return {
                "id": report.id,
                "rca_event_id": report.rca_event_id,
                "root_cause": report.root_cause,
                "rca_type": report.rca_type,
                "recommendation": report.recommendation,
                "created_at": report.created_at,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        analysis_result = analyze_log_file(file_location)
        return {
            "filename": file.filename,
            "message": "Upload successful.",
            "ok": "uploaded",
            "analysis": analysis_result
        }
    except Exception as e:
        return {"detail": str(e)}

@app.get("/api/dashboard-data")
async def get_dashboard_data():
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
async def get_log_summary(limit: int = Query(100, le=1000)):
    """
    Returns log entries from the log_summary table.
    """
    try:
        async with async_session() as db:
            result = await db.execute(select(FlowLog))
            events = result.scalars().all()
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/api/log-summary", status_code=status.HTTP_201_CREATED)
# async def create_log(log: FlowLog):
#     try:
#         async with async_session() as db:
#             new_log = FlowLog(
#                 id = log.id,
#                 srcaddr=log.srcaddr,
#                 dstaddr=log.dstaddr,
#                 srcport=log.srcport,
#                 dstport=log.dstport,
#                 protocol=log.protocol,
#                 action=log.action,
#                 log_status=log.log_status,
#                 start_time=log.start_time or datetime.utcnow()
#             )
#             db.add(new_log)
#             await db.commit()
#             await db.refresh(new_log)  # optional: get the ID back

#             return {
#                 "id": new_log.id,
#                 "srcaddr": new_log.srcaddr,
#                 "dstaddr": new_log.dstaddr,
#                 "srcport": new_log.srcport,
#                 "dstport": new_log.dstport,
#                 "protocol": new_log.protocol,
#                 "action": new_log.action,
#                 "log_status": new_log.log_status,
#                 "start_time": new_log.start_time,
#             }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))