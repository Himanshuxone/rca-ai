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
from models.rca_events import RCAEvents

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
        event_count = (await session.execute(text("SELECT COUNT(*) FROM rca_events"))).scalar()

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
                FlowLog(
                    id=3,
                    account_id=123456789018,
                    interface_id="eni-03x4y5z6a7b8c9d0e",
                    srcaddr="10.0.3.15",
                    dstaddr="10.0.4.25",
                    srcport=22,
                    dstport=22,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="ACCEPT",
                    log_status="OK",
                    vpc_id="vpc-0xyz987lk654mno32"
                ),
                FlowLog(
                    id=4,
                    account_id=123456789019,
                    interface_id="eni-04p5q6r7s8t9u0v1w",
                    srcaddr="10.0.5.12",
                    dstaddr="10.0.6.22",
                    srcport=8080,
                    dstport=443,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="ACCEPT",
                    log_status="OK",
                    vpc_id="vpc-0pqr321st654uvw99"
                ),
                FlowLog(
                    id=5,
                    account_id=123456789020,
                    interface_id="eni-05a6b7c8d9e0f1g2h",
                    srcaddr="172.16.0.5",
                    dstaddr="172.16.1.25",
                    srcport=53,
                    dstport=53,
                    protocol=17,
                    start_time=datetime.utcnow(),
                    action="REJECT",
                    log_status="NODATA",
                    vpc_id="vpc-0aaa111bbb222ccc33"
                ),
                FlowLog(
                    id=6,
                    account_id=123456789021,
                    interface_id="eni-06c7d8e9f0g1h2i3j",
                    srcaddr="192.168.1.10",
                    dstaddr="192.168.1.20",
                    srcport=25,
                    dstport=25,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="REJECT",
                    log_status="OK",
                    vpc_id="vpc-0eee444fff555ggg66"
                ),
                FlowLog(
                    id=7,
                    account_id=123456789022,
                    interface_id="eni-07h8i9j0k1l2m3n4o",
                    srcaddr="192.168.2.15",
                    dstaddr="192.168.3.25",
                    srcport=123,
                    dstport=123,
                    protocol=17,
                    start_time=datetime.utcnow(),
                    action="ACCEPT",
                    log_status="OK",
                    vpc_id="vpc-0hhh777iii888jjj99"
                ),
                FlowLog(
                    id=8,
                    account_id=123456789023,
                    interface_id="eni-08m9n0o1p2q3r4s5t",
                    srcaddr="10.1.0.15",
                    dstaddr="10.1.1.25",
                    srcport=3389,
                    dstport=3389,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="REJECT",
                    log_status="OK",
                    vpc_id="vpc-0kkk111lll222mmm33"
                ),
                FlowLog(
                    id=9,
                    account_id=123456789024,
                    interface_id="eni-09z1y2x3w4v5u6t7s",
                    srcaddr="10.2.0.5",
                    dstaddr="10.2.1.15",
                    srcport=8081,
                    dstport=3000,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="ACCEPT",
                    log_status="OK",
                    vpc_id="vpc-0zzz111yyy222xxx44"
                ),
                FlowLog(
                    id=10,
                    account_id=123456789025,
                    interface_id="eni-10a1b2c3d4e5f6g7h",
                    srcaddr="10.3.2.12",
                    dstaddr="10.3.3.18",
                    srcport=1521,
                    dstport=1521,
                    protocol=6,
                    start_time=datetime.utcnow(),
                    action="REJECT",
                    log_status="OK",
                    vpc_id="vpc-0mno111pqr222stu55"
                )
            ])
            print("✅ Inserted dummy FlowLog data.")

        if event_count == 0:
            print("📌 Inserting dummy events...")
            session.add_all([
                RCAEvents(id=1, flow_log_id=1, rca_type="blocked_port", severity="high",
                        detected_at=datetime(2025, 7, 21, 0, 21, 54, 71300),
                        summary="Database traffic blocked from app server", status="new",
                        created_at=datetime(2025, 7, 21, 0, 21, 54, 71300)),
                RCAEvents(id=2, flow_log_id=2, rca_type="normal_traffic", severity="low",
                        detected_at=datetime(2025, 7, 21, 0, 21, 54, 71300),
                        summary="No anomalies detected for this flow", status="resolved",
                        created_at=datetime(2025, 7, 21, 0, 21, 54, 71300)),
                RCAEvents(id=3, flow_log_id=3, rca_type="malware_detected", severity="critical",
                        detected_at=datetime(2025, 7, 22, 10, 15, 0),
                        summary="Malware signature detected in incoming packet", status="new",
                        created_at=datetime(2025, 7, 22, 10, 15, 0)),
                RCAEvents(id=4, flow_log_id=4, rca_type="blocked_port", severity="medium",
                        detected_at=datetime(2025, 7, 22, 11, 30, 0),
                        summary="Port 22 blocked from unauthorized IP", status="in_progress",
                        created_at=datetime(2025, 7, 22, 11, 30, 0)),
                RCAEvents(id=5, flow_log_id=5, rca_type="latency_issue", severity="high",
                        detected_at=datetime(2025, 7, 23, 9, 5, 0),
                        summary="Unusual network latency detected between regions", status="new",
                        created_at=datetime(2025, 7, 23, 9, 5, 0)),
                RCAEvents(id=6, flow_log_id=6, rca_type="packet_loss", severity="medium",
                        detected_at=datetime(2025, 7, 23, 14, 40, 0),
                        summary="Packet loss detected in internal network segment", status="new",
                        created_at=datetime(2025, 7, 23, 14, 40, 0)),
                RCAEvents(id=7, flow_log_id=7, rca_type="normal_traffic", severity="low",
                        detected_at=datetime(2025, 7, 24, 8, 55, 0),
                        summary="Traffic patterns normal", status="resolved",
                        created_at=datetime(2025, 7, 24, 8, 55, 0)),
                RCAEvents(id=8, flow_log_id=8, rca_type="malware_detected", severity="critical",
                        detected_at=datetime(2025, 7, 25, 13, 20, 0),
                        summary="Trojan activity flagged on port 8080", status="in_progress",
                        created_at=datetime(2025, 7, 25, 13, 20, 0)),
                RCAEvents(id=9, flow_log_id=9, rca_type="blocked_port", severity="high",
                        detected_at=datetime(2025, 7, 26, 16, 45, 0),
                        summary="Port 3306 blocked due to unauthorized access attempt", status="new",
                        created_at=datetime(2025, 7, 26, 16, 45, 0)),
                RCAEvents(id=10, flow_log_id=10, rca_type="latency_issue", severity="low",
                        detected_at=datetime(2025, 7, 27, 7, 15, 0),
                        summary="Minor latency spike detected during peak hours", status="resolved",
                        created_at=datetime(2025, 7, 27, 7, 15, 0))
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
