import sqlite3
from datetime import date, timedelta

DB_NAME = "labagent.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Researchers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS researchers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        department TEXT
    )
    """)

    # Equipment
    cur.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        last_calibration DATE,
        calibration_interval INTEGER,
        under_maintenance INTEGER DEFAULT 0
    )
    """)

    # Bookings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        researcher_id INTEGER,
        equipment_id INTEGER,
        booking_date DATE,
        FOREIGN KEY (researcher_id) REFERENCES researchers(id),
        FOREIGN KEY (equipment_id) REFERENCES equipment(id)
    )
    """)

    # Admin (THIS WAS MISSING)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()
