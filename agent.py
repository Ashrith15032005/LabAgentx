from datetime import date
from db import get_connection

def book_equipment(researcher_id, equipment_id, booking_date):
    conn = get_connection()
    cur = conn.cursor()

    # Fetch calibration details
    cur.execute(
        "SELECT last_calibration, calibration_interval FROM equipment WHERE id=?",
        (equipment_id,)
    )
    last_cal, interval = cur.fetchone()
    days = (date.today() - date.fromisoformat(last_cal)).days

    if days > interval:
        conn.close()
        return False, f"❌ Calibration expired ({days} days old)."

    # Conflict check with researcher name
    cur.execute("""
        SELECT r.name
        FROM bookings b
        JOIN researchers r ON b.researcher_id = r.id
        WHERE b.equipment_id=? AND b.booking_date=?
    """, (equipment_id, booking_date))

    conflict = cur.fetchone()
    if conflict:
        conn.close()
        return False, f"❌ Equipment already booked by {conflict[0]}."

    # Insert booking
    cur.execute("""
        INSERT INTO bookings (researcher_id, equipment_id, booking_date)
        VALUES (?, ?, ?)
    """, (researcher_id, equipment_id, booking_date))

    conn.commit()
    conn.close()
    return True, "✅ Equipment booked successfully."
