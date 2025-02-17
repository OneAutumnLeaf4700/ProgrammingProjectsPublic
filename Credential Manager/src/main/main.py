from utils.LibraryManager import ctk
from interface.CredentialManager import CredentialManager

if __name__ == "__main__":
    # Create the root window
    root = ctk.CTk()

    # Run the application
    app = CredentialManager(root)
    app.run()
