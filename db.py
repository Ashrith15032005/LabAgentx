import sqlite3
from datetime import date, timedelta

def get_connection():
    return sqlite3.connect("labagent.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS researchers(
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS equipment(
        id INTEGER PRIMARY KEY,
        name TEXT,
        last_calibration DATE,
        calibration_interval INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY,
        researcher_id INTEGER,
        equipment_id INTEGER,
        booking_date DATE,
        priority INTEGER
    )""")

    conn.commit()
    conn.close()
