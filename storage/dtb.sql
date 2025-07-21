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
