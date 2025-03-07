from interface.CredentialManager import CredentialManager
from utils.LibraryManager import ctk, sqlite3, re
from utils.DirectoryManager import masterpasswordsDbPath

class CreateMasterPassword(CredentialManager):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setupWindow()
    

    def setupWindow(self):
        self.root.title("Create Master Password")
        rootWidth = 600
        rootHeight = 300
        self.root.geometry(f"{rootWidth}x{rootHeight}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.createWidgets()

    def createWidgets(self):
        heading1 = ctk.CTkLabel(self.root, text="Enter A Master Password", **self.labelStyle)
        heading1.pack(pady=(20, 10))

        self.passwordEntry = ctk.CTkEntry(self.root, width=200, **self.entryStyle)
        self.passwordEntry.pack(pady=(0, 20))

        heading2 = ctk.CTkLabel(self.root, text="Re-Enter Master Password", **self.labelStyle)
        heading2.pack(pady=(20, 10))

        self.confirmPasswordEntry = ctk.CTkEntry(self.root, width=200, **self.entryStyle)
        self.confirmPasswordEntry.pack(pady=(0, 20))

        self.submitButton = ctk.CTkButton(self.root, text="Submit", width=120, command=self.saveMasterPassword, **self.buttonStyle)
        self.submitButton.pack(pady=(0, 20))

    def isMasterPasswordPresent(self):
        pass

    def saveMasterPassword(self):
        password = self.passwordEntry.get()
        confirmPassword = self.confirmPasswordEntry.get()
        # Checking for atleast one number and one symbol
        # Functions return a boolean value
        hasNumber = re.search(r'\d', password)
        hasSymbol = re.search(r'\W', password)
        # Checking if passwords are not identical
        if password != confirmPassword:
            self.popup(self.root, "Save Failed. Passwords are not identical")
            self.passwordEntry.delete(0, "end")
            self.confirmPasswordEntry.delete(0, "end")
        # Checking if password length is less than 7 characters
        elif len(password) < 7:
            self.popup(self.root, "Save Failed. Password must be greater than 7 characters")
            self.passwordEntry.delete(0, "end")
            self.confirmPasswordEntry.delete(0, "end")
        # Checking for at least one number in the password
        elif not hasNumber:
            self.popup(self.root, "Save Failed. Password must contain atleast 1 number")
            self.passwordEntry.delete(0, "end")
            self.confirmPasswordEntry.delete(0, "end")
        # Checking for at least one symbol in the password
        elif not hasSymbol:
            self.popup(self.root, "Save Failed. Passwords must contain atleast 1 symbol")
            self.passwordEntry.delete(0, "end")
            self.confirmPasswordEntry.delete(0, "end")
        else:
            # If all conditions are met, encrypt and hash the password
            hashedPassword = self.hashText(password.encode("utf-8"))
            encryptedHashedPassword = self.encryptPassword(hashedPassword)
            insertPassword = "INSERT INTO masterpassword (password) VALUES (?)"
            with sqlite3.connect(masterpasswordsDbPath) as db:
                cursor = db.cursor()
                cursor.execute(insertPassword, (encryptedHashedPassword,))
                db.commit()
            self.popup(self.root, "Save Successful")

            # Close the current window and open the main vault
            self.destroyWidgets()

            # Open the main vault
            self.runMainVault()

    def onClose(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()