# 🔬 LabAgent – Laboratory Equipment Scheduling Agent

LabAgent is a web-based intelligent scheduling system designed to manage
shared, high-value laboratory equipment such as mass spectrometers and
confocal microscopes. The system automates booking decisions by considering
equipment calibration status, existing reservations, and researcher identity.

---

## 🚀 Features

- Researcher Login & Sign-Up
- Equipment Booking System
- Automatic Conflict Detection
- Calibration-Aware Scheduling
- Equipment Availability Calendar
- Displays Researcher Name for Existing Bookings
- Session-Based Authentication
- Clean, Tab-Based User Interface

---

## 🧠 System Architecture

Streamlit Web UI
↓
Authentication Module
↓
LabAgent Scheduling Logic
↓
SQLite Database

---

## 🗂️ Project Structure

labagent_prototype/
│
├── app.py # Streamlit UI & navigation
├── db.py # Database connection & initialization
├── auth.py # Login & Sign-up logic
├── agent.py # Booking & conflict resolution logic
├── calendar_utils.py # Availability calendar generation
├── seed_db.py # One-time database seeding
├── requirements.txt
└── README.md

---

## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
# LabAgentx
