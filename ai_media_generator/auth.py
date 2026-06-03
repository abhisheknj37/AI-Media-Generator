import sqlite3
import re

def init_db():
    """Initializes the database and creates the users table."""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # We use 'username' as the column name to match your login function
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def valid_email(email):
    """Checks if the provided string follows a basic email pattern."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def strong_password(p):
    """
    Validates password strength:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    return (
        len(p) >= 8 and
        re.search(r"[A-Z]", p) and
        re.search(r"[a-z]", p) and
        re.search(r"[0-9]", p) and
        re.search(r"[!@#$%^&*]", p)
    )


def register(username, password):
    """Registers a new user after validating email and password."""
    if not valid_email(username):
        return "invalid_email"

    if not strong_password(password):
        return "weak_password"

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        status = "success"
    except sqlite3.IntegrityError:
        status = "exists"
    except Exception as e:
        status = f"error: {str(e)}"
    finally:
        conn.close()
    
    return status


def login(username, password):
    """Checks credentials against the database."""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Explicitly naming the columns helps prevent errors
    c.execute("SELECT username, password FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()

    conn.close()
    return data


def reset_password(username, new_password):
    """Updates the password for an existing username."""
    if not strong_password(new_password):
        return False

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    
    # Check if the user actually existed to be updated
    success = c.rowcount > 0
    
    conn.commit()
    conn.close()

    return success