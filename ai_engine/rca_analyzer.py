# MVP Architecture for TechRCA: AI-Powered Root Cause Analysis SaaS (Python Code Sample)

"""
This script is a simplified version of the backend logic for:
- Uploading logs
- Running RCA analysis using OpenAI
- Storing results in PostgreSQL
- Exposing FastAPI endpoints
"""

# ------------------------------
# 📦 Install Required Libraries
# ------------------------------
# pip install fastapi uvicorn openai sqlalchemy psycopg2-binary pydantic python-multipart

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openai
import os

# ------------------------------
# 🔧 Configuration
# ------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/techrca")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ------------------------------
# 🧱 Database Model
# ------------------------------
class RCAReport(Base):
    __tablename__ = "rca_reports"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    summary = Column(Text)
    raw_logs = Column(Text)

Base.metadata.create_all(bind=engine)

# ------------------------------
# 🚀 FastAPI App
# ------------------------------
app = FastAPI()

# ------------------------------
# 📄 RCA Prompt Template
# ------------------------------
def generate_rca_prompt(logs: str) -> str:
    return f"""
You are a cloud reliability expert. Given the logs below, identify:
1. Root Cause
2. Affected Services
3. Recommended Fixes

Logs:
{logs}
"""

# ------------------------------
# 🧠 RCA Analyzer (OpenAI)
# ------------------------------
def analyze_logs_with_openai(logs: str) -> str:
    prompt = generate_rca_prompt(logs)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# ------------------------------
# 📤 Upload + Analyze Endpoint
# ------------------------------
@app.post("/analyze")
async def upload_log(file: UploadFile = File(...)):
    contents = await file.read()
    logs = contents.decode("utf-8")
    summary = analyze_logs_with_openai(logs)

    db = SessionLocal()
    report = RCAReport(filename=file.filename, summary=summary, raw_logs=logs)
    db.add(report)
    db.commit()
    db.refresh(report)
    db.close()

    return {"report_id": report.id, "summary": summary}

# ------------------------------
# 📥 Get RCA Report
# ------------------------------
@app.get("/report/{report_id}")
def get_report(report_id: int):
    db = SessionLocal()
    report = db.query(RCAReport).filter(RCAReport.id == report_id).first()
    db.close()
    if report:
        return {"filename": report.filename, "summary": report.summary, "logs": report.raw_logs}
    return {"error": "Report not found"}

# ------------------------------
# ▶️ Run the app with: uvicorn main:app --reload
# ------------------------------
