import sqlite3

DB_NAME = "llm_logs.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS llm_calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        prompt_version TEXT,
        response TEXT,
        model TEXT,
        input_tokens INTEGER,
        output_tokens INTEGER,
        estimated_cost REAL,
        latency_ms REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        llm_call_id INTEGER,
        rule_score REAL,
        judge_score REAL,
        judge_reasoning TEXT,
        details TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(llm_call_id) REFERENCES llm_calls(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS regressions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        old_call_id INTEGER,
        new_call_id INTEGER,
        score_delta REAL,
        verdict TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

