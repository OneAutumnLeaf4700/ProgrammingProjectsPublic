from interface.CredentialManager import CredentialManager
from utils.LibraryManager import ctk, sqlite3

class AdditionalInformation(CredentialManager):
    _instance = None  # Class variable to store the single instance

    def __new__(cls):
        # If an instance of the class already exists, return it
        if cls._instance is not None:
            cls.popup(cls._instance.root, "Additional Information is already open")
            return cls._instance
        # If no instance exists, create a new one
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'root'):  # Check if root attribute already exists
            return  # Return without reinitializing if already initialized
        # Initialize the instance only if it's a new instance
        self.root = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        # Register the function to handle window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Additional Information")
        self.root.attributes('-topmost', True)
        root_width = 900
        root_height = 500
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        # Create a frame to hold the information sections
        info_frame = ctk.CTkFrame(self.root, corner_radius=10)
        info_frame.pack(padx=20, pady=20, fill='both', expand=True)
        # Metadata section
        metadata_label = ctk.CTkLabel(info_frame, text="Metadata", font=('Roboto', 16, 'bold'))
        metadata_label.grid(row=0, column=0, pady=(10, 5), sticky="w")
        created_label = ctk.CTkLabel(info_frame, text="Created On: 01/01/2022", font=('Roboto', 12))
        created_label.grid(row=1, column=0, sticky="w", padx=20)
        modified_label = ctk.CTkLabel(info_frame, text="Last Modified: 01/02/2022", font=('Roboto', 12))
        modified_label.grid(row=2, column=0, sticky="w", padx=20)
        # Security section
        security_label = ctk.CTkLabel(info_frame, text="Security Notes", font=('Roboto', 16, 'bold'))
        security_label.grid(row=3, column=0, pady=(20, 5), sticky="w")
        note_label = ctk.CTkLabel(info_frame, text="Ensure the password is updated regularly.", font=('Roboto', 12))
        note_label.grid(row=4, column=0, sticky="w", padx=20)
        # Tags section
        tags_label = ctk.CTkLabel(info_frame, text="Tags / Categories", font=('Roboto', 16, 'bold'))
        tags_label.grid(row=5, column=0, pady=(20, 5), sticky="w")
        tags_value_label = ctk.CTkLabel(info_frame, text="Personal, Banking", font=('Roboto', 12))
        tags_value_label.grid(row=6, column=0, sticky="w", padx=20)
        # Audit Log section
        audit_label = ctk.CTkLabel(info_frame, text="Audit Log", font=('Roboto', 16, 'bold'))
        audit_label.grid(row=7, column=0, pady=(20, 5), sticky="w")
        log_label = ctk.CTkLabel(info_frame, text="Last Access: 01/03/2022 by user@example.com", font=('Roboto', 12))
        log_label.grid(row=8, column=0, sticky="w", padx=20)

    def on_close(self):
        AdditionalInformation._instance = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()

