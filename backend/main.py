from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models import FlowLog, RCAEvent, RCAReport # ✅ Add this
from sqlalchemy import select  # ✅ THIS LINE IS REQUIRED
from datetime import datetime
import uuid, os
# from openai import OpenAI

from database import get_db, engine
from models import Base, User, Incident, RCASummary

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def test_db_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        print("✅ PostgreSQL connected successfully.")
    except Exception as e:
        print("❌ DB connection failed:", e)

# Healthcheck Route
@app.get("/health")
async def health_check():
    return {"status": "OK"}

# API Route: Get flow logs
@app.get("/api/flowlogs")
async def get_flow_logs(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(FlowLog).order_by(FlowLog.start_time.desc()).limit(100))
        logs = result.scalars().all()
        return [
            {
                "srcaddr": log.srcaddr,
                "dstaddr": log.dstaddr,
                "dstport": log.dstport,
                "action": log.action,
                "time": log.start_time.isoformat()
            }
            for log in logs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/rca-events")
async def get_rca_events(db=Depends(get_db)):
    result = await db.execute(select(RCAEvent))
    events = result.scalars().all()
    return [dict(
        summary=e.summary,
        severity=e.severity,
        detected_at=e.detected_at.isoformat()
    ) for e in events]

@app.get("/api/reports")
async def get_rca_reports(db=Depends(get_db)):
    result = await db.execute(select(RCAReport))
    reports = result.scalars().all()
    return [dict(
        root_cause=r.root_cause,
        recommendation=r.recommendation
    ) for r in reports]

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Utility Functions
def extract_text(file: UploadFile) -> str:
    return file.file.read().decode("utf-8")

def generate_summary(log_text: str) -> str:
    # Simulated AI summary for local testing without OpenAI
    return (
        "🚨 **Simulated RCA Summary**\n\n"
        "- Root cause: Database connection timeout detected in logs.\n"
        "- Affected service: PostgreSQL on port 5432\n"
        "- Mitigation: Switched to replica node and restored service\n"
        "- Next steps: Investigate primary node health and HA failover config\n"
        f"\n\n📝 (Preview of uploaded log:)\n{log_text[:250]}..."
    )
    
    # prompt = f"""
    # You are an SRE Assistant. Read the following incident log and summarize the root cause and mitigation steps.

    # Log:
    # {log_text[:4000]}
    # """
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response.choices[0].message.content.strip()


# API Endpoints
@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        log_text = extract_text(file)
        summary_text = generate_summary(log_text)

        incident = Incident(filename=file.filename)
        db.add(incident)
        db.commit()
        db.refresh(incident)

        summary = RCASummary(incident_id=incident.id, summary_text=summary_text)
        db.add(summary)
        db.commit()

        return {
            "report_id": str(summary.id),
            "summary": summary_text
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})



@app.get("/report/{report_id}")
async def get_report(report_id: str, db: Session = Depends(get_db)):
    summary = db.query(RCASummary).filter(RCASummary.id == report_id).first()
    if summary:
        return {
            "filename": summary.incident.filename,
            "summary": summary.summary_text
        }
    return JSONResponse(status_code=404, content={"error": "Report not found"})
