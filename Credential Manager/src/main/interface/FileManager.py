from interface.CredentialManager import CredentialManager
from utils.LibraryManager import *
from utils.DirectoryManager import *
from utils.UserSettingsManager import *


class FileManager(CredentialManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            cls.popup(cls._instance.root, "File Manager is already open")
            return cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'root'):
            return
        super().__init__(root)
        self.root = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Import/Export Data")
        root_width = 350
        root_height = 300
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        button_style = {"font": subtitle_type, "fg_color": button_fg_color, "border_width": button_border_width, "border_color": button_border_color, "text_color": text_color}
        label_style = {"font": title_type, "text_color": text_color, "fg_color": title_fg_color}
        # Heading label
        heading_label = ctk.CTkLabel(self.root, text="Import/Export Data", **label_style)
        heading_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        # Database section
        database_label = ctk.CTkLabel(self.root, text="Database:", **label_style)
        database_label.grid(row=1, column=0, padx=10, pady=5, columnspan=2)
        self.database_var = StringVar(value="AllItems")
        Main_database_button = ctk.CTkRadioButton(self.root, text="All Items", variable=self.database_var, value="AllItems", command=None, fg_color=button_fg_color)
        Main_database_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        Favourites_database_button = ctk.CTkRadioButton(self.root, text="Favourites", variable=self.database_var, value="Favourites", command=None, fg_color=button_fg_color)
        Favourites_database_button.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        # Import section
        import_label = ctk.CTkLabel(self.root, text="Import Data", **label_style)
        import_label.grid(row=3, column=0, padx=10, pady=5, columnspan=2)
        import_json_button = ctk.CTkButton(self.root, text="Import from JSON", command=self.import_from_json, **button_style)
        import_json_button.grid(row=4, column=0, padx=10, pady=5)
        import_csv_button = ctk.CTkButton(self.root, text="Import from CSV", command=self.import_from_csv, **button_style)
        import_csv_button.grid(row=4, column=1, padx=10, pady=5)
        # Export section
        export_label = ctk.CTkLabel(self.root, text="Export Data", **label_style)
        export_label.grid(row=5, column=0, padx=10, pady=5, columnspan=2)
        export_json_button = ctk.CTkButton(self.root, text="Export to JSON", command=self.export_as_json, **button_style)
        export_json_button.grid(row=6, column=0, padx=10, pady=5)
        export_csv_button = ctk.CTkButton(self.root, text="Export to CSV", command=self.export_as_csv, **button_style)
        export_csv_button.grid(row=6, column=1, padx=10, pady=5)

    def determine_database(self):
        # Check which database radio button is selected
        selected_database = self.database_var.get()
        # Set the appropriate database and table names based on the selected radio button
        if selected_database == "AllItems":
            self.database = "AllItems"
            self.table = "AllItems"
        elif selected_database == "Favourites":
            self.database = "Favourites"
            self.table = "Favourites"
        else:
            self.popup(self.root, "Please select a database")

    def import_from_json(self):
        # Call determine_database to set database and table names
        self.determine_database()
        # Call the import_data_from_json method with database and table parameters
        self.import_data_from_json(self.database, self.table)

    def import_from_csv(self):
        # Call determine_database to set database and table names
        self.determine_database()
        # Call the import_data_from_csv method with database and table parameters
        self.import_data_from_csv(self.database, self.table)

    def export_as_json(self):
        # Call determine_database to set database and table names
        self.determine_database()
        # Call the export_data_to_json method with database and table parameters
        self.export_data_as_json(self.database, self.table)

    def export_as_csv(self):
        # Call determine_database to set database and table names
        self.determine_database()
        # Call the export_data_to_csv method with database and table parameters
        self.export_data_as_csv(self.database, self.table)

    def import_data_from_json(self, database, table):
        try:
            # Open file dialog to select JSON file
            json_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if not json_file:
                self.popup(self.root, "No file selected.")
                return
            # Read data from selected JSON file
            with open(json_file, 'r') as file:
                data = json.load(file)
            # Connect to the SQLite database
            with sqlite3.connect(f"{db_path}/{database}.db") as db:
                cursor = db.cursor()
                # Insert each record into the specified table
                for record in data:
                    website = record.get('website', '')
                    username = record.get('username', '')
                    password = record.get('password', '')
                    # Execute SQL INSERT statement using f-string
                    cursor.execute(f"INSERT INTO {table} (website, username, password) VALUES (?, ?, ?)", (website, username, password))
                db.commit()
            self.popup(self.root, "Data imported successfully.")
        except FileNotFoundError:
            self.popup(self.root, f"File '{json_file}' not found.")
        except json.JSONDecodeError:
            self.popup(self.root, "Invalid JSON file.")
        except sqlite3.Error as e:
            self.popup(self.root, f"SQLite error: {e}")

    def import_data_from_csv(self, database, table):
        try:
            # Open file dialog to select CSV file
            csv_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not csv_file:
                self.popup(self.root, "No file selected.")
                return
            # Read data from selected CSV file
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                data = [row for row in csv_reader]
            # Connect to the SQLite database
            with sqlite3.connect(f"{db_path}/{database}.db") as db:
                cursor = db.cursor()
                # Insert each record into the specified table
                for record in data:
                    website = record.get('website', '')
                    username = record.get('username', '')
                    password = record.get('password', '')
                    # Execute SQL INSERT statement using f-string
                    cursor.execute(f"INSERT INTO {table} (website, username, password) VALUES (?, ?, ?)", (website, username, password))
                db.commit()
            self.popup(self.root, "Data imported successfully.")
        except FileNotFoundError:
            self.popup(self.root, f"File '{csv_file}' not found.")
        except csv.Error as e:
            self.popup(self.root, f"CSV error: {e}")
        except sqlite3.Error as e:
            self.popup(self.root, f"SQLite error: {e}")

    def export_data_as_json(self, database, table):
        try:
            # Connect to the SQLite database
            with sqlite3.connect(f"{db_path}/{database}.db") as db:
                cursor = db.cursor()
                # Fetch all records from the specified table
                cursor.execute(f"SELECT * FROM {table}")
                records = cursor.fetchall()
                # Convert records to a list of dictionaries
                data = []
                for record in records:
                    data.append({
                        'website': record[1],
                        'username': record[2],
                        'password': str((record[3])),
                    })
                # Open file dialog to select export location
                json_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
                if not json_file:
                    self.popup(self.root, "No file selected.")
                    return
                # Write data to the selected JSON file
                with open(json_file, 'w') as file:
                    json.dump(data, file, indent=4)
                self.popup(self.root, "Data exported successfully.")
        except sqlite3.Error as e:
            self.popup(self.root, f"SQLite error: {e}")

    def export_data_as_csv(self, database, table):
        try:
            # Connect to the SQLite database
            with sqlite3.connect(f"{db_path}/{database}.db") as db:
                cursor = db.cursor()
                # Fetch all records from the specified table
                cursor.execute(f"SELECT * FROM {table}")
                records = cursor.fetchall()
                # Open file dialog to select export location
                csv_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if not csv_file:
                    self.popup(self.root, "No file selected.")
                    return
                # Write data to the selected CSV file
                with open(csv_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Website', 'Username', 'Password']) # Write header
                    for record in records:
                        writer.writerow([record[1], record[2], str(record[3])]) # Write each record
                self.popup(self.root, "Data exported successfully.")
        except sqlite3.Error as e:
            self.popup(self.root, f"SQLite error: {e}")

    def on_close(self):
        # Reset the _instance attribute
        FileManager._instance = None
        # Destroy the current instance
        self.root.destroy()

    def is_master_password_present(self):
        pass

    def run(self):
        self.root.mainloop()
        

    def on_close(self):
        # Reset the _instance attribute
        FileManager._instance = None
        # Destroy the current instance
        self.root.destroy()

    def is_master_password_present(self):
        pass

    def run(self):
        self.root.mainloop()



