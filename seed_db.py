# seed_db.py
from db import init_db, get_connection
from datetime import date, timedelta

init_db()
conn = get_connection()
cur = conn.cursor()

# Clear old data (safe for prototype)
cur.execute("DELETE FROM bookings")
cur.execute("DELETE FROM researchers")
cur.execute("DELETE FROM equipment")
cur.execute(
    "INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)",
    ("admin", "admin123")
)


# Insert researchers
cur.executemany(
    "INSERT INTO researchers (id, name, department) VALUES (?, ?, ?)",
    [
        (1, "Ashrith Rao", "Biotechnology"),
        (2, "Akhil Ram Reddy", "Chemistry"),
        (3, "Nitta Tarun Kumar", "Physics"),
        (4,"Nandan","AI" )
    ]
)

# Insert equipment
cur.executemany(
    "INSERT INTO equipment (id, name, last_calibration, calibration_interval) VALUES (?, ?, ?, ?)",
    [
        (1, "Mass Spectrometer", date.today() - timedelta(days=10), 30),
        (2, "Confocal Microscope", date.today() - timedelta(days=45), 30)
    ]
)


conn.commit()
conn.close()

print("✅ Database seeded successfully")
