import streamlit as st
from datetime import date

from db import init_db, get_connection
from auth import authenticate_researcher, register_researcher, authenticate_admin
from agent import book_equipment
from calendar_utils import get_equipment_calendar


# --------------------------------------------------
# App Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="LabAgent",
    layout="wide"
)

init_db()


# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = None

if "access_mode" not in st.session_state:
    st.session_state.access_mode = None


# --------------------------------------------------
# ACCESS PORTAL (FIRST PAGE)
# --------------------------------------------------
if not st.session_state.logged_in and st.session_state.access_mode is None:
    st.title("LabAgent Access Portal")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Login as Researcher", use_container_width=True):
            st.session_state.access_mode = "researcher"

    with col2:
        if st.button("Login as Admin", use_container_width=True):
            st.session_state.access_mode = "admin"

    with col3:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.access_mode = "signup"

    st.stop()


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------
if not st.session_state.logged_in:

    # -------- Researcher Login --------
    if st.session_state.access_mode == "researcher":
        st.title("Researcher Login")

        name = st.text_input("Full Name")

        if st.button("Login"):
            user = authenticate_researcher(name)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.role = "researcher"
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Researcher not found.")

    # -------- Admin Login --------
    elif st.session_state.access_mode == "admin":
        st.title("Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            admin = authenticate_admin(username, password)
            if admin:
                st.session_state.logged_in = True
                st.session_state.user = admin
                st.session_state.role = "admin"
                st.session_state.page = "Manage Equipment"
                st.rerun()
            else:
                st.error("Invalid admin credentials.")

    # -------- Researcher Sign Up --------
    elif st.session_state.access_mode == "signup":
        st.title("Researcher Registration")

        name = st.text_input("Full Name")
        department = st.text_input("Department")

        if st.button("Create Account"):
            user = register_researcher(name, department)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.role = "researcher"
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Researcher already exists.")

    st.stop()


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
conn = get_connection()
cur = conn.cursor()


# --------------------------------------------------
# SIDEBAR (ROLE BASED)
# --------------------------------------------------
with st.sidebar:
    st.title("LabAgent")
    st.markdown("---")

    st.write("Logged in as:")
    st.write(st.session_state.user[1])
    st.write(f"Role: {st.session_state.role}")

    st.markdown("---")

    if st.session_state.role == "admin":

        if st.button("Manage Equipment", use_container_width=True):
            st.session_state.page = "Manage Equipment"

        if st.button("View Bookings", use_container_width=True):
            st.session_state.page = "Bookings"

    else:

        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"

        if st.button("Book Equipment", use_container_width=True):
            st.session_state.page = "Book Equipment"

        if st.button("Calendar", use_container_width=True):
            st.session_state.page = "Calendar"

    st.markdown("---")

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.page = None
        st.session_state.access_mode = None
        st.rerun()


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------
st.title("LabAgent – Laboratory Equipment Scheduling Agent")


# --------------------------------------------------
# ADMIN: MANAGE EQUIPMENT
# --------------------------------------------------
if st.session_state.page == "Manage Equipment" and st.session_state.role == "admin":
    st.subheader("Manage Laboratory Equipment")

    # Add new equipment
    st.markdown("Add New Equipment")

    name = st.text_input("Equipment Name")
    interval = st.number_input("Calibration Interval (days)", min_value=1)

    if st.button("Add Equipment"):
        cur.execute("""
            INSERT INTO equipment (name, last_calibration, calibration_interval, under_maintenance)
            VALUES (?, ?, ?, 0)
        """, (name, date.today(), interval))
        conn.commit()
        st.success("Equipment added successfully.")

    st.markdown("---")

    # Update existing equipment
    equipment_list = cur.execute(
        "SELECT id, name FROM equipment"
    ).fetchall()

    selected = st.selectbox(
        "Select Equipment",
        equipment_list,
        format_func=lambda x: x[1]
    )

    cur.execute("""
        SELECT last_calibration, calibration_interval, under_maintenance
        FROM equipment WHERE id=?
    """, (selected[0],))

    last_cal, interval, maintenance = cur.fetchone()

    new_cal = st.date_input("Last Calibration Date", value=date.fromisoformat(last_cal))
    new_interval = st.number_input("Calibration Interval (days)", value=interval)
    maintenance_flag = st.checkbox("Under Maintenance", value=bool(maintenance))

    if st.button("Update Equipment"):
        cur.execute("""
            UPDATE equipment
            SET last_calibration=?, calibration_interval=?, under_maintenance=?
            WHERE id=?
        """, (new_cal, new_interval, int(maintenance_flag), selected[0]))
        conn.commit()
        st.success("Equipment updated successfully.")


# --------------------------------------------------
# RESEARCHER: DASHBOARD
# --------------------------------------------------
elif st.session_state.page == "Dashboard":
    st.subheader("Equipment Status Overview")

    equipment = cur.execute("""
        SELECT name, last_calibration, calibration_interval, under_maintenance
        FROM equipment
    """).fetchall()

    for eq in equipment:
        days = (date.today() - date.fromisoformat(eq[1])).days

        if eq[3] == 1:
            st.error(f"{eq[0]}: Under maintenance")
        elif days > eq[2]:
            st.error(f"{eq[0]}: Calibration expired")
        else:
            st.success(f"{eq[0]}: Available")


# --------------------------------------------------
# RESEARCHER: BOOK EQUIPMENT
# --------------------------------------------------
elif st.session_state.page == "Book Equipment":
    st.subheader("Book Laboratory Equipment")

    equipment = cur.execute(
        "SELECT id, name FROM equipment"
    ).fetchall()

    selected = st.selectbox(
        "Select Equipment",
        equipment,
        format_func=lambda x: x[1]
    )

    booking_date = st.date_input("Select Date", min_value=date.today())

    if st.button("Request Booking"):
        success, message = book_equipment(
            researcher_id=st.session_state.user[0],
            equipment_id=selected[0],
            booking_date=booking_date
        )

        if success:
            st.success(message)
        else:
            st.error(message)


# --------------------------------------------------
# RESEARCHER: CALENDAR
# --------------------------------------------------
elif st.session_state.page == "Calendar":
    st.subheader("Equipment Availability Calendar")

    equipment = cur.execute(
        "SELECT id, name FROM equipment"
    ).fetchall()

    selected = st.selectbox(
        "Select Equipment",
        equipment,
        format_func=lambda x: x[1]
    )

    calendar_data = get_equipment_calendar(selected[0], days=14)
    st.table(calendar_data)


# --------------------------------------------------
# BOOKINGS (ADMIN & RESEARCHER VIEW)
# --------------------------------------------------
elif st.session_state.page == "Bookings":
    st.subheader("All Bookings")

    bookings = cur.execute("""
        SELECT r.name, e.name, b.booking_date
        FROM bookings b
        JOIN researchers r ON b.researcher_id = r.id
        JOIN equipment e ON b.equipment_id = e.id
        ORDER BY b.booking_date
    """).fetchall()

    st.table(bookings)


conn.close()
