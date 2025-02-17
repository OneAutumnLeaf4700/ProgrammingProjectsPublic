from interface.CredentialManager import CredentialManager
from utils.LibraryManager import ctk, sqlite3
from utils.DirectoryManager import masterpasswordsDbPath


class LoginScreen(CredentialManager):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setup_window()
        self.create_widgets()
        # Register the close icon as a valid method of termination
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Login Screen")
        self.root_width = 700
        self.root_height = 300
        self.root.geometry(f"{self.root_width}x{self.root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        self.heading1 = ctk.CTkLabel(self.root, text="Your vault is locked. Please verify your master password to continue.", **self.label_style)
        self.heading1.grid(row=0, column=0, pady=10)
        self.password = ctk.CTkEntry(self.root, width=300, height=45, placeholder_text="Master Password", show="*", **self.entry_style)
        self.password.grid(row=1, column=0, pady=5)
        self.unlock = ctk.CTkButton(self.root, text="Unlock", command=self.verify_master_password, **self.button_style)
        self.unlock.grid(row=2, column=0, pady=10)

    def is_master_password_present(self):
        pass

    def get_master_password(self):
        # Hash the password entered
        hashed_entered_password = self.hash_text(self.password.get().encode("utf-8"))
        # Connect to the database and retrieve the master password
        with sqlite3.connect(masterpasswordsDbPath) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM masterpassword WHERE id = 1")
            stored_password = cursor.fetchone()
            if stored_password:
                # Get the encrypted stored password from the database
                encrypted_stored_password = stored_password[1]
                # Decrypt the stored encrypted password
                decrypted_stored_password = self.decrypt_password(encrypted_stored_password)
                # Verify if the entered password matches the stored password
                if hashed_entered_password == decrypted_stored_password:
                    return True
        return False

    def verify_master_password(self):
        # Verify if the entered password matches the stored password
        match = self.get_master_password()
        if match:
            self.root.after(100, self.destroy_and_create_mainvault)
        else:
            self.popup(self.root, "Incorrect Password")
            self.password.delete(0, 'end')

    def destroy_and_create_mainvault(self):
        self.root.destroy()
        print("Opening Main Vault")
        #app = MainVault(ctk.CTk(), "All Items", "AllItems", "AllItems")
        #app.run()

    def cleanup_widgets(self):
        # Cleanup canvas elements if they exist
        if hasattr(self, 'heading1'):
            self.heading1.destroy()
        if hasattr(self, 'password'):
            self.password.destroy()
        if hasattr(self, 'unlock'):
            self.unlock.destroy()

    def on_close(self):
        self.cleanup_widgets()  # Clean up canvas elements
        self.root.destroy()

    def run_after_lock(self):
        self.root.mainloop()

    def run(self):
        self.root.mainloop()
