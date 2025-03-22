import tkinter as tk
from tkinter import ttk


class SettingsTab:
    def __init__(self, parent, theme_callback):
        self.theme_callback = theme_callback  # Callback for when theme changes.
        self.frame = ttk.Frame(parent)

        # Center container within this tab.
        self.container = ttk.Frame(self.frame)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Variable to hold the selected theme.
        self.selected_theme = tk.StringVar(value="light")

        self.lbl_theme = ttk.Label(self.container, text="Select Theme:")
        self.radio_light = ttk.Radiobutton(
            self.container,
            text="Light Mode",
            variable=self.selected_theme,
            value="light",
            command=self.change_theme
        )
        self.radio_dark = ttk.Radiobutton(
            self.container,
            text="Dark Mode",
            variable=self.selected_theme,
            value="dark",
            command=self.change_theme
        )

        # Arrange using grid.
        self.lbl_theme.grid(row=0, column=0, columnspan=2, pady=5)
        self.radio_light.grid(row=1, column=0, padx=5, pady=5)
        self.radio_dark.grid(row=1, column=1, padx=5, pady=5)

    def change_theme(self):
        """Invoke callback with the selected theme."""
        theme = self.selected_theme.get()
        if self.theme_callback:
            self.theme_callback(theme)

    def apply_theme(self, theme):
        style = ttk.Style()

        # Set custom style for settings tab elements.
        style.configure("Custom.TFrame", background=theme["bg"])
        style.configure("Custom.TLabel", background=theme["bg"], foreground=theme["fg"])
        style.configure("Custom.TRadiobutton", background=theme["bg"], foreground=theme["fg"])

        self.frame.configure(style="Custom.TFrame")
        self.container.configure(style="Custom.TFrame")
        self.lbl_theme.configure(style="Custom.TLabel")
        self.radio_light.configure(style="Custom.TRadiobutton")
        self.radio_dark.configure(style="Custom.TRadiobutton")
