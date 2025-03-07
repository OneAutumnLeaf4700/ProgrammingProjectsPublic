from utils.LibraryManager import sqlite3, messagebox, json
from utils.DirectoryManager import masterpasswordsDbPath, keyPath
from utils.Encryption import loadKey, createKey, encryptPassword, decryptPassword, hashText
from utils.UserSettingsManager import getStyles, setupUserSettings

class CredentialManager:
    def __init__(self, root):
        setupUserSettings()
        self.root = root
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.entryStyle, self.labelStyle, self.buttonStyle = getStyles()
        self.loadOrCreateKey()
        self.isMasterPasswordPresent()

    def loadOrCreateKey(self):
        with sqlite3.connect(masterpasswordsDbPath) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM masterpassword")
            stored_password = cursor.fetchone()
            if stored_password:
                # Master password exists, load the encryption key
                self.key = loadKey(keyPath)
            else:
                # Master password doesn't exist, create a new key
                createKey(keyPath)
                self.key = loadKey(keyPath)

    def isMasterPasswordPresent(self):
        try:
            with sqlite3.connect(masterpasswordsDbPath) as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM masterpassword")
                count = cursor.fetchone()
                if count:
                    self.runLoginScreen()
                else:
                    self.runCreateMasterPassword()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def addPassword(self, website, username, password):
        encrypted_pw = encryptPassword(password, self.key)
        self.password_dict[website] = {"username": username, "password": encrypted_pw}
        with open(self.password_file, "w") as file:
            json.dump(self.password_dict, file)

    def deletePassword(self, website):
        self.password_dict.pop(website)
        with open(self.password_file, "w") as file:
            json.dump(self.password_dict, file)

    def updatePassword(self, website, username, password):
        encrypted_pw = encryptPassword(password, self.key)
        self.password_dict[website] = {"username": username, "password": encrypted_pw}
        with open(self.password_file, "w") as file:
            json.dump(self.password_dict, file)

    def getPassword(self, website):
        encrypted_pw = self.password_dict[website]["password"]
        return decryptPassword(encrypted_pw, self.key)

    def encryptPassword(self, password):
        return encryptPassword(password, self.key)

    def decryptPassword(self, encrypted_password):
        return decryptPassword(encrypted_password, self.key)

    def hashText(self, text):
        return hashText(text)

    @staticmethod
    def popup(parent, text):
        messagebox.showinfo("Popup Message", text, parent=parent)

    def destroyWidgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def runLoginScreen(self):
        from interface.LoginScreen import LoginScreen
        
        app = LoginScreen(self.root)
        app.run()

    def runCreateMasterPassword(self):
        from interface.CreateMasterPassword import CreateMasterPassword

        app = CreateMasterPassword(self.root)
        app.run()

    def runMainVault(self):
        from interface.MainVault import MainVault

        app = MainVault(self.root, "All Items", "AllItems", "AllItems")
        app.run()

    def run(self):
        self.root.mainloop()
