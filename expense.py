# expense.py
import sqlite3
from db import DB_NAME

def add_expense_db(user_id, amount, category, description, date):
    """Adds an expense record for the given user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, date, description)
    )
    conn.commit()
    conn.close()

def get_expenses(user_id):
    """Retrieves a list of expenses for a given user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, category, date, description FROM Expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses
