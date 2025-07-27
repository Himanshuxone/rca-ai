# backend/rca_report_stats.py
from typing import List, Dict

class RCAReportStats:
    def __init__(self, db_conn):
        self.conn = db_conn

    def get_rca_type_counts(self):
        query = """
        SELECT rca_type, COUNT(*) AS count
        FROM rca_reports
        GROUP BY rca_type;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}
