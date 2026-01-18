# auth.py
from db import get_connection

def authenticate_researcher(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name FROM researchers WHERE name=?",
        (name,)
    )
    user = cur.fetchone()
    conn.close()

    return user


def register_researcher(name, department):
    conn = get_connection()
    cur = conn.cursor()

    # Check if already exists
    cur.execute(
        "SELECT id FROM researchers WHERE name=?",
        (name,)
    )
    if cur.fetchone():
        conn.close()
        return None

    # Insert new researcher
    cur.execute(
        "INSERT INTO researchers (name, department) VALUES (?, ?)",
        (name, department)
    )
    conn.commit()

    # Fetch newly created user
    cur.execute(
        "SELECT id, name FROM researchers WHERE name=?",
        (name,)
    )
    user = cur.fetchone()
    conn.close()

    return user