class EditCredential(CredentialManager):
    _instance = None

    def __new__(cls, database, table, record):
        if cls._instance is not None:
            cls.popup(cls._instance.root, "Edit Credential window is already open")
            return cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database, table, record):
        if hasattr(self, 'root'):
            return
        self.root = ctk.CTk()
        super().__init__(self.root)
        self.database = database
        self.table = table
        self.previous_website = record[1]
        self.previous_username = record[2]
        self.previous_password = record[3]
        self.setup_window()
        self.create_widgets()
        self.assign_values()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Edit A Credential")
        self.root.attributes('-topmost', True)
        root_width = 600
        root_height = 400
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        heading1 = ctk.CTkLabel(self.root, text="Website:", **self.label_style)
        heading1.pack(pady=(20, 10))
        self.website_entry = ctk.CTkEntry(self.root, width=300, **self.entry_style)
        self.website_entry.pack(pady=(0, 10))
        heading2 = ctk.CTkLabel(self.root, text="Username:", **self.label_style)
        heading2.pack(pady=(20, 10))
        self.username_entry = ctk.CTkEntry(self.root, width=300, **self.entry_style)
        self.username_entry.pack(pady=(0, 10))
        heading3 = ctk.CTkLabel(self.root, text="Password:", **self.label_style)
        heading3.pack(pady=(20, 10))
        self.password_entry = ctk.CTkEntry(self.root, width=300, **self.entry_style)
        self.password_entry.pack(pady=(0, 10))
        add_button = ctk.CTkButton(self.root, text="Apply", width=200, command=self.apply_values, **self.button_style)
        add_button.pack(pady=(20, 10))

    def is_master_password_present(self):
        pass

    def assign_values(self):
        # Get the website from the entry
        website = self.previous_website
        username = self.previous_username
        password = self.previous_password
        print(website, username, password, self.decrypt_password(password))
        # Connect to the database and retrieve the credential details
        with sqlite3.connect(f"F:/Programming Projects/Projects/Resume Projects/Credential Manager/{self.database}.db") as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {self.table} WHERE website = ? AND username = ? AND password = ?", (website, username, password))
            credential = cursor.fetchone()
            if credential:
                # Populate the text entries with the retrieved credential details
                self.website_entry.delete(0, 'end')
                self.website_entry.insert(0, credential[1])
                self.username_entry.delete(0, 'end')
                self.username_entry.insert(0, credential[2])
                # Decrypt the password and insert it into the password entry
                decrypted_password = self.decrypt_password(credential[3])  # Assuming password is the third column
                self.password_entry.delete(0, 'end')
                self.password_entry.insert(0, decrypted_password)
            else:
                # If credential not found, show an error message
                self.popup(self.root, f"No credential found for website: {website}")

    def apply_values(self):
        # Get the updated values from the text entries
        new_website = self.website_entry.get()
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()
        # Check if any of the fields are empty
        if not all((new_website, new_username, new_password)):
            # If any field is empty, show an error message and return
            self.popup(self.root, "Please fill in all fields.")
            return
        # Check if the values have actually changed
        if new_website != self.previous_website or new_username != self.previous_username or new_password != self.previous_password:
            # Check to see if the credential exists
            with sqlite3.connect(f"F:/Programming Projects/Projects/Resume Projects/Credential Manager/{self.database}.db") as db:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM {self.table} WHERE website = ? AND username = ?", (self.previous_website, self.previous_username))
                credential = cursor.fetchone()
                if credential:
                    # Update the database with the new values
                    update_query = f"UPDATE {self.table} SET website = ?, username = ?, password = ? WHERE website = ? AND username = ? AND password = ?"
                    encrypted_password = self.encrypt_password(new_password)
                    with sqlite3.connect(f"F:/Programming Projects/Projects/Resume Projects/Credential Manager/{self.database}.db") as db:
                        cursor = db.cursor()
                        cursor.execute(update_query, (new_website, new_username, encrypted_password, self.previous_website, self.previous_username, self.previous_password))
                        db.commit()
                    self.root.after(100, self.destroy_window_and_create_main_vault)
                else:
                    # If credential not found, show an error message
                    self.popup(self.root, f"No credential found for website: {self.previous_website} and username: {self.previous_username}")
        else:
            # No changes were made, so inform the user
            self.popup(self.root, "No changes made.")

    def destroy_window_and_create_main_vault(self):
        self.popup(self.root, "Change Successful")
        EditCredential._instance = None
        self.root.destroy()
        """EditCredential._instance = None
        if self.database == "AllItems":
            self.root.destroy()
            app = MainVault(root, "All Items", "AllItems", "AllItems")
        else:
            self.root.destroy()
            app = MainVault(root, "Favourites", "Favourites", "Favourites")
        app.run()"""

    def on_close(self):
        EditCredential._instance = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def apply_values(self):
        # Get the updated values from the text entries
        new_website = self.website_entry.get()
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()
        # Check if any of the fields are empty
        if not all((new_website, new_username, new_password)):
            # If any field is empty, show an error message and return
            self.popup(self.root, "Please fill in all fields.")
            return
        # Check if the values have actually changed
        if new_website != self.previous_website or new_username != self.previous_username or new_password != self.previous_password:
            # Check to see if the credential exists
            with sqlite3.connect(f"F:/Programming Projects/Projects/Resume Projects/Credential Manager/{self.database}.db") as db:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM {self.table} WHERE website = ? AND username = ?", (self.previous_website, self.previous_username))
                credential = cursor.fetchone()
                if credential:
                    # Update the database with the new values
                    update_query = f"UPDATE {self.table} SET website = ?, username = ?, password = ? WHERE website = ? AND username = ? AND password = ?"
                    encrypted_password = self.encrypt_password(new_password)
                    with sqlite3.connect(f"F:/Programming Projects/Projects/Resume Projects/Credential Manager/{self.database}.db") as db:
                        cursor = db.cursor()
                        cursor.execute(update_query, (new_website, new_username, encrypted_password, self.previous_website, self.previous_username, self.previous_password))
                        db.commit()
                    self.root.after(100, self.destroy_window_and_create_main_vault)
                else:
                    # If credential not found, show an error message
                    self.popup(self.root, f"No credential found for website: {self.previous_website} and username: {self.previous_username}")
        else:
            # No changes were made, so inform the user
            self.popup(self.root, "No changes made.")

    def destroy_window_and_create_main_vault(self):
        self.popup(self.root, "Change Successful")
        EditCredential._instance = None
        self.root.destroy()
        """EditCredential._instance = None
        if self.database == "AllItems":
        self.root.destroy()
        app = MainVault(root, "All Items", "AllItems", "AllItems")
        else:
        self.root.destroy()
        app = MainVault(root, "Favourites", "Favourites", "Favourites")
        app.run()"""

    def on_close(self):
        EditCredential._instance = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()

