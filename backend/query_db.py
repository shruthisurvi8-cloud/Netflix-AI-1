import sqlite3

def execute_query(sql):
    conn = sqlite3.connect("../database/netflix.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(sql)

    results = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return results