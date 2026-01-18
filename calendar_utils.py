# calendar_utils.py
from datetime import date, timedelta
from db import get_connection

def get_equipment_calendar(equipment_id, days=14):
    conn = get_connection()
    cur = conn.cursor()

    # Get equipment calibration info
    cur.execute("""
        SELECT last_calibration, calibration_interval
        FROM equipment WHERE id=?
    """, (equipment_id,))
    last_cal, interval = cur.fetchone()

    last_cal = date.fromisoformat(last_cal)
    calibration_valid_until = last_cal + timedelta(days=interval)

    # Get bookings
    cur.execute("""
    SELECT booking_date, r.name
    FROM bookings b
    JOIN researchers r ON b.researcher_id = r.id
    WHERE equipment_id=?
""", (equipment_id,))

    booking_map = {date.fromisoformat(d): name for d, name in cur.fetchall()}

    conn.close()

    calendar = []
    today = date.today()

    for i in range(days):
        current = today + timedelta(days=i)

        if current > calibration_valid_until:
            status = "⚠️ Calibration Required"
        elif current in booking_map:
            status = f"🔴 Booked ({booking_map[current]})"
        else:
            status = "🟢 Available"

        calendar.append({
            "Date": current,
            "Status": status
        })

    return calendar
