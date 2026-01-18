from datetime import date, timedelta

equipment_db = [
    {
        "id": 1,
        "name": "Mass Spectrometer",
        "last_calibration": date.today() - timedelta(days=10),
        "calibration_interval": 30,
        "status": "available"
    },
    {
        "id": 2,
        "name": "Confocal Microscope",
        "last_calibration": date.today() - timedelta(days=50),
        "calibration_interval": 30,
        "status": "available"
    }
]

bookings = []
