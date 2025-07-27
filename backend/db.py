import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="techrca",
        user="postgres",
        password="admin123",
        host="localhost",
        port=5432
    )
