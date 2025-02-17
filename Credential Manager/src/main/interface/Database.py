from utils.LibraryManager import sqlite3
from utils.DirectoryManager import masterpasswordsDbPath, allItemsDbPath, favouritesDbPath, userSettingsDbPath



def create_masterpassword_db():
    with sqlite3.connect(masterpasswordsDbPath) as db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS masterpassword (
            id INTEGER PRIMARY KEY,
            password TEXT NOT NULL
        );
        """)

def create_allitems_db():
    with sqlite3.connect(allItemsDbPath) as db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS AllItems (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """)

def create_favourites_db():
    with sqlite3.connect(favouritesDbPath) as db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Favourites (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """)

def create_usersettings_db():
    with sqlite3.connect(userSettingsDbPath) as db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            theme TEXT NOT NULL,
            widget_theme TEXT NOT NULL,
            text_size INTEGER NOT NULL,
            text_color TEXT NOT NULL,
            font_family TEXT NOT NULL
        );
        """)

        # Inserting default values
        cursor.execute("""
        INSERT INTO settings (theme, widget_theme, text_size, text_color, font_family)
        VALUES ('system', 'dark-blue', 14, 'White', 'Arial');
        """)
