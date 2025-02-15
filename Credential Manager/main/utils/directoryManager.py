import os

# Get the directory of the current file
current_file_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_file_dir)
db_path = os.path.join(base_dir, "data")

print(base_dir)
print(db_path)

# Define the paths relative to the base directory
allItemsDbPath = os.path.join(db_path, "AllItems.db")
favouritesDbPath = os.path.join(db_path, "Favourites.db")
masterpasswordsDbPath = os.path.join(db_path, "MPasswords.db")
userSettingsDbPath = os.path.join(db_path, "UserSettings.db")
keyPath = os.path.join(db_path, "key.key")
