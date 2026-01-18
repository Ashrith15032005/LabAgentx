from datetime import date
from db import get_connection


def book_equipment(researcher_id, equipment_id, booking_date):
    conn = get_connection()
    cur = conn.cursor()

    # Fetch equipment status
    cur.execute("""
        SELECT last_calibration, calibration_interval, under_maintenance
        FROM equipment
        WHERE id=?
    """, (equipment_id,))
    result = cur.fetchone()

    if not result:
        conn.close()
        return False, "Equipment not found."

    last_calibration, calibration_interval, under_maintenance = result

    # Rule 1: Maintenance check
    if under_maintenance == 1:
        conn.close()
        return False, "Booking rejected: Equipment is under maintenance."

    # Rule 2: Calibration validity check
    days_since_calibration = (
        date.today() - date.fromisoformat(last_calibration)
    ).days

    if days_since_calibration > calibration_interval:
        conn.close()
        return False, "Booking rejected: Calibration has expired."

    # Rule 3: Booking conflict check
    cur.execute("""
        SELECT r.name
        FROM bookings b
        JOIN researchers r ON b.researcher_id = r.id
        WHERE b.equipment_id=? AND b.booking_date=?
    """, (equipment_id, booking_date))

    conflict = cur.fetchone()
    if conflict:
        conn.close()
        return False, f"Booking rejected: Already booked by {conflict[0]}."

    # Rule 4: Accept booking
    cur.execute("""
        INSERT INTO bookings (researcher_id, equipment_id, booking_date)
        VALUES (?, ?, ?)
    """, (researcher_id, equipment_id, booking_date))

    conn.commit()
    conn.close()

    return True, "Booking approved successfully."