class AdditionalInformation(CredentialManager):
    _instance = None  # Class variable to store the single instance

    def __new__(cls):
        # If an instance of the class already exists, return it
        if cls._instance is not None:
            cls.popup(cls._instance.root, "Additional Information is already open")
            return cls._instance
        # If no instance exists, create a new one
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'root'):  # Check if root attribute already exists
            return  # Return without reinitializing if already initialized
        # Initialize the instance only if it's a new instance
        self.root = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        # Register the function to handle window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Additional Information")
        self.root.attributes('-topmost', True)
        root_width = 900
        root_height = 500
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        # Create a frame to hold the information sections
        info_frame = ctk.CTkFrame(self.root, corner_radius=10)
        info_frame.pack(padx=20, pady=20, fill='both', expand=True)
        # Metadata section
        metadata_label = ctk.CTkLabel(info_frame, text="Metadata", font=('Roboto', 16, 'bold'))
        metadata_label.grid(row=0, column=0, pady=(10, 5), sticky="w")
        created_label = ctk.CTkLabel(info_frame, text="Created On: 01/01/2022", font=('Roboto', 12))
        created_label.grid(row=1, column=0, sticky="w", padx=20)
        modified_label = ctk.CTkLabel(info_frame, text="Last Modified: 01/02/2022", font=('Roboto', 12))
        modified_label.grid(row=2, column=0, sticky="w", padx=20)
        # Security section
        security_label = ctk.CTkLabel(info_frame, text="Security Notes", font=('Roboto', 16, 'bold'))
        security_label.grid(row=3, column=0, pady=(20, 5), sticky="w")
        note_label = ctk.CTkLabel(info_frame, text="Ensure the password is updated regularly.", font=('Roboto', 12))
        note_label.grid(row=4, column=0, sticky="w", padx=20)
        # Tags section
        tags_label = ctk.CTkLabel(info_frame, text="Tags / Categories", font=('Roboto', 16, 'bold'))
        tags_label.grid(row=5, column=0, pady=(20, 5), sticky="w")
        tags_value_label = ctk.CTkLabel(info_frame, text="Personal, Banking", font=('Roboto', 12))
        tags_value_label.grid(row=6, column=0, sticky="w", padx=20)
        # Audit Log section
        audit_label = ctk.CTkLabel(info_frame, text="Audit Log", font=('Roboto', 16, 'bold'))
        audit_label.grid(row=7, column=0, pady=(20, 5), sticky="w")
        log_label = ctk.CTkLabel(info_frame, text="Last Access: 01/03/2022 by user@example.com", font=('Roboto', 12))
        log_label.grid(row=8, column=0, sticky="w", padx=20)

    def on_close(self):
        AdditionalInformation._instance = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()
