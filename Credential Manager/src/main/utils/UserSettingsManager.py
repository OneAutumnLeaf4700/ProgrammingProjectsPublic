from utils.LibraryManager import sqlite3, ctk
from utils.DirectoryManager import userSettingsDbPath
from interface.Database import createUserSettingsDb, createMasterPasswordDb, createAllItemsDb, createFavouritesDb

# Global variables for styles and settings
userSettings = {}
programTheme = None
widgetTheme = None
textSize = None
textColor = None
fontName = None

# Font variables (initialized later)
textType = None
subtitleType = None 
titleType = None

# Numerical Assignments
subtitleSize = None
titleSize = None
buttonBorderWidth = 2

# Style variables
txtEntryFgColor = "black"
buttonFgColor = "#0f0f0f"
buttonBorderColor = "black"
frameBgColor = "transparent"
windowBgColor = "transparent"
titleFgColor = "transparent"

# Setup user settings
def setupUserSettings():
    # Create the databases
    createUserSettingsDb()
    createMasterPasswordDb()
    createAllItemsDb()
    createFavouritesDb()
    
    # Load user settings
    loadUserSettings()

    # Apply settings
    applySettings()

    # Initialize fonts
    initializeFonts()
    
# Load user settings from the database
def loadUserSettings():
    global userSettings, programTheme, widgetTheme, textSize, textColor, fontName
    
    with sqlite3.connect(userSettingsDbPath) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM settings WHERE id = 1;")
        row = cursor.fetchone()
        if row:
            userSettings = {
                "theme": row[1],
                "widgetTheme": row[2],
                "textSize": row[3],
                "textColor": row[4],
                "fontFamily": row[5]
            }
        else:
            userSettings = {
                "theme": "system",
                "widgetTheme": "dark-blue",
                "textSize": 16,
                "textColor": "White",
                "fontFamily": "Arial"
            }

    programTheme = userSettings["theme"]
    widgetTheme = userSettings["widgetTheme"]
    textSize = userSettings["textSize"]
    textColor = userSettings["textColor"]
    fontName = userSettings["fontFamily"]

    # Numerical Assignments
    global subtitleSize, titleSize
    subtitleSize = textSize + 2
    titleSize = textSize + 4

# Initialize fonts
def initializeFonts():
    global textType, subtitleType, titleType
    textType = ctk.CTkFont(family=fontName, size=textSize)
    subtitleType = ctk.CTkFont(family=fontName, size=subtitleSize)
    titleType = ctk.CTkFont(family=fontName, size=titleSize)

# Apply settings
def applySettings():
    ctk.set_appearance_mode(programTheme)
    ctk.set_default_color_theme(widgetTheme)

# Define styles
def getStyles():
    entry_style = {
        "font": textType,
        "text_color": textColor,
        "fg_color": txtEntryFgColor
    }

    label_style = {
        "font": subtitleType,
        "text_color": textColor
    }

    button_style = {
        "font": subtitleType,
        "fg_color": buttonFgColor,
        "border_width": buttonBorderWidth,
        "border_color": buttonBorderColor,
        "text_color": textColor
    }

    return entry_style, label_style, button_style
