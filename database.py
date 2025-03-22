import sqlite3
import hashlib

DATABASE = "expense_tracker.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            name TEXT,
            description TEXT,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash the password using SHA256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def add_user(username, email, password):
    """Add a new user to the database. Returns True if successful, False if username exists."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Likely a duplicate username
        return False
    finally:
        conn.close()

def get_user(username):
    """Retrieve a user record by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user(username, password):
    """
    Verify credentials.
    Returns a tuple (True, user_id) if valid, or (False, None) if not.
    """
    user = get_user(username)
    if not user:
        return False, None
    user_id, user_name, email, db_password = user
    hashed = hash_password(password)
    if hashed == db_password:
        return True, user_id
    return False, None

def add_expense(user_id, amount, name, description, date):
    """Add a new expense for the given user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, amount, name, description, date) VALUES (?, ?, ?, ?, ?)",
                   (user_id, amount, name, description, date))
    conn.commit()
    conn.close()

def get_expenses(user_id):
    """Return a list of expenses for the given user. Each expense is a tuple: (amount, name, description, date)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount, name, description, date FROM expenses WHERE user_id=?", (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# You might want to initialize the database tables on startup.


