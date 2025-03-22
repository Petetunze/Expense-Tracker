import tkinter as tk
from tkinter import ttk, messagebox
from database import verify_user
from gui.dashboard import Dashboard


class LoginTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.container = ttk.Frame(self.frame)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_username = ttk.Label(self.container, text="Username:")
        self.entry_username = ttk.Entry(self.container)
        self.lbl_password = ttk.Label(self.container, text="Password:")
        self.entry_password = ttk.Entry(self.container, show="*")
        self.btn_login = ttk.Button(self.container, text="Login", command=self.do_login)

        self.lbl_username.grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)
        self.lbl_password.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    def do_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        success, user_id = verify_user(username, password)
        if success:
            top = self.frame.winfo_toplevel()
            for widget in top.winfo_children():
                widget.destroy()
            Dashboard(top, username, user_id)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def apply_theme(self, theme):
        style = ttk.Style()
        style.configure("Custom.TFrame", background=theme["bg"])
        style.configure("Custom.TLabel", background=theme["bg"], foreground=theme["fg"])
        style.configure("Custom.TEntry", fieldbackground=theme["entry_bg"], foreground=theme["fg"])
        style.configure("Custom.TButton",
                        background=theme["button_bg"],
                        foreground=theme["button_fg"])
        style.map("Custom.TButton",
                  background=[('active', theme["button_bg"])],
                  foreground=[('active', theme["button_fg"])])

        self.frame.configure(style="Custom.TFrame")
        self.container.configure(style="Custom.TFrame")
        self.lbl_username.configure(style="Custom.TLabel")
        self.lbl_password.configure(style="Custom.TLabel")
        self.entry_username.configure(style="Custom.TEntry")
        self.entry_password.configure(style="Custom.TEntry")
        self.btn_login.configure(style="Custom.TButton")
