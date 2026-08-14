import sqlite3
import os

DB_PATH = os.path.join("data", "db", "reception.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS call_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caller_name TEXT,
            caller_intent TEXT,
            callback_number TEXT,
            urgency_level TEXT,
            raw_transcript TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_call(name: str, intent: str, phone: str, urgency: str, transcript: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO call_records (caller_name, caller_intent, callback_number, urgency_level, raw_transcript)
        VALUES (?, ?, ?, ?, ?)
    """, (name, intent, phone, urgency, transcript))
    conn.commit()
    conn.close()

def fetch_all_calls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, caller_name, callback_number, urgency_level, caller_intent, raw_transcript FROM call_records ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records