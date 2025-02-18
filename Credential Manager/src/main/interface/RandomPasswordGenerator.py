from interface.CredentialManager import CredentialManager
from utils.LibraryManager import *
from utils.DirectoryManager import *
from utils.UserSettingsManager import *



class RandomPasswordGenerator(CredentialManager):
    _instance = None # Class variable to store the single instance

    def __new__(cls):
        # If an instance of the class already exists, return it
        if cls._instance is not None:
            cls.popup(cls._instance.root, "Random Password Generator is already open")
            return cls._instance
        # If no instance exists, create a new one
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'root'): # Check if root attribute already exists
            return # Return without reinitializing if already initialized
        # Initialize the instance only if it's a new instance
        self.root = ctk.CTk()
        self.setup_window()
        self.create_widgets()
        # Register the function to handle window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.root.title("Random Password Generator")
        self.root.attributes('-topmost', True)
        root_width = 900
        root_height = 500
        self.root.geometry(f"{root_width}x{root_height}")
        self.root.resizable(False, False)

    def create_widgets(self):
        button_style = {"font": text_type, "fg_color": button_fg_color, "border_width": button_border_width, "border_color": button_border_color}
        label_style = {"font": title_type, "text_color": text_color, "fg_color": title_fg_color}
        # Frame for the password generator
        pass_generator_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        pass_generator_frame.place(relx=0, rely=0, relwidth=0.75, relheight=1)
        # Frame for the checkboxes and position it at the top
        checkbox_frame = ctk.CTkFrame(self.root, fg_color="#0f0f0f")
        checkbox_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)
        # Checkbox Frame Widgets
        self.uppercase_var = IntVar()
        self.lowercase_var = IntVar()
        self.numbers_var = IntVar()
        self.symbols_var = IntVar()
        uppercase_btn = ctk.CTkCheckBox(checkbox_frame, text="Uppercase", variable=self.uppercase_var)
        uppercase_btn.grid(row=0, column=0, sticky="w")
        lowercase_btn = ctk.CTkCheckBox(checkbox_frame, text="Lowercase", variable=self.lowercase_var)
        lowercase_btn.grid(row=1, column=0, sticky="w")
        numbers_btn = ctk.CTkCheckBox(checkbox_frame, text="Numbers", variable=self.numbers_var)
        numbers_btn.grid(row=2, column=0, sticky="w")
        symbols_btn = ctk.CTkCheckBox(checkbox_frame, text="Symbols", variable=self.symbols_var)
        symbols_btn.grid(row=3, column=0, sticky="w")
        # Password Generator Frame Widgets
        title = ctk.CTkLabel(pass_generator_frame, text="Customize your password", **label_style)
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=30)
        self.slider_label = ctk.CTkLabel(pass_generator_frame, text="Password Length: 25", **label_style)
        self.slider_label.grid(row=1, column=0, sticky="w", pady=20, padx=30)
        self.slider = ctk.CTkSlider(pass_generator_frame, from_=1, to=50, number_of_steps=50, command=self.slider_event, fg_color=button_fg_color, button_color=button_fg_color, button_hover_color=button_fg_color, width=400)
        self.slider.grid(sticky="w", row=2, column=0, columnspan=2, pady=20, padx=30)
        self.generated_password_label = ctk.CTkLabel(pass_generator_frame, text="Generated Password: ", **label_style)
        self.generated_password_label.grid(row=3, column=0, columnspan=2, padx=30)
        generate_btn = ctk.CTkButton(master=pass_generator_frame, text="Generate Password", command=self.update_random_password, **button_style)
        generate_btn.grid(row=4, column=0, pady=30, padx=30, sticky="e")
        copy_password_btn = ctk.CTkButton(master=pass_generator_frame, text="Copy To Clipboard", command=self.copytext, **button_style)
        copy_password_btn.grid(row=4, column=1, pady=30, sticky="w")

    def slider_event(self, value):
        value_int = int(value) # Convert the float value to an integer
        formatted_value = f"{value_int:02}"
        self.slider_label.configure(text=f"Password Length: {formatted_value}")

    def update_random_password(self):
        length = int(self.slider.get()) # Sets length of the password to the value of the slider
        character_sets = [] # Creates a character set that will be appended to by the required character types
        if self.uppercase_var.get():
            character_sets.append(string.ascii_uppercase)
        if self.lowercase_var.get():
            character_sets.append(string.ascii_lowercase)
        if self.numbers_var.get():
            character_sets.append(string.digits)
        if self.symbols_var.get():
            character_sets.append(string.punctuation)
        if character_sets:
            alphabet = ''.join(character_sets) # Combine selected character sets
            # Takes a random character from the character set
            # Creates a randomly generated password
            # Repeats this process as many times as the users required length to fill the password length requirement
            generated_password = ''.join(secrets.choice(alphabet) for _ in range(length))
            # Displays the generated password on a new line
            self.generated_password_label.configure(text=f"Generated Password:\n{generated_password}")
        else:
            # Displays a popup to tell the user to select a checkbox if none are selected
            self.popup(self.root, "Please select at least one character set")

    def copytext(self):
        generated_password = self.generated_password_label.cget("text") # Get the password from the generated password label
        lines = generated_password.split('\n') # Split the text into lines
        if len(lines) >= 2:
            # Get the password from the second second line as the first line is occupied by "Generated Password:"
            password = lines[1]
            pyperclip.copy(password)
            self.popup(self.root, "Password Copied to Clipboard")
        else:
            self.popup(self.root, "No Password Found")

    def on_close(self):
        RandomPasswordGenerator._instance = None
        self.root.destroy()