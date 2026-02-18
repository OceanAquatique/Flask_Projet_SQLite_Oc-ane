import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tasks.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema_tasks.sql")

def main():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    print(f"✅ Base créée : {DB_PATH}")

if __name__ == "__main__":
    main()
