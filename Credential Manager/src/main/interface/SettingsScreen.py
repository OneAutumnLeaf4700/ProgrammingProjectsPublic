from interface.CredentialManager import CredentialManager
from utils.LibraryManager import *
from utils.DirectoryManager import *
from utils.UserSettingsManager import *


class SettingsScreen(CredentialManager):
    _instance = None # Class variable to store the single instance

    def __new__(cls):
        # If an instance of the class already exists, return it
        if cls._instance is not None:
            cls.popup(cls._instance.root, "Settings window is already open")
            return cls._instance
        # If no instance exists, create a new one
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'root'): # Check if root attribute already exists
            return # Return without reinitializing if already initialized
        self.root = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Settings")
        root_width = 700
        root_height = 350
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        button_style = {"font": text_type, "fg_color": button_fg_color, "border_width": button_border_width, "border_color": button_border_color, "text_color": text_color}
        radio_button_style = {"fg_color": button_fg_color}
        label_style = {"font": title_type, "text_color": text_color, "fg_color": title_fg_color}
        # Theme Widgets
        theme_label = ctk.CTkLabel(self.root, text="Theme:", **label_style)
        theme_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.theme_var = StringVar()
        self.theme_var.set(user_settings["theme"])
        theme_button = ctk.CTkRadioButton(self.root, text="Automatic", variable=self.theme_var, value="system", command=None, **radio_button_style)
        theme_button.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        theme_button = ctk.CTkRadioButton(self.root, text="Light", variable=self.theme_var, value="light", command=None, **radio_button_style)
        theme_button.grid(row=0, column=2, padx=20, pady=10, sticky="w")
        theme_button = ctk.CTkRadioButton(self.root, text="Dark", variable=self.theme_var, value="dark", command=None, **radio_button_style)
        theme_button.grid(row=0, column=3, padx=20, pady=10, sticky="w")
        # Widget Theme Options
        widget_theme_label = ctk.CTkLabel(self.root, text="Widget Theme:", **label_style)
        widget_theme_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.widget_theme_var = StringVar()
        self.widget_theme_var.set(user_settings["widget_theme"])
        widget_theme_button = ctk.CTkRadioButton(self.root, text="Blue", variable=self.widget_theme_var, value="blue", command=None, **radio_button_style)
        widget_theme_button.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        widget_theme_button = ctk.CTkRadioButton(self.root, text="Dark Blue", variable=self.widget_theme_var, value="dark-blue", command=None, **radio_button_style)
        widget_theme_button.grid(row=1, column=2, padx=20, pady=10, sticky="w")
        widget_theme_button = ctk.CTkRadioButton(self.root, text="Green", variable=self.widget_theme_var, value="green", command=None, **radio_button_style)
        widget_theme_button.grid(row=1, column=3, padx=20, pady=10, sticky="w")
        # Text Size Option
        text_size_label = ctk.CTkLabel(self.root, text="Text Size:", **label_style)
        text_size_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.text_size_var = IntVar()
        self.text_size_var.set(user_settings["text_size"])
        text_size_btn = ctk.CTkRadioButton(self.root, text="Small", variable=self.text_size_var, value=14, command=None, **radio_button_style)
        text_size_btn.grid(row=2, column=1, columnspan=2, padx=20, pady=10, sticky="w")
        text_size_btn = ctk.CTkRadioButton(self.root, text="Medium", variable=self.text_size_var, value=16, command=None, **radio_button_style)
        text_size_btn.grid(row=2, column=2, columnspan=2, padx=20, pady=10, sticky="w")
        text_size_btn = ctk.CTkRadioButton(self.root, text="Large", variable=self.text_size_var, value=18, command=None, **radio_button_style)
        text_size_btn.grid(row=2, column=3, columnspan=2, padx=20, pady=10, sticky="w")
        # Text Color Option
        text_color_label = ctk.CTkLabel(self.root, text="Text Color:", **label_style)
        text_color_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.text_color_var = StringVar()
        self.text_color_var.set(user_settings["text_color"])
        text_color_options = ctk.CTkOptionMenu(self.root, values=["White", "Black", "Grey"], command=None, variable=self.text_color_var, fg_color=button_fg_color)
        text_color_options.grid(row=3, column=1, columnspan=2, padx=20, pady=10, sticky="w")
        # Font Family Option
        font_family_label = ctk.CTkLabel(self.root, text="Font Family:", **label_style)
        font_family_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.font_family_var = StringVar()
        self.font_family_var.set(user_settings["font_family"])
        font_family_options = ctk.CTkOptionMenu(self.root, values=["Arial", "IMPACT", "Times New Roman"], command=None, variable=self.font_family_var, fg_color=button_fg_color)
        font_family_options.grid(row=4, column=1, columnspan=2, padx=20, pady=10, sticky="w")
        # Apply Button
        apply_button = ctk.CTkButton(self.root, text="Apply Settings", command=self.apply_settings, **button_style)
        apply_button.grid(row=5, column=1, columnspan=2, padx=20, pady=10)

    def apply_settings(self):
        # Getting Theme
        self.current_theme = self.theme_var.get()
        # Getting Widget theme
        self.current_widget_theme = self.widget_theme_var.get()
        # Getting the text size
        self.current_text_size = self.text_size_var.get()
        # Getting the text color
        self.current_text_color = self.text_color_var.get()
        # Getting the font type
        self.current_font_family = self.font_family_var.get()
        # Connecting to the UserSettings Database
        with sqlite3.connect(userSettingsDbPath) as db:
            cursor = db.cursor()
            # Update the settings in the database
            self.update_database(cursor, db)
            # Fetch and print the updated values
            cursor.execute("SELECT * FROM settings WHERE id = 1;")
            updated_values = cursor.fetchone()
            # Update the user_settings dictionary
            self.update_user_settings(updated_values)
            self.refresh_ui()
            self.on_close()

    def refresh_ui(self):
        # Set New Appearance Mode
        ctk.set_appearance_mode(user_settings["theme"])
        ctk.set_default_color_theme(user_settings["widget_theme"])
        text_type.configure(family=user_settings["font_family"], size=user_settings["text_size"])
        subtitle_type.configure(family=user_settings["font_family"], size=user_settings["text_size"] + 2)
        title_type.configure(family=user_settings["font_family"], size=user_settings["text_size"] + 4)
        self.update_text_color()

    def update_database(self, cursor, db):
        # Update values in the settings table
        cursor.execute("""
            UPDATE settings
            SET
                theme = ?,
                widget_theme = ?,
                text_size = ?,
                text_color = ?,
                font_family = ?
            WHERE id = 1;
        """, (self.current_theme, self.current_widget_theme, self.current_text_size, self.current_text_color, self.current_font_family))
        db.commit()

    def update_user_settings(self, values):
        # Update the user_settings dictionary
        user_settings["theme"] = values[1]
        user_settings["widget_theme"] = values[2]
        user_settings["text_size"] = values[3]
        user_settings["text_color"] = values[4]
        user_settings["font_family"] = values[5]

    def update_text_color(self):
        global text_color
        text_color = user_settings["text_color"]

    def on_close(self):
        # Reset the _instance attribute
        SettingsScreen._instance = None
        # Destroy the current instance
        self.root.after(50, self.root.destroy())

    def run(self):
        self.root.mainloop()
        # Getting the font type
        self.current_font_family = self.font_family_var.get()
        # Connecting to the UserSettings Database
        with sqlite3.connect(userSettingsDbPath) as db:
            cursor = db.cursor()
            # Update the settings in the database
            self.update_database(cursor, db)
            # Fetch and print the updated values
            cursor.execute("SELECT * FROM settings WHERE id = 1;")
            updated_values = cursor.fetchone()
            # Update the user_settings dictionary
            self.update_user_settings(updated_values)
            self.refresh_ui()
            self.on_close()

    def refresh_ui(self):
        # Set New Appearance Mode
        ctk.set_appearance_mode(user_settings["theme"])
        ctk.set_default_color_theme(user_settings["widget_theme"])
        text_type.configure(family=user_settings["font_family"], size=user_settings["text_size"])
        subtitle_type.configure(family=user_settings["font_family"], size=user_settings["text_size"] + 2)
        title_type.configure(family=user_settings["font_family"], size=user_settings["text_size"] + 4)
        self.update_text_color()

    def update_database(self, cursor, db):
        # Update values in the settings table
        cursor.execute("""
            UPDATE settings
            SET
                theme = ?,
                widget_theme = ?,
                text_size = ?,
                text_color = ?,
                font_family = ?
            WHERE id = 1;
        """, (self.current_theme, self.current_widget_theme, self.current_text_size, self.current_text_color, self.current_font_family))
        db.commit()

    def update_user_settings(self, values):
        # Update the user_settings dictionary
        user_settings["theme"] = values[1]
        user_settings["widget_theme"] = values[2]
        user_settings["text_size"] = values[3]
        user_settings["text_color"] = values[4]
        user_settings["font_family"] = values[5]

    def update_text_color(self):
        global text_color
        text_color = user_settings["text_color"]

    def on_close(self):
        from interface.MainVault import MainVault
        
        # Reset the _instance attribute
        SettingsScreen._instance = None
        # Destroy the current instance
        self.root.after(50, self.root.destroy())

        app = MainVault(root, "All Items", "AllItems", "AllItems")
        app.run()

    def run(self):
        self.root.mainloop()