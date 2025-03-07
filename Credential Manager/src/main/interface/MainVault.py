from interface.CredentialManager import CredentialManager
from interface.LoginScreen import LoginScreen
from interface.RandomPasswordGenerator import RandomPasswordGenerator
from interface.SettingsScreen import SettingsScreen
from interface.FileManager import FileManager
from interface.AddCredential import AddCredential
from interface.EditCredential import EditCredential
from interface.AdditionalInformation import AdditionalInformation
from utils.LibraryManager import ctk
from utils.UserSettingsManager import *
from utils.DirectoryManager import *


class MainVault(CredentialManager):
    _instance = None

    def __new__(cls, root, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MainVault, cls).__new__(cls)
        return cls._instance


    def __init__(self, root, title, database, table):
        if hasattr(self, 'initialized') and self.initialized:
            return
        super().__init__(root)
        self.root = root
        self.title = title
        self.database = database
        self.table = table
        self.current_page = 1  # Initialize current page to 1
        self.initialize_root_window()
        self.initialize_left_frame()
        self.initialize_right_frame(title, database, table)

    def show_login_screen(self):
        # This method creates a new root window for the LoginScreen and displays it
        new_root = ctk.CTk()
        login_screen = LoginScreen(new_root)
        login_screen.run_after_lock()

    def on_close(self):
        MainVault._instance = None
        self.root.destroy()

    def run(self):
        # Start the mainloop
        self.root.mainloop()

    def initialize_root_window(self):
        # Clearing the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Main Vault")
        self.root_width = 1800
        self.root_height = 800
        self.root.geometry(f"{self.root_width}x{self.root_height}")
        self.root.resizable(False, False)

    def initialize_left_frame(self):
        left_frame_color = "#0f0f0f"
        self.left_frame_width = 300
        self.left_frame_height = self.root_height
        button_style = {"font": subtitle_type, "fg_color": left_frame_color, "border_width": button_border_width, "border_color": left_frame_color, "text_color": text_color}
        frame_style = {"fg_color": left_frame_color}
        self.left_frame = ctk.CTkFrame(self.root, width=self.left_frame_width, height=self.left_frame_height, **frame_style)
        self.left_frame.grid(row=0, column=0, sticky="nse")
        self.left_frame.grid_propagate(False)
        # Define a lambda function to call initialize_right_frame with the "Favourites" argument
        initialize_all_items_func = lambda: self.initialize_right_frame("All Items", "AllItems", "AllItems")
        btn = ctk.CTkButton(self.left_frame, text="All items", command=initialize_all_items_func, **button_style)
        btn.grid(column=0, row=0, pady=10)
        # Define a lambda function to call initialize_right_frame with the "Favourites" argument
        initialize_favourites_func = lambda: self.initialize_right_frame("Favourites", "Favourites", "Favourites")
        favourites_button = ctk.CTkButton(self.left_frame, text="Favourites", command=initialize_favourites_func, **button_style)
        favourites_button.grid(column=0, row=1, pady=10)
        self.random_password_generator_button = ctk.CTkButton(self.left_frame, text="Random Password Generator", command=self.run_random_password_generator, **button_style)
        self.random_password_generator_button.grid(column=0, row=2, pady=10)
        self.btn = ctk.CTkButton(self.left_frame, text="Settings", command=self.run_settings, **button_style)
        self.btn.grid(column=0, row=3, pady=10)
        self.btn = ctk.CTkButton(self.left_frame, text="Import/Export", command=self.run_filemanager, **button_style)
        self.btn.grid(column=0, row=4, pady=10)
        self.btn = ctk.CTkButton(self.left_frame, text="Additional Information", command=self.run_additional_information, **button_style)
        self.btn.grid(column=0, row=5, pady=10)

    def initialize_right_frame(self, window_title, database, table):
        # Clear everything in the root window except the left frame
        self.clear_right_widgets()
        self.right_frame_width = self.root_width - self.left_frame_width
        self.right_frame_height = self.root_height
        self.window_title = window_title
        # Initialize the right frame
        label_style = {"font": title_type, "text_color": text_color, "fg_color": title_fg_color}
        self.right_frame = ctk.CTkFrame(self.root, width=self.right_frame_width, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_propagate(False)
        self.right_frame.rowconfigure(2, weight=1)
        # Set the title label
        title_label = ctk.CTkLabel(self.right_frame, text=self.window_title, **label_style)
        title_label.grid(row=0, column=0, padx=10)
        # Set other labels as needed
        website_label = ctk.CTkButton(self.right_frame, text="Website", font=title_type, fg_color="transparent", border_width=None, border_color="Transparent", text_color=text_color, command=lambda: self.load_credentials("website", database, table))
        website_label.grid(row=1, column=0, padx=10, pady=30)
        username_label = ctk.CTkButton(self.right_frame, text="Username", font=title_type, fg_color="transparent", border_width=None, border_color="Transparent", text_color=text_color, command=lambda: self.load_credentials("username", database, table))
        username_label.grid(row=1, column=1, padx=30)
        password_label = ctk.CTkLabel(self.right_frame, text="Password", **label_style)
        password_label.grid(row=1, column=2, padx=30)
        self.initialize_search_frame(database, table)
        self.initialize_scrollable_frame(database, table)
        self.initialize_lifted_widgets(database, table)

    def initialize_search_frame(self, database, table):
        button_style = {"font": text_type, "fg_color": "#0f0f0f", "border_width": button_border_width, "border_color": button_border_color, "text_color": text_color}
        entry_style = {"font": subtitle_type, "text_color": text_color, "fg_color": txt_entry_fg_color}
        search_bar_frame = ctk.CTkFrame(self.right_frame, width=600, height=40, fg_color="transparent")
        search_bar_frame.place(relx=1, rely=0, anchor="ne")
        # Store a reference to the search_bar widget as an instance variable
        self.search_bar = ctk.CTkEntry(search_bar_frame, width=300, placeholder_text="Search", **entry_style)
        self.search_bar.grid(row=0, column=0, sticky="ne", padx=5, pady=10)
        # Define a lambda function to call search_credentials with the appropriate table name
        search_func = lambda: self.search_credentials(database, table)
        btn = ctk.CTkButton(search_bar_frame, text="Search", command=search_func, **button_style)
        btn.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

    def initialize_scrollable_frame(self, database, table):
        # Scrollable frame to display credentials
        self.scrollable_window = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent", width=self.right_frame_width - 20, height=500)
        self.scrollable_window.grid(row=2, column=0, columnspan=6, rowspan=6, sticky="nsew")
        self.load_credentials("website", database, table)

    def initialize_lifted_widgets(self, database, table):
        button_style = {"font": subtitle_type, "fg_color": "transparent", "border_width": None, "border_color": "Transparent", "text_color": text_color}
        # Create a frame for the add button
        lifted_frame = ctk.CTkFrame(self.right_frame, width=self.right_frame_width, height=100, fg_color="transparent")
        lifted_frame.place(relx=0, rely=1, anchor='sw', relwidth=1)
        # Create navigation buttons
        prev_button = ctk.CTkButton(lifted_frame, text="Previous Page", command=self.previous_page, **button_style)
        prev_button.place(relx=0.4, rely=0.5, anchor='center')
        next_button = ctk.CTkButton(lifted_frame, text="Next Page", command=self.next_page, **button_style)
        next_button.place(relx=0.5, rely=0.5, anchor='center')
        add_credential_func = lambda: self.run_add_credential(database, table, self.credentialArray)
        add_button = ctk.CTkButton(lifted_frame, text="Add", command=add_credential_func, **button_style)
        add_button.place(relx=0.95, rely=0.5, anchor='e')

    def clear_right_widgets(self):
        # Iterate over all children widgets of the root window
        for widget in self.root.winfo_children():
            # Check if the widget is not the left frame
            if widget != self.left_frame:
                # Destroy the widget
                widget.destroy()

    def is_master_password_present(self):
        pass

    def load_credentials(self, sort_by, database, table):
        # Clear previous credentials displayed
        self.clear_credentials()
        # Calculate start and end indices based on current page
        start_index = (self.current_page - 1) * 6
        end_index = self.current_page * 6
        with sqlite3.connect(f"{db_path}/{database}.db") as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            self.credentialArray = cursor.fetchall()
            
            # Sort the credentialArray based on the specified field
            if sort_by == "website":
                self.credentialArray.sort(key=lambda x: x[1])  # Sort by website name
            elif sort_by == "username":
                self.credentialArray.sort(key=lambda x: x[2])  # Sort by username
            label_style = {"font": title_type, "text_color": text_color, "fg_color": title_fg_color}
            button_style = {"font": title_type, "fg_color": "transparent", "border_width": None, "border_color": None}

        def create_edit_func(row):
            return lambda: self.run_edit_credential(database, table, self.credentialArray[row])

        for row_value in range(start_index, min(end_index, len(self.credentialArray))):
            toggle_password_func = lambda row=row_value, col=3: self.toggle_password_visibility(row, col)
            favourite_func = lambda: self.favorite_record(self.credentialArray[row_value])
            edit_func = create_edit_func(row_value)  # Create edit_func with captured row_value
            delete_func = lambda position=row_value: self.delete_record(position, database, table)
            website_label = ctk.CTkLabel(self.scrollable_window, width=200, text=self.credentialArray[row_value][1], **label_style)
            website_label.grid(column=0, row=row_value, pady=20, sticky="w")
            username_label = ctk.CTkLabel(self.scrollable_window, width=200, text=self.credentialArray[row_value][2], **label_style)
            username_label.grid(column=1, row=row_value, padx=50, pady=20, sticky="w")
            self.password_label = ctk.CTkLabel(self.scrollable_window, width=200, text="********", **label_style)
            self.password_label.grid(column=2, row=row_value, padx=50, pady=20, sticky="w")
            self.toggle_password_btn = ctk.CTkButton(self.scrollable_window, text="Show/Hide Password", command=toggle_password_func, **button_style)
            self.toggle_password_btn.grid(row=row_value, column=3)
            if database == "AllItems":
                btn = ctk.CTkButton(self.scrollable_window, text="Favourite", command=lambda row=row_value: self.favorite_record(self.credentialArray[row]), **button_style)
                btn.grid(column=4, row=row_value, pady=10)
                btn = ctk.CTkButton(self.scrollable_window, text="Edit", command=edit_func, **button_style)
                btn.grid(column=5, row=row_value, pady=10)
                btn = ctk.CTkButton(self.scrollable_window, text="Delete", command=lambda position=row_value: self.delete_record(position, database, table), **button_style)
                btn.grid(column=6, row=row_value, pady=10)
            else:
                btn = ctk.CTkButton(self.scrollable_window, text="Edit", command=lambda: self.run_edit_credential(database, table, self.credentialArray[row_value]), **button_style)
                btn.grid(column=4, row=row_value, pady=10)
                btn = ctk.CTkButton(self.scrollable_window, text="Delete", command=lambda position=row_value: self.delete_record(position, database, table), **button_style)
                btn.grid(column=5, row=row_value, pady=10)

    def search_credentials(self, database, table):
        query = self.search_bar.get().strip()
        # Construct the SQL query based on the provided table name
        sql_query = f"SELECT * FROM {table} WHERE website LIKE ? OR username LIKE ?"
        with sqlite3.connect(f"{db_path}/{database}.db") as db:
            cursor = db.cursor()
            cursor.execute(sql_query, ('%' + query + '%', '%' + query + '%'))
            search_results = cursor.fetchall()
        self.display_search_results(search_results)

    def display_search_results(self, search_results):
        # Clear previous search results
        for widget in self.scrollable_window.winfo_children():
            widget.destroy()
        # Display the search results
        for counter, result in enumerate(search_results):
            self.row_value = counter
            self.website_label = ctk.CTkLabel(self.scrollable_window, width=200, text=result[1], **self.label_style)
            self.website_label.grid(column=0, row=self.row_value, pady=20, sticky="w")
            self.username_label = ctk.CTkLabel(self.scrollable_window, width=200, text=result[2], **self.label_style)
            self.username_label.grid(column=1, row=self.row_value, pady=20, sticky="w")
            self.password_label = ctk.CTkLabel(self.scrollable_window, width=200, text="********", **self.label_style)
            self.password_label.grid(column=2, row=self.row_value, pady=20, sticky="w")
            self.toggle_password_btn = ctk.CTkButton(self.scrollable_window, text="Show/Hide Password", command=None, **self.button_style)
            self.toggle_password_btn.grid(row=self.row_value, column=3)
            self.toggle_password_btn = ctk.CTkButton(self.scrollable_window, text="Edit", command=None, **self.button_style)
            self.toggle_password_btn.grid(row=self.row_value, column=4, pady=10, padx=10)
            self.btn = ctk.CTkButton(self.scrollable_window, text="Delete", command=None, **self.button_style)
            self.btn.grid(column=5, row=self.row_value, pady=10, padx=10)

    def toggle_password_visibility(self, row, col):
        # Function to toggle the visibility of password at the specified row and column
        try:
            displayed_password = self.credentialArray[row][col]
            current_text = self.password_label.cget("text")
            if current_text == "********":
                # If password is hidden, show it
                encrypted_password = displayed_password
                decrypted_password = self.decrypt_password(encrypted_password)
                self.password_label.configure(text=decrypted_password)
            else:
                # If password is shown, hide it
                self.password_label.configure(text="********")
        except IndexError:
            print("Invalid row index provided.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def favorite_record(self, record_array):
        website = record_array[1]
        username = record_array[2]
        encrypted_password = record_array[3]
        try:
            # Check if the record already exists in the favorites database
            with sqlite3.connect(favouritesDbPath) as db:
                cursor = db.cursor()
                # Execute a query to check if the record exists
                cursor.execute("SELECT * FROM Favourites WHERE website = ? AND username = ?", (website, username))
                existing_record = cursor.fetchone()
                if existing_record:
                    # If the record exists, display a message and return
                    self.popup(self.root, "Credential already exists in favorites")
                    return
                # If the record does not exist, insert it into the favorites database
                insert_values = """INSERT INTO Favourites(website, username, password) VALUES (?, ?, ?) """
                with sqlite3.connect(favouritesDbPath) as db:
                    cursor = db.cursor()
                    cursor.execute(insert_values, (website, username, encrypted_password))
                    db.commit()
                self.popup(self.root, "Credential added to favorites")
        except Exception as e:
            self.popup(self.root, f"An error occurred: {e}")

    def delete_record(self, row_value, database, table):
        with sqlite3.connect(f"{db_path}/{database}.db") as db:
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id=?", (self.credentialArray[row_value][0],))
            db.commit()
        app = MainVault(self.root, self.title, self.database, self.table)
        app.run()

    def next_page(self):
        # Increment current page
        self.current_page += 1
        # Reload credentials based on the new page
        self.load_credentials("website", self.database, self.table)

    def previous_page(self):
        # Ensure current page doesn't go below 1
        if self.current_page > 1:
            # Decrement current page
            self.current_page -= 1
            # Reload credentials based on the new page
            self.load_credentials("website", self.database, self.table)

    def clear_credentials(self):
        # Clear the scrollable window
        for widget in self.scrollable_window.winfo_children():
            widget.destroy()

    def run_random_password_generator(self):
        self.random_password_generator_instance = RandomPasswordGenerator()
        self.random_password_generator_instance.run()

    def run_settings(self):
        self.settings_instance = SettingsScreen()
        self.settings_instance.run()

    def run_filemanager(self):
        self.filemanager_instance = FileManager()
        self.filemanager_instance.run()

    def run_add_credential(self, database, table, array):
        add_credential_instance = AddCredential(database, table, array)
        add_credential_instance.run()

    def run_edit_credential(self, database, table, record_array):
        edit_credentials_instance = EditCredential(database, table, record_array)
        edit_credentials_instance.run()

    def run_additional_information(self):
        additional_information_instance = AdditionalInformation()
        additional_information_instance.run()

    def toggle_password_visibility(self, row, col):
        # Function to toggle the visibility of password at the specified row and column
        try:
            displayed_password = self.credentialArray[row][col]
            current_text = self.password_label.cget("text")
            if current_text == "********":
                # If password is hidden, show it
                encrypted_password = displayed_password
                decrypted_password = self.decrypt_password(encrypted_password)
                self.password_label.configure(text=decrypted_password)
            else:
                # If password is shown, hide it
                self.password_label.configure(text="********")
        except IndexError:
            print("Invalid row index provided.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def favorite_record(self, record_array):
        website = record_array[1]
        username = record_array[2]
        encrypted_password = record_array[3]
        try:
            # Check if the record already exists in the favorites database
            with sqlite3.connect(favouritesDbPath) as db:
                cursor = db.cursor()
                # Execute a query to check if the record exists
                cursor.execute("SELECT * FROM Favourites WHERE website = ? AND username = ?", (website, username))
                existing_record = cursor.fetchone()
                if existing_record:
                    # If the record exists, display a message and return
                    self.popup(self.root, "Credential already exists in favorites")
                    return
                # If the record does not exist, insert it into the favorites database
                insert_values = """INSERT INTO Favourites(website, username, password) VALUES (?, ?, ?) """
                with sqlite3.connect(favouritesDbPath) as db:
                    cursor = db.cursor()
                    cursor.execute(insert_values, (website, username, encrypted_password))
                    db.commit()
                self.popup(self.root, "Credential added to favorites")
        except Exception as e:
            self.popup(self.root, f"An error occurred: {e}")

    def delete_record(self, row_value, database, table):
        with sqlite3.connect(f"{db_path}/{database}.db") as db:
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id=?", (self.credentialArray[row_value][0],))
            db.commit()
        app = MainVault(self.root, self.title, self.database, self.table)
        app.run()

    def next_page(self):
        # Increment current page
        self.current_page += 1
        # Reload credentials based on the new page
        self.load_credentials("website", self.database, self.table)

    def previous_page(self):
        # Ensure current page doesn't go below 1
        if self.current_page > 1:
            # Decrement current page
            self.current_page -= 1
            # Reload credentials based on the new page
            self.load_credentials("website", self.database, self.table)

    def clear_credentials(self):
        # Clear the scrollable window
        for widget in self.scrollable_window.winfo_children():
            widget.destroy()

    def run_random_password_generator(self):
        self.random_password_generator_instance = RandomPasswordGenerator()
        self.random_password_generator_instance.run()

    def run_settings(self):
        self.settings_instance = SettingsScreen()
        self.settings_instance.run()

    def run_filemanager(self):
        self.filemanager_instance = FileManager()
        self.filemanager_instance.run()

    def run_add_credential(self, database, table, array):
        add_credential_instance = AddCredential(database, table, array)
        add_credential_instance.run()

    def run_edit_credential(self, database, table, record_array):
        edit_credentials_instance = EditCredential(database, table, record_array)
        edit_credentials_instance.run()

    def run_additional_information(self):
        additional_information_instance = AdditionalInformation()
        additional_information_instance.run()