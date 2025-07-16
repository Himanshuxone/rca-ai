from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uuid, os
import openai

from database import get_db, engine
from models import Base, User, Incident, RCASummary

Base.metadata.create_all(bind=engine)  # Create tables on startup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Utility Functions
def extract_text(file: UploadFile) -> str:
    return file.file.read().decode("utf-8")

def generate_summary(log_text: str) -> str:
    prompt = f"""
    You are an SRE Assistant. Read the following incident log and summarize the root cause and mitigation steps.

    Log:
    {log_text[:4000]}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# API Endpoints
@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        log_text = extract_text(file)
        summary_text = generate_summary(log_text)

        # Create Incident and RCA Summary
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
