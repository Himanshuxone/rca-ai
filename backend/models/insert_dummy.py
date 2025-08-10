# insert_dummy_data.py
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from init_db import async_session  # ✅ import your session
from models.flow_log import FlowLog, RCAReports  # ✅ import models here
from sqlalchemy import insert

# ✅ Dummy Event model (adjust fields if needed)
from sqlalchemy import Column, Integer, String, DateTime
from db_base import Base

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# ✅ Insert dummy records
async def insert_dummy_data():
    async with async_session() as session:
        async with session.begin():
            # Insert Events
            session.add_all([
                Event(id=1, name="API Failure in Production", description="API response delay", status="open", created_at=datetime.utcnow()),
                Event(id=2, name="Database Connection Issue", description="PostgreSQL issue", status="resolved", created_at=datetime.utcnow())
            ])

            # Insert RCAReports
            session.add_all([
                RCAReports(id=1, rca_event_id=1, root_cause="Connection pool exhausted", rca_type="infrastructure", recommendation="Increase pool size", created_at=datetime.utcnow()),
                RCAReports(id=2, rca_event_id=2, root_cause="Network misconfiguration", rca_type="network", recommendation="Update route tables", created_at=datetime.utcnow())
            ])

            # Insert FlowLogs
            session.add_all([
                FlowLog(id=1, event_id=1, request_payload='{"action":"fetchUser","params":{"id":123}}', response_payload='{"error":"timeout"}', status="failed", timestamp=datetime.utcnow()),
                FlowLog(id=2, event_id=1, request_payload='{"action":"fetchUser","params":{"id":124}}', response_payload='{"data":{"user":"John"}}', status="success", timestamp=datetime.utcnow()),
                FlowLog(id=3, event_id=2, request_payload='{"connect_to_db":true}', response_payload='{"error":"connection refused"}', status="failed", timestamp=datetime.utcnow())
            ])

        await session.commit()
        print("✅ Dummy data inserted successfully!")

# Run script
if __name__ == "__main__":
    asyncio.run(insert_dummy_data())
