# init_db.py
import asyncio
import os
import traceback
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

import logging
from db_base import Base
from models.flow_log import FlowLog
from models.rca_reports import RCAReports

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@db:5432/techrca"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# --- DB INIT ---
async def init_db(max_retries=10, delay=3):
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Database initialized successfully.")
            return
        except Exception as e:
            print(f"❌ Error initializing the database (attempt {attempt + 1}/{max_retries}): {e}")
            traceback.print_exc()
            await asyncio.sleep(delay)
    raise RuntimeError("❌ Could not connect to the database after several retries.")

# --- TEST CONNECTION ---
async def test_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful.")
    except OperationalError as e:
        print(f"❌ OperationalError: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()

# --- POPULATE DUMMY DATA ---
async def populate_dummy_data():
    async with async_session() as session:
        # Check if already populated
        flow_count = (await session.execute(text("SELECT COUNT(*) FROM flow_logs"))).scalar()
        rca_count = (await session.execute(text("SELECT COUNT(*) FROM rca_reports"))).scalar()

        if flow_count == 0:
            print("📌 Inserting dummy Flow Logs...")
            session.add_all([
                FlowLog(
                    id=1,
                    account_id=123456789012,
                    interface_id="eni-01a2b3c4d5e6f7g8h",
                    srcaddr="10.0.1.10",
                    dstaddr="10.0.2.20",
                    srcport=443,
                    dstport=3306,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="REJECT",
                    log_status="OK",
                    vpc_id="vpc-0abc123de456fgh78"
                ),
                FlowLog(
                    id=2,
                    account_id=123456789015,
                    interface_id="eni-02a3b4c5d6e7f8g9h",
                    srcaddr="10.0.1.11",
                    dstaddr="10.0.2.21",
                    srcport=443,
                    dstport=80,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="REJECT",
                    log_status="OK",
                    vpc_id="vpc-0abc123de456fgh75"
                ),
            ])
            print("✅ Inserted dummy FlowLog data.")

        if rca_count == 0:
            print("📌 Inserting dummy RCA Reports...")
            session.add_all([
                RCAReports(
                    id=1,
                    rca_event_id=1,
                    root_cause="Security Group misconfiguration blocking MySQL port 3306 from application subnet.",
                    recommendation="Update the SG on db instance to allow inbound TCP:3306 from app subnet 10.0.1.0/24.",
                    evidence_json='[{"dst": "10.0.2.20", "src": "10.0.1.10", "port": 3306, "action": "REJECT", "protocol": "TCP"}]',
                    created_at=datetime.fromisoformat("2025-07-21 00:22:11.202869"),
                    rca_type="low"
                ),
                RCAReports(
                    id=2,
                    rca_event_id=2,
                    root_cause="Traffic was accepted; no action needed.",
                    recommendation="None.",
                    evidence_json='{}',
                    created_at=datetime.fromisoformat("2025-07-21 00:22:11.202869"),
                    rca_type="medium"
                ),
                RCAReports(
                    id=3,
                    rca_event_id=3,
                    root_cause="Security group missing required inbound rules for SSH access (port 22)",
                    recommendation="Add inbound rule to the security group for port 22 from your IP range",
                    evidence_json='{"eventName": "AuthorizeSecurityGroupIngress", "eventTime": "2025-07-25T09:15:00Z", "userIdentity": {"type": "IAMUser", "userName": "devops-admin"}, "sourceIPAddress": "198.51.100.10"}',
                    created_at=datetime.fromisoformat("2025-07-22 12:37:29.611344"),
                    rca_type="medium"
                ),
                RCAReports(
                    id=4,
                    rca_event_id=4,
                    root_cause="NACL explicitly denying all inbound traffic on port 443",
                    recommendation="Update the NACL to allow HTTPS traffic (port 443) from external IPs",
                    evidence_json='{"eventName": "CreateNetworkAclEntry", "eventTime": "2025-07-23T14:35:21Z", "userIdentity": {"type": "Root", "userName": "root"}, "sourceIPAddress": "203.0.113.5"}',
                    created_at=datetime.fromisoformat("2025-07-24 12:37:29.611344"),
                    rca_type="high"
                ),
                RCAReports(
                    id=5,
                    rca_event_id=5,
                    root_cause="VPC route table missing route to NAT Gateway for outbound internet access",
                    recommendation="Add a route to the NAT Gateway in the route table associated with the private subnet",
                    evidence_json='{"eventName": "ReplaceRoute", "eventTime": "2025-07-22T12:00:00Z", "userIdentity": {"type": "IAMUser", "userName": "network-engineer"}, "sourceIPAddress": "192.0.2.25"}',
                    created_at=datetime.fromisoformat("2025-07-25 12:37:29.611344"),
                    rca_type="high"
                ),
                RCAReports(
                    id=6,
                    rca_event_id=6,
                    root_cause="Route table incorrectly routes internal subnet traffic to an internet gateway",
                    recommendation="Remove IGW route for internal CIDR and use proper VPC peering or private routing",
                    evidence_json='{"eventName": "CreateRoute", "eventTime": "2025-07-20T10:45:00Z", "userIdentity": {"type": "IAMUser", "userName": "infra-admin"}, "sourceIPAddress": "192.168.0.12"}',
                    created_at=datetime.fromisoformat("2025-07-20 12:39:37.67436"),
                    rca_type="medium"
                ),
                RCAReports(
                    id=7,
                    rca_event_id=7,
                    root_cause="CloudTrail shows EC2 instance was stopped manually during deployment",
                    recommendation="Implement tagging and IAM policies to restrict accidental instance shutdown",
                    evidence_json='{"eventName": "StopInstances", "eventTime": "2025-07-18T09:30:00Z", "userIdentity": {"type": "IAMUser", "userName": "developer"}, "sourceIPAddress": "10.0.0.123"}',
                    created_at=datetime.fromisoformat("2025-07-17 12:39:37.67436"),
                    rca_type="low"
                ),
                RCAReports(
                    id=8,
                    rca_event_id=8,
                    root_cause="Elastic Network Interface detached from EC2 instance causing network drop",
                    recommendation="Reattach ENI or update EC2 config to persistently attach required interfaces",
                    evidence_json='{"eventName": "DetachNetworkInterface", "eventTime": "2025-07-17T12:00:00Z", "userIdentity": {"type": "IAMUser", "userName": "netops"}, "sourceIPAddress": "172.16.2.10"}',
                    created_at=datetime.fromisoformat("2025-07-15 12:39:37.67436"),
                    rca_type="high"
                ),
                RCAReports(
                    id=9,
                    rca_event_id=9,
                    root_cause="Firewall misconfiguration blocked traffic to port 3306 (MySQL)",
                    recommendation="Allow port 3306 on security group and restrict to known IPs only",
                    evidence_json='{"eventName": "AuthorizeSecurityGroupIngress", "eventTime": "2025-07-19T11:11:00Z", "userIdentity": {"type": "IAMUser", "userName": "db-admin"}, "sourceIPAddress": "203.0.113.200"}',
                    created_at=datetime.fromisoformat("2025-07-19 12:39:37.67436"),
                    rca_type="medium"
                ),
                RCAReports(
                    id=10,
                    rca_event_id=10,
                    root_cause="Multiple failed login attempts from unknown IP detected",
                    recommendation="Block IP and enable CloudTrail alerts for failed auth events",
                    evidence_json='{"eventName": "ConsoleLogin", "eventTime": "2025-07-21T18:22:00Z", "userIdentity": {"type": "IAMUser", "userName": "unknown"}, "sourceIPAddress": "45.77.88.99"}',
                    created_at=datetime.fromisoformat("2025-07-21 12:39:37.67436"),
                    rca_type="high"
                ),
            ])
            print("✅ Inserted dummy RCAReports data.")

        await session.commit()

# --- RUN ---
if __name__ == "__main__":
    asyncio.run(test_connection())
    asyncio.run(init_db())
    asyncio.run(populate_dummy_data())
