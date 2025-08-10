## Database connectivty
- Running docker compose
```shell
himanshu@himanshu-ThinkPad-E15:~/workspace/AI/rca-ai$ docker-compose up --build
himanshu@himanshu-ThinkPad-E15:~/workspace/AI/rca-ai$ docker-compose down -v
```
- Testing database connectivity when running all backend pods of connectivty
```shell
himanshu@himanshu-ThinkPad-E15:~/workspace/AI/rca-ai$ docker-compose exec backend python init_db.py
2025-07-30 18:55:23,751 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2025-07-30 18:55:23,751 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-07-30 18:55:23,754 INFO sqlalchemy.engine.Engine select current_schema()
2025-07-30 18:55:23,754 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-07-30 18:55:23,757 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2025-07-30 18:55:23,757 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-07-30 18:55:23,759 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-07-30 18:55:23,759 INFO sqlalchemy.engine.Engine SELECT 1
2025-07-30 18:55:23,759 INFO sqlalchemy.engine.Engine [generated in 0.00030s] ()
2025-07-30 18:55:23,760 INFO sqlalchemy.engine.Engine ROLLBACK
✅ Database connection successful.
```

### Verifying the database
```shell
himanshu@himanshu-ThinkPad-E15:~/workspace/AI/rca-ai$ docker container ls
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
7faec744abc2   rca-ai-frontend   "/docker-entrypoint.…"   13 minutes ago   Up 13 minutes             0.0.0.0:3000->80/tcp, [::]:3000->80/tcp       rca-ai-frontend
68693bcc4ec2   rca-ai-backend    "uvicorn main:app --…"   13 minutes ago   Up 13 minutes             0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   rca-ai-backend
ff950240d8c4   postgres:15       "docker-entrypoint.s…"   13 minutes ago   Up 13 minutes (healthy)   5432/tcp                                      rca-ai-db
himanshu@himanshu-ThinkPad-E15:~/workspace/AI/rca-ai$ docker exec -it rca-ai-db sh
# psql -U postgres -h localhost -d testdb
psql: error: connection to server at "localhost" (::1), port 5432 failed: FATAL:  database "testdb" does not exist
# psql -U postgres -h localhost -d techrca
psql (15.13 (Debian 15.13-1.pgdg120+1))
Type "help" for help.

techrca=# \dt
            List of relations
 Schema |    Name     | Type  |  Owner   
--------+-------------+-------+----------
 public | flow_logs   | table | postgres
 public | rca_reports | table | postgres
(2 rows)

techrca=# Select * from rca_reports;
 id | rca_event_id | root_cause | rca_type | recommendation | created_at 
----+--------------+------------+----------+----------------+------------
(0 rows)

techrca=# himanshu@himanshu-ThinkPad-E15:~/workspace/AI/rca-ai$ docker exec -it rca-ai-db sh
# psql -U postgres -h localhost -d techrca
psql (15.13 (Debian 15.13-1.pgdg120+1))
Type "help" for help.

techrca=# \dt
            List of relations
 Schema |    Name     | Type  |  Owner   
--------+-------------+-------+----------
 public | flow_logs   | table | postgres
 public | rca_events  | table | postgres
 public | rca_reports | table | postgres
(3 rows)

techrca=# Select * from flow_logs;
 id | account_id | vpc_id | interface_id | srcaddr | dstaddr | srcport | dstport | protocol | action | log_status | start_time 
----+------------+--------+--------------+---------+---------+---------+---------+----------+--------+------------+------------
(0 rows)

techrca=# Select * from rca_events;
 id | rca_type | severity | summary | status | created_at 
----+----------+----------+---------+--------+------------
(0 rows)

techrca=# Select * from rca_reports;
 id | rca_event_id | root_cause | rca_type | recommendation | created_at 
----+--------------+------------+----------+----------------+------------
(0 rows)

```
### Selecting data from the tables
```shell
techrca=# \dt
            List of relations
 Schema |    Name     | Type  |  Owner   
--------+-------------+-------+----------
 public | flow_logs   | table | postgres
 public | rca_reports | table | postgres
(2 rows)

techrca=# SELECT rca_reports.id, rca_reports.rca_event_id, rca_reports.root_cause, rca_reports.rca_type, rca_reports.recommendation, rca_reports.created_at FROM rca_reports;
 id | rca_event_id |        root_cause         | rca_type |   recommendation    |         created_at         
----+--------------+---------------------------+----------+---------------------+----------------------------
  1 |            1 | Connection pool exhausted | infra    | Increase pool size  | 2025-08-09 19:21:47.137627
  2 |            2 | Incorrect configuration   | ops      | Fix database config | 2025-08-09 19:21:47.137666
(2 rows)

techrca=# SELECT flow_logs.id, flow_logs.account_id, flow_logs.vpc_id, flow_logs.interface_id, flow_logs.srcaddr, flow_logs.dstaddr, flow_logs.srcport, flow_logs.dstport, flow_logs.protocol, flow_logs.action, flow_logs.log_status, flow_logs.start_time from flow_logs;
 id |  account_id  |        vpc_id         |     interface_id      |  srcaddr  |  dstaddr  | srcport | dstport | protocol | action | log_status |         start_time         
----+--------------+-----------------------+-----------------------+-----------+-----------+---------+---------+----------+--------+------------+----------------------------
  1 | 123456789012 | vpc-0abc123de456fgh78 | eni-01a2b3c4d5e6f7g8h | 10.0.1.10 | 10.0.2.20 |     443 |    3306 |        6 | REJECT | OK         | 2025-08-09 19:21:47.135122
  2 | 123456789015 | vpc-0abc123de456fgh75 | eni-02a3b4c5d6e7f8g9h | 10.0.1.11 | 10.0.2.21 |     443 |      80 |        6 | REJECT | OK         | 2025-08-09 19:21:47.137523
(2 rows)

```