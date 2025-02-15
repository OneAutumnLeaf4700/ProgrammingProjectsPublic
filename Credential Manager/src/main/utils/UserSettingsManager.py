from utils.LibraryManager import sqlite3, ctk
from utils.DirectoryManager import userSettingsDbPath

# Global variables for styles and settings
user_settings = {}
program_theme = None
widget_theme = None
text_size = None
text_color = None
font_name = None

# Font variables (initialized later)
text_type = None
subtitle_type = None
title_type = None

# Numerical Assignments
subtitle_size = None
title_size = None
button_border_width = 2

# Style variables
txt_entry_fg_color = "black"
button_fg_color = "#0f0f0f"
button_border_color = "black"
frame_bg_color = "transparent"
window_bg_color = "transparent"
title_fg_color = "transparent"


def setup_user_settings():
    # Load user settings
    load_user_settings()

    # Apply settings
    apply_settings()

    # Initialize fonts
    initialize_fonts()



# Load user settings from the database
def load_user_settings():
    global user_settings, program_theme, widget_theme, text_size, text_color, font_name
    
    with sqlite3.connect(userSettingsDbPath) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM settings WHERE id = 1;")
        row = cursor.fetchone()
        if row:
            user_settings = {
                "theme": row[1],
                "widget_theme": row[2],
                "text_size": row[3],
                "text_color": row[4],
                "font_family": row[5]
            }
        else:
            user_settings = {
                "theme": "system",
                "widget_theme": "dark-blue",
                "text_size": 16,
                "text_color": "White",
                "font_family": "Arial"
            }

    program_theme = user_settings["theme"]
    widget_theme = user_settings["widget_theme"]
    text_size = user_settings["text_size"]
    text_color = user_settings["text_color"]
    font_name = user_settings["font_family"]

    # Numerical Assignments
    global subtitle_size, title_size
    subtitle_size = text_size + 2
    title_size = text_size + 4

# Initialize fonts
def initialize_fonts():
    global text_type, subtitle_type, title_type
    text_type = ctk.CTkFont(family=font_name, size=text_size)
    subtitle_type = ctk.CTkFont(family=font_name, size=subtitle_size)
    title_type = ctk.CTkFont(family=font_name, size=title_size)

# Apply settings
def apply_settings():
    ctk.set_appearance_mode(program_theme)
    ctk.set_default_color_theme(widget_theme)

# Define styles
def get_styles():
    entry_style = {
        "font": text_type,
        "text_color": text_color,
        "fg_color": txt_entry_fg_color
    }

    label_style = {
        "font": subtitle_type,
        "text_color": text_color
    }

    button_style = {
        "font": subtitle_type,
        "fg_color": button_fg_color,
        "border_width": button_border_width,
        "border_color": button_border_color,
        "text_color": text_color
    }

    return entry_style, label_style, button_style
