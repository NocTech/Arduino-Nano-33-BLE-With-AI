import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS temperature_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def log_temperature(temp):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    c.execute(
        "INSERT INTO temperature_log (timestamp, temperature) VALUES (?, ?)", (now, temp))
    conn.commit()
    conn.close()
