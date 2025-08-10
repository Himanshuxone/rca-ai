CREATE TABLE techrca (id INTEGER PRIMARY KEY, name VARCHAR);
\dt
SELECT * FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';

sudo apt install postgresql
sudo -u postgres psql template1
sudo --host localhost -u postgres psql template1
ALTER USER postgres with encrypted password 'admin123';
psql --host localhost --username postgres --password template1

himanshu@himanshu-ThinkPad-E15:/etc/postgresql/16/main$ sudo --host localhost -u postgres psql template1
sudo: a remote host may only be specified when listing privileges.
himanshu@himanshu-ThinkPad-E15:/etc/postgresql/16/main$ psql -U postgres -d postgres -c "alter user produser with password 'produser';"
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: Connection refused
	Is the server running locally and accepting connections on that socket?
himanshu@himanshu-ThinkPad-E15:/etc/postgresql/16/main$ pwd
/etc/postgresql/16/main


INSERT INTO events (id, name, description, status, created_at)
VALUES 
  (1, 'API Failure in Production', 'API response delay and timeout observed in production', 'open', NOW()),
  (2, 'Database Connection Issue', 'Unable to connect to PostgreSQL from backend service', 'resolved', NOW());


INSERT INTO rca_reports (id, rca_event_id, root_cause, rca_type, recommendation, created_at)
VALUES 
  (1, 1, 'Database connection pool exhausted', 'infrastructure', 'Increase max connections in pool', NOW()),
  (2, 2, 'Network misconfiguration on the production subnet', 'network', 'Fix route tables and add monitoring', NOW());

INSERT INTO flow_logs (id, event_id, request_payload, response_payload, status, timestamp)
VALUES 
  (1, 1, '{"action":"fetchUser","params":{"id":123}}', '{"error":"timeout"}', 'failed', NOW()),
  (2, 1, '{"action":"fetchUser","params":{"id":124}}', '{"data":{"user":"John"}}', 'success', NOW()),
  (3, 2, '{"connect_to_db":true}', '{"error":"connection refused"}', 'failed', NOW());
