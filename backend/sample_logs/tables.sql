Update rca_reports Set rca_type = 'medium' where id = 1;

SELECT *
  FROM information_schema.columns
 WHERE table_schema = 'public'
   AND table_name   = 'rca_reports'
     ;

INSERT INTO rca_reports (
    root_cause, recommendation, evidence_json, created_at, rca_type
) VALUES
-- 1
(
'Security group missing required inbound rules for SSH access (port 22)',
'Add inbound rule to the security group for port 22 from your IP range',
'{
  "eventName": "AuthorizeSecurityGroupIngress",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "devops-admin"
  },
  "sourceIPAddress": "198.51.100.10",
  "eventTime": "2025-07-25T09:15:00Z"
}', 
NOW() - INTERVAL '5 days', 'medium'),

-- 2
(
'NACL explicitly denying all inbound traffic on port 443',
'Update the NACL to allow HTTPS traffic (port 443) from external IPs',
'{
  "eventName": "CreateNetworkAclEntry",
  "userIdentity": {
    "type": "Root",
    "userName": "root"
  },
  "sourceIPAddress": "203.0.113.5",
  "eventTime": "2025-07-23T14:35:21Z"
}', 
NOW() - INTERVAL '3 days', 'high'),

-- 3
( 
'VPC route table missing route to NAT Gateway for outbound internet access',
'Add a route to the NAT Gateway in the route table associated with the private subnet',
'{
  "eventName": "ReplaceRoute",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "network-engineer"
  },
  "sourceIPAddress": "192.0.2.25",
  "eventTime": "2025-07-22T12:00:00Z"
}', 
NOW() - INTERVAL '2 days', 'high');


-- Add more dummy records to reports table
INSERT INTO rca_reports (
    root_cause, recommendation, evidence_json, created_at, rca_type
) VALUES
-- 4
(
'Route table incorrectly routes internal subnet traffic to an internet gateway',
'Remove IGW route for internal CIDR and use proper VPC peering or private routing',
'{
  "eventName": "CreateRoute",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "infra-admin"
  },
  "sourceIPAddress": "192.168.0.12",
  "eventTime": "2025-07-20T10:45:00Z"
}', 
NOW() - INTERVAL '7 days', 'medium'),

-- 5
(
'CloudTrail shows EC2 instance was stopped manually during deployment',
'Implement tagging and IAM policies to restrict accidental instance shutdown',
'{
  "eventName": "StopInstances",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "developer"
  },
  "sourceIPAddress": "10.0.0.123",
  "eventTime": "2025-07-18T09:30:00Z"
}', 
NOW() - INTERVAL '10 days', 'low'),

-- 6
(
'Elastic Network Interface detached from EC2 instance causing network drop',
'Reattach ENI or update EC2 config to persistently attach required interfaces',
'{
  "eventName": "DetachNetworkInterface",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "netops"
  },
  "sourceIPAddress": "172.16.2.10",
  "eventTime": "2025-07-17T12:00:00Z"
}', 
NOW() - INTERVAL '12 days', 'high'),

-- 7
(
'Firewall misconfiguration blocked traffic to port 3306 (MySQL)',
'Allow port 3306 on security group and restrict to known IPs only',
'{
  "eventName": "AuthorizeSecurityGroupIngress",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "db-admin"
  },
  "sourceIPAddress": "203.0.113.200",
  "eventTime": "2025-07-19T11:11:00Z"
}', 
NOW() - INTERVAL '8 days', 'medium'),

-- 8
(
'Multiple failed login attempts from unknown IP detected',
'Block IP and enable CloudTrail alerts for failed auth events',
'{
  "eventName": "ConsoleLogin",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "unknown"
  },
  "sourceIPAddress": "45.77.88.99",
  "eventTime": "2025-07-21T18:22:00Z"
}', 
NOW() - INTERVAL '6 days', 'high');

------- count the risks vul

SELECT rca_type, COUNT(*) AS count
FROM reports
GROUP BY rca_type
ORDER BY count DESC;