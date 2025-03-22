import tkinter as tk
from tkinter import ttk
import config
from gui.login_tab import LoginTab
from gui.register_tab import RegisterTab
from gui.settings_tab import SettingsTab
import database

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("600x400")
        self.configure(highlightbackground=config.THEMES[config.CURRENT_THEME]["bg"],
                       highlightcolor=config.THEMES[config.CURRENT_THEME]["bg"], bd=0)

        # Use a theme that respects our custom style changes.
        style = ttk.Style(self)
        style.theme_use("clam")

        self.notebook = ttk.Notebook(self, style="TNotebook")
        self.notebook.pack(expand=True, fill="both")

        self.login_tab = LoginTab(self.notebook)
        self.register_tab = RegisterTab(self.notebook)
        self.settings_tab = SettingsTab(self.notebook, self.update_theme)

        self.notebook.add(self.login_tab.frame, text="Login")
        self.notebook.add(self.register_tab.frame, text="Register")
        self.notebook.add(self.settings_tab.frame, text="Settings")

        self.apply_theme(config.THEMES[config.CURRENT_THEME])

    def update_theme(self, theme_name):
        """Callback used by the Settings tab to update the current theme."""
        config.CURRENT_THEME = theme_name
        self.apply_theme(config.THEMES[theme_name])


    def apply_theme(self, theme):
        self.configure(bg=theme["bg"],
                       highlightbackground=theme["bg"],
                       highlightcolor=theme["bg"])
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=theme["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=theme["bg"], foreground=theme["fg"], padding=[10, 5])
        style.map("TNotebook.Tab",
                  background=[("selected", theme["button_bg"])],
                  foreground=[("selected", theme["button_fg"])])
        style.configure("TFrame", background=theme["bg"])

        self.login_tab.apply_theme(theme)
        self.register_tab.apply_theme(theme)
        self.settings_tab.apply_theme(theme)

if __name__ == "__main__":
    database.create_tables()
    app = App()
    app.mainloop()
