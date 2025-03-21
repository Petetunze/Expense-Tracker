# styling.py

# Light Mode Palette
LIGHT_THEME = {
    "background": "#ffffff",  # White
    "foreground": "#000000",  # Black
    "button_bg": "#e0e0e0",   # Light gray
    "button_fg": "#000000",
    "tree_bg": "#f5f5f5",
    "tree_fg": "#000000"
}

# Dark Mode Palette
DARK_THEME = {
    "background": "#1e1e1e",  # Dark gray
    "foreground": "#ffffff",  # White
    "button_bg": "#333333",   # Darker gray
    "button_fg": "#ffffff",
    "tree_bg": "#2d2d2d",
    "tree_fg": "#ffffff"
}

# A function to easily switch themes
def get_theme(mode):
    return LIGHT_THEME if mode == "light" else DARK_THEME
