from utils.LibraryManager import sqlite3, messagebox, json
from utils.DirectoryManager import masterpasswordsDbPath, keyPath
from utils.Encryption import load_key, create_key, encrypt_password, decrypt_password, hash_text
from utils.UserSettingsManager import get_styles, setup_user_settings



class CredentialManager:
    def __init__(self, root):
        setup_user_settings()
        self.root = root
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.entry_style, self.label_style, self.button_style = get_styles()
        self.load_or_create_key()
        self.is_master_password_present()

    def load_or_create_key(self):
        with sqlite3.connect(masterpasswordsDbPath) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM masterpassword")
            stored_password = cursor.fetchone()
            if stored_password:
                # Master password exists, load the encryption key
                self.key = load_key(keyPath)
            else:
                # Master password doesn't exist, create a new key
                create_key(keyPath)
                self.key = load_key(keyPath)

    def is_master_password_present(self):
        try:
            with sqlite3.connect(masterpasswordsDbPath) as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM masterpassword")
                count = cursor.fetchone()
                if count:
                    self.run_login_screen()
                else:
                    self.run_create_master_password()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def add_password(self, website, username, password):
        encrypted_pw = encrypt_password(password, self.key)
        self.password_dict[website] = {"username": username, "password": encrypted_pw}
        with open(self.password_file, "w") as file:
            json.dump(self.password_dict, file)

    def delete_password(self, website):
        self.password_dict.pop(website)
        with open(self.password_file, "w") as file:
            json.dump(self.password_dict, file)

    def update_password(self, website, username, password):
        encrypted_pw = encrypt_password(password, self.key)
        self.password_dict[website] = {"username": username, "password": encrypted_pw}
        with open(self.password_file, "w") as file:
            json.dump(self.password_dict, file)

    def get_password(self, website):
        encrypted_pw = self.password_dict[website]["password"]
        return decrypt_password(encrypted_pw, self.key)

    def encrypt_password(self, password):
        return encrypt_password(password, self.key)

    def hash_text(self, text):
        return hash_text(text)

    @staticmethod
    def popup(parent, text):
        messagebox.showinfo("Popup Message", text, parent=parent)

    def run_login_screen(self):
        from interface.LoginScreen import LoginScreen
        
        app = LoginScreen(self.root)
        app.run()

    def run_create_master_password(self):
        from interface.CreateMasterPassword import CreateMasterPassword

        app = CreateMasterPassword(self.root)
        app.run()

    def run_mainvault(self):
        from interface.MainVault import MainVault

        app = MainVault(self.root)
        app.run()

    def run(self):
        self.root.mainloop()





















