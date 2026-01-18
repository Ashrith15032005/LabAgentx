from datetime import date

def check_calibration(equipment):
    days = (date.today() - equipment["last_calibration"]).days
    return days <= equipment["calibration_interval"], days

def check_conflict(bookings, equipment_id, requested_date):
    for booking in bookings:
        if booking["equipment_id"] == equipment_id and booking["date"] == requested_date:
            return booking
    return None

def process_booking(equipment, bookings, request):
    ok, days = check_calibration(equipment)
    if not ok:
        return False, f"❌ Booking rejected: Calibration expired ({days} days old)."

    conflict = check_conflict(bookings, equipment["id"], request["date"])
    if conflict:
        if request["priority"] > conflict["priority"]:
            bookings.remove(conflict)
            bookings.append(request)
            return True, "⚠️ Conflict resolved: higher priority booking approved."
        else:
            return False, "❌ Slot unavailable: already booked by higher priority user."

    bookings.append(request)
    return True, "✅ Booking approved."
