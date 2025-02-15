from utils.LibraryManager import *
from utils.DirectoryManager import *
from interface.CredentialManager import CredentialManager
from utils.UserSettingsManager import setup_user_settings

if __name__ == "__main__":
    # Create the root window
    root = ctk.CTk()

    setup_user_settings()

    # Run the application
    app = CredentialManager(root)
    app.run()
