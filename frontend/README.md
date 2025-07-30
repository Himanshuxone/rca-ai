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