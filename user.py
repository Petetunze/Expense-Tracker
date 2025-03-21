# user.py
import sqlite3
from db import DB_NAME

def register_user(username, password):
    """Registers a new user and returns (True, message) on success or (False, error_message) on failure."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose a different username."
    finally:
        conn.close()

def login_user(username, password):
    """Attempts to log in a user. Returns the user's id if successful, otherwise None."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None
