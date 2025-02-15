import os

# Get the directory of the current file
current_file_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(current_file_dir)
data_dir = os.path.join(main_dir, "..", "data")
db_path = os.path.join(main_dir, "..", "data", "database")

print(main_dir)
print(data_dir)
print(db_path)

# Define the paths relative to the base directory
allItemsDbPath = os.path.join(db_path, "AllItems.db")
favouritesDbPath = os.path.join(db_path, "Favourites.db")
masterpasswordsDbPath = os.path.join(db_path, "MPasswords.db")
userSettingsDbPath = os.path.join(db_path, "UserSettings.db")
keyPath = os.path.join(db_path, "key.key")
