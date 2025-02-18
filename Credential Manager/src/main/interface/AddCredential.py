from interface.CredentialManager import CredentialManager
from utils.LibraryManager import *
from utils.DirectoryManager import *
from utils.UserSettingsManager import *


class AddCredential(CredentialManager):
    _instance = None

    def __new__(cls, database, table, credential_array):
        if cls._instance is not None:
            cls.popup(cls._instance.root, "Add Credential window is already open")
            return cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database, table, credential_array):
        if hasattr(self, 'root'):
            return
        super().__init__(root)
        self.root = ctk.CTk()
        self.database = database
        self.table = table
        self.credentialArray = credential_array
        self.setup_window()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Add A Credential")
        self.root.attributes('-topmost', True)
        root_width = 600
        root_height = 600
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        heading1 = ctk.CTkLabel(self.root, text="Website:", **label_style)
        heading1.pack(pady=(20, 10))
        self.website_entry = ctk.CTkEntry(self.root, width=300, **entry_style)
        self.website_entry.pack(pady=(0, 10))
        heading2 = ctk.CTkLabel(self.root, text="Username:", **label_style)
        heading2.pack(pady=(20, 10))
        self.username_entry = ctk.CTkEntry(self.root, width=300, **entry_style)
        self.username_entry.pack(pady=(0, 10))
        heading3 = ctk.CTkLabel(self.root, text="Password:", **label_style)
        heading3.pack(pady=(20, 10))
        self.password_entry = ctk.CTkEntry(self.root, width=300, show="*", **entry_style)
        self.password_entry.pack(pady=(0, 10))
        heading4 = ctk.CTkLabel(self.root, text="Confirm Password:", **label_style)
        heading4.pack(pady=(20, 10))
        self.confirm_password_entry = ctk.CTkEntry(self.root, width=300, show="*", **entry_style)
        self.confirm_password_entry.pack(pady=(0, 10))
        add_button = ctk.CTkButton(self.root, text="Add", width=200, command=self.add_values, **button_style)
        add_button.pack(pady=(20, 10))

    def is_master_password_present(self):
        pass # do nothing

    def add_values(self):
        # Get the values from the text entries
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        # Check if any of the fields are empty
        if not website or not username or not password or not confirm_password:
            # If any field is empty, show a message to the user
            self.popup(self.root, "Please fill in all the fields")
            # Clear the text entries
            self.website_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
        elif password != confirm_password:
            # If passwords don't match, show an error message
            self.popup(self.root, "Passwords do not match")
            # Clear the password fields
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
        else:
            try:
                # Check if the credential already exists
                for credential in self.credentialArray:
                    if credential[1] == website and credential[2] == username:
                        self.popup(self.root, "Credential already exists")
                        return # Exit the function if credential already exists
                # If all entries are filled, passwords match, and credential doesn't exist, proceed to encrypt the password
                encrypted_password = self.encrypt_password(password)
                # Insert the encrypted password into the database
                insert_values = f"""INSERT INTO {self.table}(website, username, password) VALUES (?, ?, ?) """
                with sqlite3.connect(f"F:/Programming Projects/Projects/Resume Projects/Credential Manager/{self.database}.db") as db:
                    cursor = db.cursor()
                    cursor.execute(insert_values, (website, username, encrypted_password))
                    db.commit()
                # Destroy the current window after a short delay and create a new instance of MainVault
                self.root.after(100, self.destroy_window_and_create_main_vault)
            except Exception as e:
                self.popup(self.root, f"An error occurred: {e}")

    def destroy_window_and_create_main_vault(self):
        self.popup(self.root, "Credential Added Successfully")
        AddCredential._instance = None
        self.root.destroy()

    def on_close(self):
        # Reset the _instance attribute of AddCredential
        AddCredential._instance = None
        # Destroy the current instance
        self.root.destroy()

    def run(self):
        self.root.mainloop()
