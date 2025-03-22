import tkinter as tk
from tkinter import ttk, messagebox
from database import add_user


class RegisterTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        # Center the container.
        self.container = ttk.Frame(self.frame)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Registration UI elements (email removed).
        self.lbl_username = ttk.Label(self.container, text="Username:")
        self.entry_username = ttk.Entry(self.container)
        self.lbl_password = ttk.Label(self.container, text="Password:")
        self.entry_password = ttk.Entry(self.container, show="*")
        self.btn_register = ttk.Button(self.container, text="Register", command=self.do_register)

        # Arrange widgets in a grid.
        self.lbl_username.grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)
        self.lbl_password.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)
        self.btn_register.grid(row=2, column=0, columnspan=2, pady=10)

    def do_register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showerror("Registration Error", "Please fill out all fields.")
            return

        # Pass an empty string for email since we're not using it.
        success = add_user(username, "", password)
        if success:
            messagebox.showinfo("Registration Success", "User registered successfully. Please login now.")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("Registration Failed", "Username already exists. Please choose another.")

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
        self.btn_register.configure(style="Custom.TButton")
