# File: main.py
from fastapi import FastAPI, HTTPException, File, UploadFile, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, DateTime, select, Text, func
from init_db import init_db, async_session, Base, populate_dummy_data  # ✅ Correct import
from datetime import datetime
from rca_report_stats import RCAReportStats
from utils.models_utils import model_to_dict_recursive
from models.flow_log import FlowLog  # ✅ make sure this file contains your SQLAlchemy models
from models.rca_reports import RCAReports  # ✅ make sure this file contains your SQLAlchemy models
import os
import sys
import shutil
import json

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
    if os.getenv("ENV", "dev") == "dev":  # ✅ Only run in dev mode
        print("🚀 Running dev startup tasks...")
        await init_db()
        await populate_dummy_data()
    else:
        print("✅ Startup without dummy data (non-dev environment).")

@app.get("/")
async def root():
    return {"message": "TechRCA API is running"}

# API endpoints
@app.get("/api/rca-events")
async def get_rca_events():
    try:
        async with async_session() as db:
            result = await db.execute(select(FlowLog))
            events = result.scalars().all()
            # print("📄 Events:", json.dumps([model_to_dict_recursive(r) for r in events]))
            return [model_to_dict_recursive(r) for r in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rca-summary")
async def get_rca_summary():
    try:
        async with async_session() as db:
            # Query grouped counts
            grouped_result = await db.execute(
                select(
                    RCAReports.rca_type,
                    func.count(RCAReports.id).label("count")
                )
                .group_by(RCAReports.rca_type)
            )
            grouped_data = [{"label": r[0], "count": r[1]} for r in grouped_result.all()]

            # Query total count
            total_result = await db.execute(select(func.count(RCAReports.id)))
            total_count = total_result.scalar()

            return {
                "total": total_count,
                "summary": grouped_data
            }

    except Exception as e:
        print("Error in /api/rca-summary:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rca-reports")
async def get_rca_reports():
    try:
        async with async_session() as db:
            result = await db.execute(select(RCAReports))
            reports = result.scalars().all()
            # print("📄 Reports:", json.dumps([model_to_dict_recursive(r) for r in reports]))
            return [model_to_dict_recursive(r) for r in reports]
    except Exception as e:
        print(f"Error in /api/rca-reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rca-reports/{report_id}")
async def get_report_detail(report_id: int):
    try:
        async with async_session() as db:
            report = await db.get(RCAReports, report_id)
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
        print(f"Error in /api/rca-reports: {e}")
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
        print(f"Error in /api/upload: {e}")
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
            flowLogs = result.scalars().all()
            # print("📄 Flow Logs:", json.dumps([model_to_dict_recursive(r) for r in flowLogs]))
            return [model_to_dict_recursive(r) for r in flowLogs]
    except Exception as e:
        print(f"Error in /api/log-summary: {e}")
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