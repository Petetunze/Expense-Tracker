'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import config
from database import get_expenses, add_expense

class Dashboard:
    def __init__(self, parent, username, user_id):
        self.parent = parent
        self.username = username
        self.user_id = user_id

        self.parent.title("Dashboard - " + username)
        self.parent.geometry("600x500")

        # Main container frame.
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(expand=True, fill="both")

        # Greeting label.
        self.lbl_greeting = ttk.Label(self.frame, text=self.get_greeting(), font=("Helvetica", 16))
        self.lbl_greeting.pack(pady=10)

        # --- Expense Entry Panel ---
        self.add_panel = ttk.Frame(self.frame)
        self.add_panel.pack(fill="x", padx=10, pady=10)

        # Expense Amount.
        lbl_amount = ttk.Label(self.add_panel, text="Amount:")
        lbl_amount.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_amount = ttk.Entry(self.add_panel)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Expense Name.
        lbl_name = ttk.Label(self.add_panel, text="Name:")
        lbl_name.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_name = ttk.Entry(self.add_panel)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Expense Description.
        lbl_desc = ttk.Label(self.add_panel, text="Description:")
        lbl_desc.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_desc = ttk.Entry(self.add_panel)
        self.entry_desc.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Expense Date - Radiobuttons for "Today" and "Other".
        lbl_date = ttk.Label(self.add_panel, text="Date:")
        lbl_date.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.date_mode = tk.IntVar(value=0)  # 0: Today, 1: Other.
        rb_today = ttk.Radiobutton(
            self.add_panel,
            text="Today",
            variable=self.date_mode,
            value=0,
            command=self.toggle_date_entry
        )
        rb_today.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        rb_other = ttk.Radiobutton(
            self.add_panel,
            text="Other:",
            variable=self.date_mode,
            value=1,
            command=self.toggle_date_entry
        )
        rb_other.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_date = ttk.Entry(self.add_panel, width=12)
        self.entry_date.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.entry_date.configure(state="disabled")

        # Button to add expense.
        self.btn_add_expense = ttk.Button(self.add_panel, text="Add Expense", command=self.handle_add_expense)
        self.btn_add_expense.grid(row=4, column=0, columnspan=4, pady=10)

        # --- Expenses Listing ---
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Amount", "Name", "Description", "Date"),
            show="headings"
        )
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Date", text="Date")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.populate_expenses()

        # --- Logout Button ---
        # The logout button is placed in its own frame and centered horizontally.
        logout_frame = ttk.Frame(self.frame)
        logout_frame.pack(fill="x", pady=10)
        self.btn_logout = ttk.Button(logout_frame, text="Logout", command=self.logout)
        self.btn_logout.pack(anchor="center")

        # Apply the global theme.
        self.apply_theme(config.THEMES[config.CURRENT_THEME])

    def get_greeting(self):
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good Morning, "
        elif current_hour < 18:
            greeting = "Good Afternoon, "
        else:
            greeting = "Good Evening, "
        return greeting + self.username

    def toggle_date_entry(self):
        """Enable or disable the date entry field based on the radio selection."""
        if self.date_mode.get() == 1:
            self.entry_date.configure(state="normal")
        else:
            self.entry_date.delete(0, tk.END)
            self.entry_date.configure(state="disabled")

    def handle_add_expense(self):
        # Gather input values.
        amount_text = self.entry_amount.get().strip()
        name = self.entry_name.get().strip()
        description = self.entry_desc.get().strip()

        # Determine the expense date.
        if self.date_mode.get() == 0:
            expense_date = date.today().isoformat()
        else:
            expense_date = self.entry_date.get().strip()

        # Validate amount.
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return

        # Validate the date if "Other" is chosen.
        if self.date_mode.get() == 1:
            try:
                datetime.strptime(expense_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
                return

        # Save the expense.
        add_expense(self.user_id, amount, name, description, expense_date)
        self.populate_expenses()

        # Clear input fields.
        self.entry_amount.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        if self.date_mode.get() == 1:
            self.entry_date.delete(0, tk.END)
        # Reset to "Today"
        self.date_mode.set(0)
        self.toggle_date_entry()

    def populate_expenses(self):
        """Clear and refresh the expense list from the database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        expenses = get_expenses(self.user_id)  # Expected tuple: (amount, name, description, expense_date)
        if expenses:
            for expense in expenses:
                self.tree.insert("", tk.END, values=expense)
        else:
            self.tree.insert("", tk.END, values=("0.00", "No expenses", "", ""))

    def logout(self):
        """Clear the current dashboard and display the original Notebook with Login, Register, & Settings."""
        root = self.parent
        for widget in root.winfo_children():
            widget.destroy()

        # Re-import the main view tabs.
        from gui.login_tab import LoginTab
        from gui.register_tab import RegisterTab
        from gui.settings_tab import SettingsTab

        # Re-create the main Notebook view.
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        login_tab = LoginTab(notebook)
        register_tab = RegisterTab(notebook)
        # For Settings, pass a dummy callback; in a full application, you might want to
        # hook this up to a proper theme update function.
        settings_tab = SettingsTab(notebook, lambda theme_name: None)

        notebook.add(login_tab.frame, text="Login")
        notebook.add(register_tab.frame, text="Register")
        notebook.add(settings_tab.frame, text="Settings")

        # Apply the current theme.
        login_tab.apply_theme(config.THEMES[config.CURRENT_THEME])
        register_tab.apply_theme(config.THEMES[config.CURRENT_THEME])
        settings_tab.apply_theme(config.THEMES[config.CURRENT_THEME])

    def apply_theme(self, theme):
        style = ttk.Style(self.parent)
        style.theme_use("clam")
        style.configure("Custom.TFrame", background=theme["bg"])
        style.configure(
            "Custom.TLabel",
            background=theme["bg"],
            foreground=theme["fg"]
        )
        style.configure(
            "Custom.Treeview",
            background=theme["entry_bg"],
            fieldbackground=theme["entry_bg"],
            foreground=theme["fg"]
        )

        self.parent.configure(bg=theme["bg"])
        self.frame.configure(style="Custom.TFrame")
        self.lbl_greeting.configure(style="Custom.TLabel")
        self.tree.configure(style="Custom.Treeview")
'''

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import config
from database import get_expenses, add_expense

class Dashboard:
    def __init__(self, parent, username, user_id):
        self.parent = parent
        self.username = username
        self.user_id = user_id

        self.parent.title("Dashboard - " + username)
        self.parent.geometry("800x700")

        # Main container frame.
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(expand=True, fill="both")

        # Greeting label.
        self.lbl_greeting = ttk.Label(self.frame, text=self.get_greeting(), font=("Helvetica", 16))
        self.lbl_greeting.pack(pady=10)

        # --- Expense Entry Panel ---
        self.add_panel = ttk.Frame(self.frame)
        self.add_panel.pack(fill="x", padx=10, pady=10)

        # Expense Amount.
        self.lbl_amount = ttk.Label(self.add_panel, text="Amount:")
        self.lbl_amount.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_amount = ttk.Entry(self.add_panel)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Expense Name.
        self.lbl_name = ttk.Label(self.add_panel, text="Name:")
        self.lbl_name.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_name = ttk.Entry(self.add_panel)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Expense Description.
        self.lbl_desc = ttk.Label(self.add_panel, text="Description:")
        self.lbl_desc.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_desc = ttk.Entry(self.add_panel)
        self.entry_desc.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Expense Date - Radiobuttons for "Today" and "Other".
        self.lbl_date = ttk.Label(self.add_panel, text="Date:")
        self.lbl_date.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.date_mode = tk.IntVar(value=0)  # 0: Today, 1: Other.
        self.rb_today = ttk.Radiobutton(
            self.add_panel,
            text="Today",
            variable=self.date_mode,
            value=0,
            command=self.toggle_date_entry
        )
        self.rb_today.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.rb_other = ttk.Radiobutton(
            self.add_panel,
            text="Other:",
            variable=self.date_mode,
            value=1,
            command=self.toggle_date_entry
        )
        self.rb_other.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_date = ttk.Entry(self.add_panel, width=12)
        self.entry_date.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.entry_date.configure(state="disabled")

        # Button to add expense.
        self.btn_add_expense = ttk.Button(self.add_panel, text="Add Expense", command=self.handle_add_expense)
        self.btn_add_expense.grid(row=4, column=0, columnspan=4, pady=10)

        # --- Expenses Listing ---
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Amount", "Name", "Description", "Date"),
            show="headings"
        )

        self.tree.column("Amount", width=100)  # set the width of the Amount column to 100 pixels
        self.tree.column("Name", width=150)  # set the width of the Name column to 150 pixels
        self.tree.column("Description", width=200)  # set the width of the Description column to 200 pixels
        self.tree.column("Date", width=120)  # set the width of the Date column to 120 pixels

        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Date", text="Date")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.populate_expenses()

        # --- Logout Button ---
        logout_frame = ttk.Frame(self.frame)
        logout_frame.pack(fill="x", pady=10)
        self.btn_logout = ttk.Button(logout_frame, text="Logout", command=self.logout)
        self.btn_logout.pack(anchor="center")

        # Apply the global theme.
        self.apply_theme(config.THEMES[config.CURRENT_THEME])

    def get_greeting(self):
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good Morning, "
        elif current_hour < 18:
            greeting = "Good Afternoon, "
        else:
            greeting = "Good Evening, "
        return greeting + self.username

    def toggle_date_entry(self):
        if self.date_mode.get() == 1:
            self.entry_date.configure(state="normal")
        else:
            self.entry_date.delete(0, tk.END)
            self.entry_date.configure(state="disabled")

    def handle_add_expense(self):
        amount_text = self.entry_amount.get().strip()
        name = self.entry_name.get().strip()
        description = self.entry_desc.get().strip()

        if self.date_mode.get() == 0:
            expense_date = date.today().isoformat()
        else:
            expense_date = self.entry_date.get().strip()

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return

        if self.date_mode.get() == 1:
            try:
                datetime.strptime(expense_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
                return

        add_expense(self.user_id, amount, name, description, expense_date)
        self.populate_expenses()

        self.entry_amount.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        if self.date_mode.get() == 1:
            self.entry_date.delete(0, tk.END)
        self.date_mode.set(0)
        self.toggle_date_entry()

    def populate_expenses(self):
        # Clear the existing items in the Treeview.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch the expenses for this user.
        expenses = get_expenses(self.user_id)  # Expected tuple: (amount, name, description, expense_date)
        if expenses:
            for expense in expenses:
                amount, name, description, expense_date = expense

                # Format the date (convert from YYYY-MM-DD to "Month Day, Year").
                try:
                    formatted_date = datetime.strptime(expense_date, "%Y-%m-%d").strftime("%B %d, %Y")
                except ValueError:
                    # Handle any malformed dates by falling back to the original date string.
                    formatted_date = expense_date

                # Insert the expense into the Treeview.
                self.tree.insert("", tk.END, values=(amount, name, description, formatted_date))
        else:
            # Display a placeholder row if there are no expenses.
            self.tree.insert("", tk.END, values=("0.00", "No expenses", "", ""))

    def logout(self):
        """Clear the current dashboard and display the original Notebook with Login, Register, & Settings."""
        root = self.parent
        for widget in root.winfo_children():
            widget.destroy()

        # Re-import the main view tabs.
        from gui.login_tab import LoginTab
        from gui.register_tab import RegisterTab
        from gui.settings_tab import SettingsTab

        # Create the main Notebook view.
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        # Import the main app's update_theme method.
        app = root  # Assuming `root` is the main application instance.

        login_tab = LoginTab(notebook)
        register_tab = RegisterTab(notebook)
        settings_tab = SettingsTab(notebook, app.update_theme)  # Hook the update_theme method here.

        notebook.add(login_tab.frame, text="Login")
        notebook.add(register_tab.frame, text="Register")
        notebook.add(settings_tab.frame, text="Settings")

        # Apply the current theme.
        login_tab.apply_theme(config.THEMES[config.CURRENT_THEME])
        register_tab.apply_theme(config.THEMES[config.CURRENT_THEME])
        settings_tab.apply_theme(config.THEMES[config.CURRENT_THEME])

    def apply_theme(self, theme):

        if hasattr(self, 'login_tab') and self.login_tab and self.login_tab.frame.winfo_exists():
            self.login_tab.apply_theme(theme)
        if hasattr(self, 'register_tab') and self.register_tab and self.register_tab.frame.winfo_exists():
            self.register_tab.apply_theme(theme)
        if hasattr(self, 'settings_tab') and self.settings_tab and self.settings_tab.frame.winfo_exists():
            self.settings_tab.apply_theme(theme)

        style = ttk.Style(self.parent)
        style.theme_use("clam")

        # Update styles for frames and labels
        style.configure("Custom.TFrame", background=theme["bg"])
        style.configure("Custom.TLabel", background=theme["bg"], foreground=theme["fg"])
        style.configure("Custom.TButton", background=theme["button_bg"], foreground=theme["button_fg"])
        style.map("Custom.TButton",
                  background=[("active", theme["button_bg"]), ("!active", theme["button_bg"])],
                  foreground=[("active", theme["button_fg"]), ("!active", theme["button_fg"])])
        style.configure("Custom.TEntry", fieldbackground=theme["entry_bg"], foreground=theme["fg"])
        style.configure("Custom.TRadiobutton", background=theme["bg"], foreground=theme["fg"])
        style.configure("Custom.Treeview", background=theme["bg"], fieldbackground=theme["bg"], foreground=theme["fg"])
        style.configure("Custom.Treeview.Heading", background=theme["bg"], foreground=theme["fg"])

        # Apply the theme to the main window and all widgets
        self.parent.configure(bg=theme["bg"])
        self.frame.configure(style="Custom.TFrame")
        self.lbl_greeting.configure(style="Custom.TLabel")

        # Update Add Expense panel widgets
        self.lbl_amount.configure(style="Custom.TLabel")
        self.lbl_name.configure(style="Custom.TLabel")
        self.lbl_desc.configure(style="Custom.TLabel")
        self.lbl_date.configure(style="Custom.TLabel")
        self.entry_amount.configure(style="Custom.TEntry")
        self.entry_name.configure(style="Custom.TEntry")
        self.entry_desc.configure(style="Custom.TEntry")
        self.entry_date.configure(style="Custom.TEntry")
        self.rb_today.configure(style="Custom.TRadiobutton")
        self.rb_other.configure(style="Custom.TRadiobutton")
        self.btn_add_expense.configure(style="Custom.TButton")

        # Update the Treeview and Logout button styles
        self.tree.configure(style="Custom.Treeview")
        self.btn_logout.configure(style="Custom.TButton")

