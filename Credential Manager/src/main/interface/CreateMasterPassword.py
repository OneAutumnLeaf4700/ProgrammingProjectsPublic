from interface.CredentialManager import CredentialManager
from utils.LibraryManager import ctk, sqlite3, re
from interface.MainVault import MainVault
from utils.Encryption import hash_text, encrypt_password
from utils.DirectoryManager import masterpasswordsDbPath

class CreateMasterPassword(CredentialManager):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setup_window()
        self.create_widgets()
        
        # Register the close icon as a valid method of termination
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Create Master Password")
        root_width = 600
        root_height = 300
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        heading1 = ctk.CTkLabel(self.root, text="Enter A Master Password", **self.label_style)
        heading1.pack(pady=(20, 10))
        self.password_entry = ctk.CTkEntry(self.root, width=200, **self.entry_style)
        self.password_entry.pack(pady=(0, 20))
        heading2 = ctk.CTkLabel(self.root, text="Re-Enter Master Password", **self.label_style)
        heading2.pack(pady=(20, 10))
        self.confirm_password_entry = ctk.CTkEntry(self.root, width=200, **self.entry_style)
        self.confirm_password_entry.pack(pady=(0, 20))
        self.submit_button = ctk.CTkButton(self.root, text="Submit", width=120,
                                           command=self.save_master_password, **self.button_style)
        self.submit_button.pack(pady=(0, 20))

    def is_master_password_present(self):
        pass

    def save_master_password(self):
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        # Checking for atleast one number and one symbol
        # Functions return a boolean value
        has_number = re.search(r'\d', password)
        has_symbol = re.search(r'\W', password)
        # Checking if passwords are not identical
        if password != confirm_password:
            self.popup(self.root, "Save Failed. Passwords are not identical")
            self.password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
        # Checking if password length is less than 7 characters
        elif len(password) < 7:
            self.popup(self.root, "Save Failed. Password must be greater than 7 characters")
            self.password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
        # Checking for at least one number in the password
        elif not has_number:
            self.popup(self.root, "Save Failed. Password must contain atleast 1 number")
            self.password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
        # Checking for at least one symbol in the password
        elif not has_symbol:
            self.popup(self.root, "Save Failed. Passwords must contain atleast 1 symbol")
            self.password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
        else:
            # If all conditions are met, encrypt and hash the password
            hashed_password = self.hash_text(password.encode("utf-8"))
            encrypted_hashed_password = self.encrypt_password(hashed_password)
            insert_password = "INSERT INTO masterpassword (password) VALUES (?)"
            with sqlite3.connect(masterpasswordsDbPath) as db:
                cursor = db.cursor()
                cursor.execute(insert_password, (encrypted_hashed_password,))
                db.commit()
            self.popup(self.root, "Save Successfull")
            app = MainVault(self.root, "All Items", "AllItems", "AllItems")
            app.run()

    def on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()