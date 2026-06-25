import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "netflix.db")

def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    return [dict(zip(columns, row)) for row in rows]