# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import Column, Integer, String, DateTime, select, Text
# from init_db import async_session
# from models.flow_log import FlowLog
# from models.rca_reports import RCAReports
# from datetime import datetime

# # Import your Event model
# from models.event import Event  # Adjust this path
# async def populate_dummy_data():
#     async with async_session() as session:
#         async with session.begin():
#             # 🔹 Check Events
#             existing_events = await session.execute(select(Event).limit(1))
#             if not existing_events.scalars().first():
#                 print("📌 Inserting dummy Events...")
#                 session.add_all([
#                     Event(
#                         id=1,
#                         rca_type="blocked_port",
#                         severity="high",
#                         summary="Database traffic blocked from app server",
#                         status="new",
#                         created_at=datetime.utcnow()
#                     ),
#                     Event(
#                         id=1,
#                         rca_type="normal_traffic",
#                         severity="low",
#                         summary="No anomalies detected for this flow",
#                         status="resolved",
#                         created_at=datetime.utcnow()
#                     ),
#                 ])
#             else:
#                 print("✅ Events already populated. Skipping.")

#             # 🔹 Check RCA Reports
#             existing_reports = await session.execute(select(RCAReports).limit(1))
#             if not existing_reports.scalars().first():
#                 print("📌 Inserting dummy RCA Reports...")
#                 session.add_all([
#                     RCAReports(
#                         id=1,
#                         rca_event_id=1,
#                         root_cause="Connection pool exhausted",
#                         rca_type="infra",
#                         recommendation="Increase pool size",
#                         created_at=datetime.utcnow()
#                     ),
#                     RCAReports(
#                         id=2,
#                         rca_event_id=2,
#                         root_cause="Incorrect configuration",
#                         rca_type="ops",
#                         recommendation="Fix database config",
#                         created_at=datetime.utcnow()
#                     ),
#                 ])
#             else:
#                 print("✅ RCA Reports already populated. Skipping.")

#             # 🔹 Check Flow Logs
#             existing_logs = await session.execute(select(FlowLog).limit(1))
#             if not existing_logs.scalars().first():
#                 print("📌 Inserting dummy Flow Logs...")
#                 session.add_all([
#                     FlowLog(
#                         id=1,
#                         event_id=1,
#                         request_payload='{"action":"getUser"}',
#                         response_payload='{"error":"timeout"}',
#                         status="failed",
#                         timestamp=datetime.utcnow()
#                     ),
#                     FlowLog(
#                         id=2,
#                         event_id=2,
#                         request_payload='{"action":"connect"}',
#                         response_payload='{"status":"error"}',
#                         status="failed",
#                         timestamp=datetime.utcnow()
#                     ),
#                 ])
#             else:
#                 print("✅ Flow Logs already populated. Skipping.")
#         await session.commit()
#         print("🎯 Dummy data population complete.")
