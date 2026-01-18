from db import get_connection


# --------------------------------------------------
# Researcher Authentication
# --------------------------------------------------
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

    try:
        cur.execute(
            "INSERT INTO researchers (name, department) VALUES (?, ?)",
            (name, department)
        )
        conn.commit()
    except Exception:
        conn.close()
        return None

    cur.execute(
        "SELECT id, name FROM researchers WHERE name=?",
        (name,)
    )
    user = cur.fetchone()
    conn.close()
    return user


# --------------------------------------------------
# Admin Authentication
# --------------------------------------------------
def authenticate_admin(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username FROM admin WHERE username=? AND password=?",
        (username, password)
    )

    admin = cur.fetchone()
    conn.close()
    return admin
