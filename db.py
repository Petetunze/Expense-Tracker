import sqlite3

DB_NAME = "expenses.db"

def init_db():
    """Initializes the database and creates tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    # Create Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
    ''')
    conn.commit()
    conn.close()
