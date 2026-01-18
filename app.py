import streamlit as st
from datetime import date

from db import init_db, get_connection
from auth import authenticate_researcher, register_researcher
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

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# --------------------------------------------------
# Authentication Page (Login / Sign Up)
# --------------------------------------------------
if not st.session_state.logged_in:
    st.title("LabAgent Access Portal")

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        st.subheader("Researcher Login")
        name = st.text_input("Full Name", key="login_name")

        if st.button("Login", key="login_btn"):
            user = authenticate_researcher(name)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Researcher not found. Please sign up.")

    with tab_signup:
        st.subheader("New Researcher Registration")
        name = st.text_input("Full Name", key="signup_name")
        department = st.text_input("Department")

        if st.button("Sign Up", key="signup_btn"):
            user = register_researcher(name, department)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Researcher already exists.")

    st.stop()


# --------------------------------------------------
# Database Load
# --------------------------------------------------
conn = get_connection()
cur = conn.cursor()

equipment = cur.execute(
    "SELECT id, name, last_calibration, calibration_interval FROM equipment"
).fetchall()


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------
with st.sidebar:
    st.title("LabAgent")
    st.markdown("---")

    st.subheader("Researcher")
    st.write(st.session_state.user[1])

    st.markdown("---")
    st.subheader("Navigation")

    if st.button("Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.button("Book Equipment", use_container_width=True):
        st.session_state.page = "Book Equipment"

    if st.button("Calendar", use_container_width=True):
        st.session_state.page = "Calendar"

    if st.button("Bookings", use_container_width=True):
        st.session_state.page = "Bookings"

    st.markdown("---")

    if st.button("Logout", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "Dashboard"
        st.rerun()


# --------------------------------------------------
# Page Header
# --------------------------------------------------
st.title("LabAgent – Laboratory Equipment Scheduling Agent")
st.caption(f"Logged in as: {st.session_state.user[1]}")

page = st.session_state.page


# --------------------------------------------------
# Dashboard Page
# --------------------------------------------------
if page == "Dashboard":
    st.subheader("Equipment Health Overview")

    for eq in equipment:
        days_since = (date.today() - date.fromisoformat(eq[2])).days

        if days_since > eq[3]:
            st.error(f"{eq[1]} - Calibration expired ({days_since} days)")
        else:
            st.success(f"{eq[1]} - Calibrated ({days_since} days ago)")


# --------------------------------------------------
# Book Equipment Page
# --------------------------------------------------
elif page == "Book Equipment":
    st.subheader("Book Laboratory Equipment")

    selected_equipment = st.selectbox(
        "Select Equipment",
        equipment,
        format_func=lambda x: x[1]
    )

    booking_date = st.date_input(
        "Select Date",
        min_value=date.today()
    )

    if st.button("Request Booking"):
        success, message = book_equipment(
            researcher_id=st.session_state.user[0],
            equipment_id=selected_equipment[0],
            booking_date=booking_date
        )

        if success:
            st.success(message)
        else:
            st.error(message)


# --------------------------------------------------
# Calendar Page
# --------------------------------------------------
elif page == "Calendar":
    st.subheader("Equipment Availability Calendar")

    cal_equipment = st.selectbox(
        "Select Equipment",
        equipment,
        format_func=lambda x: x[1],
        key="calendar_equipment"
    )

    calendar_data = get_equipment_calendar(
        equipment_id=cal_equipment[0],
        days=14
    )

    st.table(calendar_data)


# --------------------------------------------------
# Bookings Page
# --------------------------------------------------
elif page == "Bookings":
    st.subheader("Current Bookings")

    bookings = cur.execute("""
        SELECT r.name, e.name, b.booking_date
        FROM bookings b
        JOIN researchers r ON b.researcher_id = r.id
        JOIN equipment e ON b.equipment_id = e.id
        ORDER BY b.booking_date
    """).fetchall()

    st.table(bookings)


conn.close()
