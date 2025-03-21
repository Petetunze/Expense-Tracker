# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from db import init_db
from user import register_user, login_user
from expense import add_expense_db, get_expenses

from styling import get_theme


class LoginFrame(ttk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.login_button = None
        self.entry_password = None
        self.entry_username = None
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_username = ttk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return
        user_id = login_user(username, password)
        if user_id is None:
            messagebox.showerror("Login Failed", "Invalid credentials.")
        else:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.on_login_success(user_id)


class RegisterFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.register_button = None
        self.entry_password = None
        self.entry_username = None
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_username = ttk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.register_button = ttk.Button(self, text="Register", command=self.register)
        self.register_button.grid(row=2, column=0, columnspan=2, pady=10)

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return
        success, msg = register_user(username, password)
        if success:
            messagebox.showinfo("Registration Successful", msg)
        else:
            messagebox.showerror("Registration Failed", msg)


class MainDashboard(ttk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.app = None
        self.refresh_button = None
        self.tree = None
        self.add_button = None
        self.entry_description = None
        self.entry_category = None
        self.entry_amount = None
        self.logout_button = None
        self.user_id = user_id
        self.create_widgets()
        self.refresh_expenses()  # Load expenses on initialization

    def logout(self):
        self.app.switch_to_auth()


    def create_widgets(self):
        # Add Expense Form
        form_frame = ttk.LabelFrame(self, text="Add Expense")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_amount = ttk.Entry(form_frame)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_category = ttk.Entry(form_frame)
        self.entry_category.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_description = ttk.Entry(form_frame)
        self.entry_description.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(form_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Expense List
        list_frame = ttk.LabelFrame(self, text="Your Expenses")
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(list_frame, columns=("Amount", "Category", "Date", "Description"), show="headings")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.column("Amount", width=80)
        self.tree.column("Category", width=100)
        self.tree.column("Date", width=100)
        self.tree.column("Description", width=200)
        self.tree.pack(fill="both", expand=True)

        self.refresh_button = ttk.Button(self, text="Refresh Expenses", command=self.refresh_expenses)
        self.refresh_button.grid(row=2, column=0, pady=5)

        self.logout_button = ttk.Button(self, text="Logout", command=self.logout_btn)
        self.logout_button.grid(row=3, column=0, pady=5)

    def add_expense(self):
        try:
            amount = float(self.entry_amount.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numerical amount.")
            return
        category = self.entry_category.get().strip()
        description = self.entry_description.get().strip()
        if not category:
            messagebox.showerror("Input Error", "Please enter a category.")
            return
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        add_expense_db(self.user_id, amount, category, description, date_str)
        messagebox.showinfo("Success", "Expense added successfully!")
        self.refresh_expenses()

    def refresh_expenses(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        for expense in get_expenses(self.user_id):
            # Each expense is (id, amount, category, date, description)
            _, amount, category, date, description = expense
            self.tree.insert("", "end", values=(amount, category, date, description))

    def logout_btn(self):
        self.master.master.switch_to_auth()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = None
        self.current_theme = None
        self.title("Expense Tracker")
        self.geometry("500x500")
        self.resizable(False, False)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.show_authentication()


    def show_authentication(self):
        self.clear_container()
        # Use a Notebook (tabbed view) for Login and Registration.
        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True)
        login_frame = LoginFrame(notebook, self.on_login_success)
        register_frame = RegisterFrame(notebook)
        notebook.add(login_frame, text="Login")
        notebook.add(register_frame, text="Register")

    def on_login_success(self, user_id):
        self.clear_container()
        dashboard = MainDashboard(self.container, user_id)
        dashboard.pack(fill="both", expand=True)

    def switch_to_auth(self):
        self.show_authentication()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def set_theme(self, mode):
        """Sets the theme based on user selection."""
        self.current_theme = get_theme(mode)
        self.apply_theme(self.current_theme)
        return self.current_theme

    def apply_theme(self, theme):
        """Apply the given theme to the entire app."""
        self.configure(bg=theme["background"])
        self.container.configure(style="Main.TFrame")
        self.style = ttk.Style()

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Select Theme:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.theme_var = tk.StringVar(value="light")  # Default to Light Mode

        # Radio buttons for theme selection
        ttk.Radiobutton(self, text="Light Mode", variable=self.theme_var, value="light", command=self.apply_theme).grid(
            row=1, column=0, padx=10, sticky="w")
        ttk.Radiobutton(self, text="Dark Mode", variable=self.theme_var, value="dark", command=self.apply_theme).grid(
            row=2, column=0, padx=10, sticky="w")

    def apply_theme(self):
        # Apply the selected theme
        selected_theme = self.theme_var.get()
        theme = self.app.set_theme(selected_theme)  # Call the Application's method to apply theme
        self.update_preview(theme)

    def update_preview(self, theme):
        # Example: Update preview of theme settings (optional)
        pass  # You could add a theme previewer here if desired


if __name__ == '__main__':
    init_db()  # Ensure the database and tables are set up.
    app = Application()
    app.mainloop()
