import customtkinter as ctk  # Import the CustomTkinter library, which provides custom themed widgets for Tkinter, as 'ctk'
import tkinter as tk  # Import the standard Tkinter library for creating GUI applications, as 'tk'
import os  # Import the os module for interacting with the operating system (file and directory management)
import random  # Import the random module to generate random numbers
from collections import deque  # Import deque from collections for creating a double-ended queue, useful for managing a sequence of items
from PIL import Image, ImageTk  # Import the Image and ImageTk classes from the Pillow library for image processing and display
from matplotlib.figure import Figure  # Import the Figure class from matplotlib for creating figures for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import the FigureCanvasTkAgg class to integrate Matplotlib figures into Tkinter
from datetime import datetime  # Import the datetime class to handle date and time operations
from cryptography.fernet import Fernet  # Import the Fernet class from the cryptography library for secure encryption and decryption, particularly for handling passwords
import json
import re  # For sanitizing filenames

class UserManager:
    def __init__(self, user_dir):
        self.user_dir = user_dir  # Directory to store user JSON files
        os.makedirs(self.user_dir, exist_ok=True)  # Create the directory if it doesn't exist
        self.key = self._get_or_generate_key()
        self.cipher = Fernet(self.key)

    def _get_or_generate_key(self):
        key_file = "secret.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def _encrypt_password(self, password):
        """Encrypt the password."""
        return self.cipher.encrypt(password.encode()).decode()

    def _decrypt_password(self, encrypted_password):
        """Decrypt the password."""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    #maybe get rid of this
    def _sanitize_username(self, username):
        """Sanitize the username to create a safe filename."""
        return re.sub(r'[^a-zA-Z0-9_-]', '_', username)

    def _get_user_file_path(self, username):
        """Get the file path for the user's JSON file."""
        sanitized_username = self._sanitize_username(username)
        return os.path.join(self.user_dir, f"{sanitized_username}.json")

    def user_exists(self, username):
        """Check if a user exists."""
        return os.path.exists(self._get_user_file_path(username))

    def read_user(self, username):
        """Read a user's data from their JSON file."""
        file_path = self._get_user_file_path(username)
        if not os.path.exists(file_path):
            return None  # User does not exist

        with open(file_path, "r") as file:
            data = json.load(file)
            # Decrypt the password before returning
            data['password'] = self._decrypt_password(data['password'])
            return data

    def save_user(self, username, password):
        """Save a new user to their own JSON file."""
        if self.user_exists(username):
            raise ValueError("User already exists.")

        encrypted_password = self._encrypt_password(password)
        user_data = {
            "username": username,
            "password": encrypted_password,
            "AOO": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1},
            "VOO": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1},
            "AAI": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1, "Atrial Sensitivity": 2.5, "ARP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12},
            "VVI": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1, "Ventricular Sensitivity": 2.5, "VRP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12},
            "AOOR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            "VOOR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            "AAIR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1, "Atrial Sensitivity": 2.5, "ARP": 250, "PVARP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            "VVIR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1, "Ventricular Sensitivity": 2.5, "VRP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            # You can add more user-specific data here
        }

        file_path = self._get_user_file_path(username)
        with open(file_path, "w") as file:
            json.dump(user_data, file, indent=4)

    def update_user_data(self, username, data):      
        file_path = self._get_user_file_path(username)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def delete_user(self, username):
        """Delete a user's JSON file."""
        file_path = self._get_user_file_path(username)
        if os.path.exists(file_path):
            os.remove(file_path)

    def read_all_users(self):
        """Read all users' data."""
        users = {}
        for filename in os.listdir(self.user_dir):
            if filename.endswith(".json"):
                username = filename[:-5]  # Remove '.json' extension
                user_data = self.read_user(username)
                if user_data:
                    users[username] = user_data['password']
        return users

class LoginPage:
    def __init__(self, master, user_manager, app, success_message=False):  # Initialize the login page
        self.master = master # The main window that contains everything
        self.user_manager = user_manager # UserManager instance to handle user data
        self.app = app  # Store the app reference to the main application
        self.success_message = success_message  # Whether to show a success message
        self.create_top_widgets()  #Call the function to create the interface elements
        self.create_widgets()  #Call the function to create the interface elements

    

    def create_top_widgets(self):
        # Create a frame to contain the top bar
        container_frame = ctk.CTkFrame(self.master, height=25, fg_color="#000000")
        container_frame.pack(fill="x", pady=2)
        container_frame.columnconfigure(0, weight=1)
        container_frame.columnconfigure(1, weight=1)
        container_frame.columnconfigure(2, weight=1)

        # Left section: Pacemaker Connection
        pacemaker_connection_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        pacemaker_connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Use a nested frame for label + icon

        pacemaker_connection = ctk.CTkLabel(pacemaker_connection_frame, text="Pacemaker Connection:", font=("Arial", 14, "bold"))
        pacemaker_connection.pack(side="left", padx=5)

        connection_status = True  # Need to change this still
        # Load the Pacemaker Icon
        if connection_status==True:
            pacemaker_icon_path = "icons/connected.png"
        else:
            pacemaker_icon_path = "icons/disconnected.png"  # Path to the saved pacemaker icon
        pacemaker_image = Image.open(pacemaker_icon_path).resize((20, 20))  # Resize as needed
        pacemaker_icon = ImageTk.PhotoImage(pacemaker_image)

        # Pacemaker Icon Label
        pacemaker_icon_label = ctk.CTkLabel(pacemaker_connection_frame, image=pacemaker_icon, text="")
        pacemaker_icon_label.image = pacemaker_icon  # Prevent garbage collection
        pacemaker_icon_label.pack(side="left")

        # Middle section: Date and Time
        self.date_time_label = ctk.CTkLabel(container_frame, text="", font=("Arial", 14), anchor="center")
        self.date_time_label.grid(row=0, column=1, padx=10, pady=10)

        # Right section: Battery Life
        battery_life_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        battery_life_frame.grid(row=0, column=2, padx=10, pady=10, sticky="e")  # Use a nested frame for label + icon

        # Battery Life Label
        battery_life = ctk.CTkLabel(battery_life_frame, text="Battery Life:", font=("Arial", 14))
        battery_life.pack(side="left", padx=5)

        # Load the Battery Icon
        battery_icon_path = "icons/battery.png"  # Path to the saved battery icon
        battery_image = Image.open(battery_icon_path).resize((20, 20))  # Resize as needed
        battery_icon = ImageTk.PhotoImage(battery_image)

        # Battery Icon Label
        battery_icon_label = ctk.CTkLabel(battery_life_frame, image=battery_icon, text="")
        battery_icon_label.image = battery_icon  # Prevent garbage collection
        battery_icon_label.pack(side="left")

        # Start updating the time
        self.update_time()



    def update_time(self):
        if self.date_time_label.winfo_exists():
            formatted_datetime = datetime.now().strftime("%Y-%m-%d - %H:%M:%S")
            self.date_time_label.configure(text=f"{formatted_datetime}")
            self.master.after(1000, self.update_time)  # Schedule the next update

    def create_widgets(self):
        # Create a frame to contain the login form
        container_frame = ctk.CTkFrame(self.master, width = 200, height = 300, corner_radius=15,fg_color='#ADD8E6')
        container_frame.pack(pady=30) 

        # Configure grid for the container_frame to manage resizing
        container_frame.columnconfigure(0, weight=1)
        container_frame.rowconfigure(0, weight=1) # For login label
        container_frame.rowconfigure(1, weight=1) # For username entry
        container_frame.rowconfigure(2, weight=1) # For password entry
        container_frame.rowconfigure(3, weight=1) # For login button
        container_frame.rowconfigure(4, weight=1) # For exit button

        # Create a frame to center the login form
        center_frame = ctk.CTkFrame(container_frame, corner_radius=15)
        center_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Login label (header) with custom font size
        login_label = ctk.CTkLabel(center_frame, text="LeTron James PACEMAKER", font=("Arial", 24))
        login_label.pack(pady=(20, 10), padx=10, fill="both")

        # Username label
        username_label = ctk.CTkLabel(center_frame, text="Username:", font=("Arial", 18))
        username_label.pack(pady=(5, 2),padx=178, anchor='w')

        # Entry box for the username (adjusted height and width)
        self.username_entry = ctk.CTkEntry(center_frame, height=40, width=300, font=("Arial", 18))
        self.username_entry.pack(pady=(2,5))

        # Password label
        password_label = ctk.CTkLabel(center_frame, text="Password:", font=("Arial", 18))
        password_label.pack(pady=(5, 2), padx=178, anchor='w')

        # Entry box for the password (shows '*' instead of actual characters)
        self.password_entry = ctk.CTkEntry(center_frame, show="*", height=40, width=300, font=("Arial", 18))
        self.password_entry.pack(pady=(2,5))

        # Label to show error messages if login fails (initially empty)
        self.login_error_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent", font=("Arial", 16))
        self.login_error_label.pack(pady=(5, 2))

        # If a user was successfully created, display a success message
        if self.success_message:
            success_label = ctk.CTkLabel(center_frame, text="User successfully created!", text_color="green", font=("Arial", 16))
            success_label.pack(pady=(5, 2))

        # Login button with adjusted size
        login_button = ctk.CTkButton(center_frame, text="Login", command=self.handle_login, height=50, width=300, font=("Arial", 18))
        login_button.pack(pady=(20, 10))

        # Bind the Enter key to trigger the login action
        self.master.unbind("<Return>")  # Unbind any previous bindings
        self.master.bind("<Return>", lambda event: self.handle_login())  # Bind Enter to login

        # Create New User button with adjusted size
        create_user_button = ctk.CTkButton(center_frame, text="Create New User", command=self.open_create_user_page, height=50, width=300, font=("Arial", 18))
        create_user_button.pack(pady=(10, 20))

        user_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        user_frame.pack(pady=(10, 20))
        total_users = len(os.listdir(self.user_manager.user_dir))
        static_users_label = ctk.CTkLabel(user_frame, text=f"Total Users: ", font=("Arial", 16))
        static_users_label.pack(side="left")
        if total_users >= 10:
            dynamic_users_label = ctk.CTkLabel(user_frame, text=f"{total_users}/10", font=("Arial", 16), text_color="red")
            dynamic_users_label.pack(side="left")
        else:
            dynamic_users_label = ctk.CTkLabel(user_frame, text=f"{total_users}/10", font=("Arial", 16))
            dynamic_users_label.pack(side="left")
        
    def handle_login(self):
        # Get the username and password from the entry boxes entered by user
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Call the login function to check if credentials are correct
        self.login(username, password)

    def login(self, username, password):
        user_data = self.user_manager.read_user(username)
        self.login_error_label.configure(text="")

        if user_data and user_data['password'] == password:
            self.app.open_main_page(username)
        else:
            # Show error message
            self.login_error_label.configure(
                text="", fg_color="transparent")
            self.master.after(100, lambda: self.login_error_label.configure(
                text="Incorrect username or password.", text_color="red"))
            # Clear input fields
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


    def open_create_user_page(self):
        self.app.open_create_user_page() # Open the page to create a new user

class CreateUserPage:
    def __init__(self, master, user_manager, app): # Initialize the create user page
        self.master = master  # Reference to the main window (the parent window)
        self.user_manager = user_manager  # Reference to the user manager for saving and reading user data
        self.app = app  # Reference to the main application
        self.create_top_widgets()
        self.create_widgets()  # Call the function to create the interface elements

    def create_top_widgets(self):
        # Create a frame to contain the top bar
        container_frame = ctk.CTkFrame(self.master, height=25, fg_color="#000000")
        container_frame.pack(fill="x", pady=2)
        container_frame.columnconfigure(0, weight=1)
        container_frame.columnconfigure(1, weight=1)
        container_frame.columnconfigure(2, weight=1)

        # Left section: Pacemaker Connection
        pacemaker_connection_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        pacemaker_connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Use a nested frame for label + icon

        pacemaker_connection = ctk.CTkLabel(pacemaker_connection_frame, text="Pacemaker Connection:", font=("Arial", 14, "bold"))
        pacemaker_connection.pack(side="left", padx=5)

        connection_status = True  # Need to change this still
        # Load the Pacemaker Icon
        if connection_status==True:
            pacemaker_icon_path = "icons/connected.png"
        else:
            pacemaker_icon_path = "icons/disconnected.png"  # Path to the saved pacemaker icon
        pacemaker_image = Image.open(pacemaker_icon_path).resize((20, 20))  # Resize as needed
        pacemaker_icon = ImageTk.PhotoImage(pacemaker_image)

        # Pacemaker Icon Label
        pacemaker_icon_label = ctk.CTkLabel(pacemaker_connection_frame, image=pacemaker_icon, text="")
        pacemaker_icon_label.image = pacemaker_icon  # Prevent garbage collection
        pacemaker_icon_label.pack(side="left")

        # Middle section: Date and Time
        self.date_time_label = ctk.CTkLabel(container_frame, text="", font=("Arial", 14), anchor="center")
        self.date_time_label.grid(row=0, column=1, padx=10, pady=10)

        # Right section: Battery Life
        battery_life_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        battery_life_frame.grid(row=0, column=2, padx=10, pady=10, sticky="e")  # Use a nested frame for label + icon

        # Battery Life Label
        battery_life = ctk.CTkLabel(battery_life_frame, text="Battery Life:", font=("Arial", 14))
        battery_life.pack(side="left", padx=5)

        # Load the Battery Icon
        battery_icon_path = "icons/battery.png"  # Path to the saved battery icon
        battery_image = Image.open(battery_icon_path).resize((20, 20))  # Resize as needed
        battery_icon = ImageTk.PhotoImage(battery_image)

        # Battery Icon Label
        battery_icon_label = ctk.CTkLabel(battery_life_frame, image=battery_icon, text="")
        battery_icon_label.image = battery_icon  # Prevent garbage collection
        battery_icon_label.pack(side="left")

        # Start updating the time
        self.update_time()



    def update_time(self):
        if self.date_time_label.winfo_exists():
            formatted_datetime = datetime.now().strftime("%Y-%m-%d - %H:%M:%S")
            self.date_time_label.configure(text=f"{formatted_datetime}")
            self.master.after(1000, self.update_time)  # Schedule the next update


    def create_widgets(self):
        # Create a frame that will fill the window screen
        container_frame = ctk.CTkFrame(self.master, width=200, height= 300, corner_radius=15, fg_color="#ADD8E6")
        container_frame.pack(pady=30) # Make it expand to fill the screen

        # Configure a grid system inside the container for proper resizing
        container_frame.columnconfigure(0, weight=1)  # Allow column to stretch
        container_frame.rowconfigure(0, weight=1)  # For title
        container_frame.rowconfigure(1, weight=1)  # For username label
        container_frame.rowconfigure(2, weight=1)  # For password label
        container_frame.rowconfigure(3, weight=1)  # For error label
        container_frame.rowconfigure(4, weight=1)  # For buttons
        

        # Center Frame to contain the create user form
        center_frame = ctk.CTkFrame(container_frame)
        center_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew") # Positioned at the center

        # Label for the create user page
        create_user_label = ctk.CTkLabel(center_frame, text="Create a New User", font=("Arial", 24))
        create_user_label.pack(pady=(20, 10), padx=10, fill="both") # Add padding and fill horizontally

        # Label for the new username input
        new_username_label = ctk.CTkLabel(center_frame, text="New Username:", font=("Arial", 18))
        new_username_label.pack(pady=(5, 2), padx=52, anchor="w") # Add padding and align to the left

        # Entry box for the new username (with increased size)
        self.new_username_entry = ctk.CTkEntry(center_frame, height=40, width=300, font=("Arial", 18))  # Increased size
        self.new_username_entry.pack(pady=(2,10),padx=50) # Add padding around the entry field

        # New Password label and entry
        new_password_label = ctk.CTkLabel(center_frame, text="New Password:", font=("Arial", 18))
        new_password_label.pack(pady=(5, 2), padx=52, anchor="w") # Add padding between label and entry field

        # Entry box for the new password (hidden characters with '*')
        self.new_password_entry = ctk.CTkEntry(center_frame, show="*", height=40, width=300, font=("Arial", 18))  # Password hidden
        self.new_password_entry.pack(pady=(2,10), padx=50)  # Add padding around the entry field

        # Label for displaying error messages (initially empty)
        self.create_user_error_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent", font=("Arial", 16))
        self.create_user_error_label.pack(pady=(5, 2))  # Add padding around the error label

        # Button for creating a new user
        create_user_button = ctk.CTkButton(center_frame, text="Create User", command=self.handle_create_user, height=50, width=300, font=("Arial", 18))
        create_user_button.pack(pady=(20, 10))  # Add padding for the create button

        # Unbind any previous Enter key actions
        self.master.unbind("<Return>")
        # Bind the Enter key to the create user action
        self.master.bind("<Return>", lambda event: self.handle_create_user())

        # Button to go back to the login page
        back_button = ctk.CTkButton(center_frame, text="Back", command=self.app.open_login_page, height=50, width=300, font=("Arial", 18))
        back_button.pack(pady=(10, 20))  # Add padding for the back button

        user_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        user_frame.pack(pady=(10, 20))
        total_users = len(os.listdir(self.user_manager.user_dir))
        static_users_label = ctk.CTkLabel(user_frame, text=f"Total Users: ", font=("Arial", 16))
        static_users_label.pack(side="left")
        if total_users >= 10:
            dynamic_users_label = ctk.CTkLabel(user_frame, text=f"{total_users}/10", font=("Arial", 16), text_color="red")
            dynamic_users_label.pack(side="left")
        else:
            dynamic_users_label = ctk.CTkLabel(user_frame, text=f"{total_users}/10", font=("Arial", 16))
            dynamic_users_label.pack(side="left")

    # this might cause an issue with the sizing if the length of the error message is larger than the entry box
    def handle_create_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if self.user_manager.user_exists(new_username):
            self.show_error("Error: Username already exists! Choose a different one.")
        elif len(os.listdir(self.user_manager.user_dir)) >= 10:
            self.show_error("Error: Max number of users reached.")
        elif " " in new_username or ":" in new_username or " " in new_password or ":" in new_password:
            self.show_error("Error: Usernames and passwords cannot contain spaces or colons.")
        elif "" == new_username or "" == new_password:
            self.show_error("Must create both a username and password.")
        else:
            try:
                self.user_manager.save_user(new_username, new_password)
                self.app.open_login_page(success_message=True)
            except ValueError as ve:
                self.show_error(str(ve))

    def show_error(self, message):
        self.create_user_error_label.configure(text="", fg_color="transparent") # Clear any previous error messages
        self.master.after(100, lambda: self.create_user_error_label.configure(text=message, text_color="red")) # After 100 ms, show the error message
        self.new_username_entry.delete(0, tk.END) # Clear the new username entry field
        self.new_password_entry.delete(0, tk.END) # Clear the new password entry field

class MainPage:
    def __init__(self, master, app, username, user_manager): # Initialize the main page
        self.master = master # Reference to the main window
        self.app = app # Reference to the main application
        self.username = username # Store the username for the current user
        
        self.user_manager = user_manager  # Ensure user_manager is passed to the main page
        
        
        #initial graphing data
        self.y_values = deque([0] * 30, maxlen=30)  # Y-axis values for the plot
        self.x_values = deque(range(0, 3000, 100), maxlen=30)  # X-axis values for the plot

        # Create a figure and axis for the plot
        self.fig = Figure(figsize=(3, 5), dpi=100)  # Adjust size for better visibility
        self.ax = self.fig.add_subplot(111)

        # Label the graph
        self.ax.set_title("Electrogram")  # Set the title of the plot
        self.ax.set_xlabel("Time (ms)")   # Label for the x-axis
        self.ax.set_ylabel("Amplitude (V)")  # Label for the y-axis

        self.line, = self.ax.plot(self.x_values, self.y_values)  #Plot the initial x and y values (empty or default data)

        self.create_top_widgets()
        self.create_widgets() # Call the function to create the interface elements

    def create_top_widgets(self):
        # Create a frame to contain the top bar
        container_frame = ctk.CTkFrame(self.master, height=25, fg_color="#000000")
        container_frame.pack(fill="x", pady=2)
        container_frame.columnconfigure(0, weight=1)
        container_frame.columnconfigure(1, weight=1)
        container_frame.columnconfigure(2, weight=1)

        # Left section: Pacemaker Connection
        pacemaker_connection_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        pacemaker_connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Use a nested frame for label + icon

        pacemaker_connection = ctk.CTkLabel(pacemaker_connection_frame, text="Pacemaker Connection:", font=("Arial", 14, "bold"))
        pacemaker_connection.pack(side="left", padx=5)

        connection_status = True  # Need to change this still
        # Load the Pacemaker Icon
        if connection_status==True:
            pacemaker_icon_path = "icons/connected.png"
        else:
            pacemaker_icon_path = "icons/disconnected.png"  # Path to the saved pacemaker icon
        pacemaker_image = Image.open(pacemaker_icon_path).resize((20, 20))  # Resize as needed
        pacemaker_icon = ImageTk.PhotoImage(pacemaker_image)

        # Pacemaker Icon Label
        pacemaker_icon_label = ctk.CTkLabel(pacemaker_connection_frame, image=pacemaker_icon, text="")
        pacemaker_icon_label.image = pacemaker_icon  # Prevent garbage collection
        pacemaker_icon_label.pack(side="left")

        # Middle section: Date and Time
        self.date_time_label = ctk.CTkLabel(container_frame, text="", font=("Arial", 14), anchor="center")
        self.date_time_label.grid(row=0, column=1, padx=10, pady=10)

        # Right section: Battery Life
        battery_life_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        battery_life_frame.grid(row=0, column=2, padx=10, pady=10, sticky="e")  # Use a nested frame for label + icon

        # Battery Life Label
        battery_life = ctk.CTkLabel(battery_life_frame, text="Battery Life:", font=("Arial", 14))
        battery_life.pack(side="left", padx=5)

        # Load the Battery Icon
        battery_icon_path = "icons/battery.png"  # Path to the saved battery icon
        battery_image = Image.open(battery_icon_path).resize((20, 20))  # Resize as needed
        battery_icon = ImageTk.PhotoImage(battery_image)

        # Battery Icon Label
        battery_icon_label = ctk.CTkLabel(battery_life_frame, image=battery_icon, text="")
        battery_icon_label.image = battery_icon  # Prevent garbage collection
        battery_icon_label.pack(side="left")

        # Start updating the time
        self.update_time()



    def update_time(self):
        if self.date_time_label.winfo_exists():
            formatted_datetime = datetime.now().strftime("%Y-%m-%d - %H:%M:%S")
            self.date_time_label.configure(text=f"{formatted_datetime}")
            self.master.after(1000, self.update_time)  # Schedule the next update

   
    def create_widgets(self):

        container_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        container_frame.pack(fill="both", expand=True)
        # Setting up the Grid Layout
        container_frame.columnconfigure((0, 1), weight=1)
        container_frame.columnconfigure((2, 3), weight=4)
        container_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        #setting up graph area
        # Create a canvas widget to display the matplotlib figure within the tkinter frame.
        self.electrogram_frame = ctk.CTkScrollableFrame(container_frame)
        self.electrogram_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Create the canvas for the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.electrogram_frame)
        
        # Attach the canvas to the tkinter grid, center it within the frame with padding.
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Frame for editing parameters
        self.edit_frame = ctk.CTkScrollableFrame(container_frame)
        self.edit_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew")
        
         
        #Setting up the rest of the area

        select_mode_label = ctk.CTkLabel(container_frame, text="Select Mode", font=("Arial", 16, "bold")) # Create a label for selecting pacemaker modes.
        select_mode_label.grid(row=0, column=0, pady=1, padx=10, sticky="sw") # Place the mode label in the grid.

        pacemaker_state_options = ["AOO", "VOO", "AAI", "VVI", "AOOR", "VOOR", "AAIR", "VVIR"] # Define the options for pacemaker modes (AOO, VOO, AAI, VVI)
        self.initial_state = tk.StringVar(value="AOO")  # Initialize the pacemaker mode variable with a default value of "AOO".
        pacemaker_state_optionmenu = ctk.CTkOptionMenu(container_frame, values=pacemaker_state_options, variable=self.initial_state, command=self.update_edit_frame) # Create an option menu for selecting the pacemaker mode.
        pacemaker_state_optionmenu.grid(row=1, column=0, sticky="new", pady=1, padx=(10, 1)) # Place the option menu in the grid.

        # Segmented Button for Show Electrogram and Edit Parameters
        self.segmented_button = ctk.CTkSegmentedButton(container_frame, values=["Edit Parameters", "Show Electrogram"], command=self.segment_button_callback, font=("Arial", 16, "bold")) # Create a segmented button with two options
        self.segmented_button.grid(row=2, column=0, sticky="nesw", pady=1, padx=(10, 1))  # Place the segmented button in the grid
        self.segmented_button.set("Edit Parameters") # Set the default selection to "Edit Parameters"

        edit_data_button = ctk.CTkButton(container_frame, text="Save Data", command=self.update_user_data_check, font=("Arial", 22, "bold")) # Create a button to export data
        edit_data_button.grid(row=3, column=0, sticky="nesw", pady=1, padx=(10, 1))
        self.edit_data_button = edit_data_button # Store the reference to the button in self.edit_data_button for later use
        self.edit_data_button.configure(state="disabled") # Disable the edit data button
            
        # Admin Mode Toggle Button
        self.admin_mode = tk.BooleanVar(value=False) # Initialize a Boolean variable to track the state of admin mode (OFF by default)
        admin_mode_button = ctk.CTkButton(container_frame, text="Admin Mode: OFF", command=self.toggle_admin_mode, font=("Arial", 22, "bold")) # Create a button labeled "Admin Mode: OFF" that calls toggle_admin_mode when clicked
        admin_mode_button.grid(row=4, column=0, sticky="nesw", pady=1, padx=(10, 1)) # Place the button in the grid layout at row 8, column 0, spanning 2 columns with padding
        self.admin_mode_button = admin_mode_button # Store the reference to the button in self.admin_mode_button for later use

        logout_button = ctk.CTkButton(container_frame, text="Logout", command=self.app.open_login_page, font=("Arial", 22, "bold")) # Create a button to log out
        logout_button.grid(row=7, column=0, sticky="nesw", pady=1, padx=(10, 1))

        delete_user_button = ctk.CTkButton(container_frame, text="Delete User", command=self.delete_current_user_check, font=("Arial", 22, "bold")) # Create a button to delete the current user
        delete_user_button.grid(row=8, column=0, sticky="nesw", pady=(1,10), padx=(10, 1))
        self.delete_user_button = delete_user_button # Store the reference to the button in self.delete_user_button for later use
        self.delete_user_button.configure(state="disabled")
        

        # Initialize by hiding the electrogram frame
        self.electrogram_frame.grid_forget()
        self.show_edit_frame() 


    def toggle_admin_mode(self):
        if not self.admin_mode.get():  # Admin Mode is OFF, prompt for a password
            # Create a popup frame and store it as an instance attribute
            self.popup_frame = ctk.CTkFrame(self.master, corner_radius=10)  
            self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
            
            # Create the label, entry, and submit button inside the popup frame
            self.admin_label = ctk.CTkLabel(self.popup_frame, text="Enter Admin Password:", font=("Arial", 16, "bold"))  
            self.admin_label.pack(pady=10, padx=15)  # Add padding to the label
            
            self.admin_password_entry = ctk.CTkEntry(self.popup_frame, show="*", font=("Arial", 16))  
            self.admin_password_entry.pack(pady=10)  # Add padding to the entry field
            
            self.submit_button = ctk.CTkButton(
                self.popup_frame, 
                text="Submit", 
                command=self.check_admin_password, 
                font=("Arial", 16, "bold")
            )  
            self.submit_button.pack(pady=10)  # Add padding to the submit button
        else:
            # Incorrect password: disable admin mode and show an error message
            self.admin_mode.set(False)
            self.admin_mode_button.configure(text="Admin Mode: OFF")
            self.edit_data_button.configure(state="disabled")
            self.delete_user_button.configure(state="disabled")
            self.update_edit_frame(self.initial_state.get())

    def check_admin_password(self):
        # Get the entered password
        entered_password = self.admin_password_entry.get()  
        
        # Validate the entered password
        if entered_password == "1234":  # Replace with a secure password
            # Correct password: enable admin mode
            self.admin_mode.set(True)
            self.admin_mode_button.configure(text="Admin Mode: ON")
            self.edit_data_button.configure(state="normal")
            self.delete_user_button.configure(state="normal")
            # Destroy the popup frame and its contents
            self.popup_frame.destroy()
            self.correct_password = ctk.CTkLabel(self.master, text="Correct Password", font=("Arial", 16, "bold"), text_color="green")
            self.correct_password.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
            self.master.after(3000, lambda: self.correct_password.destroy())
        else:
            # Incorrect password: disable admin mode and show an error message
            self.admin_mode.set(False)
            self.admin_mode_button.configure(text="Admin Mode: OFF")
            self.edit_data_button.configure(state="disabled")
            self.delete_user_button.configure(state="disabled")
            # Destroy the popup frame and its contents
            self.popup_frame.destroy()
            self.incorrect_password = ctk.CTkLabel(self.master, text="Incorrect Password", font=("Arial", 16, "bold"), text_color="red")
            self.incorrect_password.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
            self.master.after(3000, lambda: self.incorrect_password.destroy())
            
        
        

        # Update the frame with the new admin state
        self.update_edit_frame(self.initial_state.get())
    
    def delete_current_user_check(self):
         # Create a popup frame and store it as an instance attribute
        self.popup_frame = ctk.CTkFrame(self.master, corner_radius=10)  
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
        # Create BooleanVar for checkboxes
        self.checkbox1_var = ctk.BooleanVar()
        self.checkbox2_var = ctk.BooleanVar()
        self.check = ctk.CTkLabel(self.popup_frame, text="Are you sure you want to delete this account?", font=("Arial", 16, "bold"))
        self.check.pack(pady=10, padx=10)
        # Create checkboxes
        self.checkbox1 = ctk.CTkCheckBox(self.popup_frame, text="Yes", variable=self.checkbox1_var, command=self.delete_current_user)
        self.checkbox1.pack(side="left", pady=10, padx=(50, 10))

        self.checkbox2 = ctk.CTkCheckBox(self.popup_frame, text="No", variable=self.checkbox2_var, command=self.delete_current_user)
        self.checkbox2.pack(side="right", pady=10, padx=10)

    def delete_current_user(self):
        if self.checkbox1_var.get() and not self.checkbox2_var.get():
            self.popup_frame.destroy()
            current_user = self.username  # Get the username of the current user
            self.user_manager.delete_user(current_user)  # Delete the current user
            self.app.open_login_page()  # Open the login page after deleting the user
        else:
            self.popup_frame.destroy()

    def reset_plot(self):
        self.y_values.clear()  # Clear existing y-values
        self.x_values.clear()  # Clear existing x-values
        self.y_values.extend([0] * 30)  # Reset y-values to 30 zeros
        self.x_values.extend(range(0, 3000, 100))  # Reset x-values from 0 to 3000, with increments of 100

        # Update the line data
        self.line.set_ydata(self.y_values) # Set the y-data of the plot line to the new y-values
        self.line.set_xdata(self.x_values) # Set the x-data of the plot line to the new x-values

        # Reset axis limits
        self.ax.set_xlim(0, 3000) # Show x-axis limits
        self.ax.set_ylim(0, 1) # Show y-axis limits

        # Redraw the canvas
        self.canvas.draw()

    def segment_button_callback(self, value): 
        if value == "Show Electrogram":
            self.reset_plot() # Reset the plot when electrogram is shown
            self.show_electrogram() # Call the function to show the electrogram frame
            
        elif value == "Edit Parameters":
            self.show_edit_frame() # Call the function to show the parameter editing frame

    def show_electrogram(self):
        # Hide edit frame and show electrogram frame
        self.edit_frame.grid_forget() # Remove the edit frame from the grid layout (not destroyed, just hidden)

        # Display electrogram frame with the plot
        self.electrogram_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew") # Show the electrogram plot frame in a specific grid position
        self.update_plot() # Call the function to update the plot with new values or refreshed data

    def update_plot(self):
        # Generate a new random y-value between 0 and 1
        new_y_value = random.uniform(0, 1)

        # Update the y_values deque
        self.y_values.append(new_y_value)

        # Shift the x-values to create a moving window effect
        new_x_value = self.x_values[-1] + 100  # Increment the last x-value by 100 ms
        self.x_values.append(new_x_value) # Append the new x-value to the x_values deque

        # Update the plot data with the new x and y values
        self.line.set_ydata(self.y_values) # Update the y-data of the plot line
        self.line.set_xdata(self.x_values) # Update the x-data of the plot line

        # Set x-axis limits to show the last 3000 ms of data
        self.ax.set_xlim(max(0, new_x_value - 3000), new_x_value)  # Adjust x-limits to show last 3000 ms
        self.ax.set_ylim(0, 1)  # Set Y-axis range

        # Redraw the canvas with the updated plot
        self.canvas.draw()

        # Schedule the next update after 200 ms
        self.master.after(200, self.update_plot)
    
    def show_edit_frame(self):
        # Hide the electrogram frame to make the edit frame visible
        self.electrogram_frame.grid_forget()

        # Display the edit frame in the specified grid position with padding
        self.edit_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Clear existing widgets in the edit frame before adding new ones (optional for cleanliness)
        for widget in self.edit_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame

        self.update_edit_frame(self.initial_state.get())

    def update_edit_frame(self, mode):
        # Clear existing widgets in the edit frame before adding new ones (optional for cleanliness)
        for widget in self.edit_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame (to avoid duplication or clutter)

        username_data = self.user_manager.read_user(self.username)
        if mode not in username_data:
            username_data[mode] = {}

        # Define the variables and their values based on the selected mode
        if mode == "AOO":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AOO"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AOO"]["Upper Rate Limit"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AOO"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AOO"]["Atrial Pulse Width"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Atrial Amplitude", 0.5, 5.0, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1)
            ]
            

        elif mode == "VOO":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VOO"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VOO"]["Upper Rate Limit"])
            self.ventricular_amplitude = tk.DoubleVar(value=username_data["VOO"]["Ventricular Amplitude"])
            self.ventricular_pulse_width = tk.DoubleVar(value=username_data["VOO"]["Ventricular Pulse Width"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Ventricular Amplitude", 0.5, 5.0, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
            ]
            

        elif mode == "AAI":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AAI"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AAI"]["Upper Rate Limit"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AAI"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AAI"]["Atrial Pulse Width"])

            self.atrial_sensitivity = tk.DoubleVar(value=username_data["AAI"]["Atrial Sensitivity"]) 
            self.arp = tk.DoubleVar(value=username_data["AAI"]["ARP"]) 
            self.hysteresis = tk.DoubleVar(value=username_data["AAI"]["Hysteresis"])  
            self.rate_smoothing = tk.DoubleVar(value=username_data["AAI"]["Rate Smoothing"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Atrial Amplitude", 0.5, 5.0, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1),
                ("Atrial Sensitivity", 0, 5.0, self.atrial_sensitivity, 0.5),
                ("ARP", 100, 500, self.arp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3)
            ]
            
        elif mode == "VVI":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VVI"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VVI"]["Upper Rate Limit"])
            self.ventricular_amplitude = tk.DoubleVar(value=username_data["VVI"]["Ventricular Amplitude"])
            self.ventricular_pulse_width = tk.DoubleVar(value=username_data["VVI"]["Ventricular Pulse Width"])
            self.ventrical_sensitivity = tk.DoubleVar(value=username_data["VVI"]["Ventricular Sensitivity"]) 
            self.vrp = tk.DoubleVar(value=username_data["VVI"]["VRP"])  
            self.hysteresis = tk.DoubleVar(value=username_data["VVI"]["Hysteresis"])  
            self.rate_smoothing = tk.DoubleVar(value=username_data["VVI"]["Rate Smoothing"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Ventricular Amplitude", 0.5, 5.0, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
                ("Ventrical Sensitivity", 0, 5.0, self.ventrical_sensitivity, 0.5),
                ("VRP", 100, 500, self.vrp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3)
            ]
        elif mode == "AOOR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AOOR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AOOR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["AOOR"]["Max Sensor Rate"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AOOR"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AOOR"]["Atrial Pulse Width"])
            self.activity_threshold = tk.DoubleVar(value=username_data["AOOR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["AOOR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["AOOR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["AOOR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Atrial Amplitude", 0.5, 5.0, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1),
                ("Activity Threshold", 0, 5.0, self.activity_threshold, 0.5),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
            ]
        elif mode == "VOOR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VOOR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VOOR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["VOOR"]["Max Sensor Rate"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["VOOR"]["Ventricular Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["VOOR"]["Ventricular Pulse Width"])
            self.activity_threshold = tk.DoubleVar(value=username_data["VOOR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["VOOR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["VOOR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["VOOR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Ventricular Amplitude", 0.5, 5.0, self.atrial_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.atrial_pulse_width, 1),
                ("Activity Threshold", 0, 5.0, self.activity_threshold, 0.5),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
            ]
        elif mode == "AAIR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AAIR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AAIR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["AAIR"]["Max Sensor Rate"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AAIR"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AAIR"]["Atrial Pulse Width"])
            self.atrial_sensitivity = tk.DoubleVar(value=username_data["AAIR"]["Atrial Sensitivity"]) 
            self.arp = tk.DoubleVar(value=username_data["AAIR"]["ARP"]) 
            self.pvarp = tk.DoubleVar(value=username_data["AAIR"]["PVARP"])
            self.hysteresis = tk.DoubleVar(value=username_data["AAIR"]["Hysteresis"])  
            self.rate_smoothing = tk.DoubleVar(value=username_data["AAIR"]["Rate Smoothing"])
            self.activity_threshold = tk.DoubleVar(value=username_data["AAIR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["AAIR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["AAIR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["AAIR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Atrial Amplitude", 0.5, 5.0, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1),
                ("Atrial Sensitivity", 0, 5.0, self.atrial_sensitivity, 0.5),
                ("ARP", 100, 500, self.arp, 10),
                ("PVARP", 150, 500, self.pvarp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3),
                ("Activity Threshold", 0, 5.0, self.activity_threshold, 0.5),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
            ]
        elif mode == "VVIR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VVIR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VVIR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["VVIR"]["Max Sensor Rate"])
            self.ventricular_amplitude = tk.DoubleVar(value=username_data["VVIR"]["Ventricular Amplitude"])
            self.ventricular_pulse_width = tk.DoubleVar(value=username_data["VVIR"]["Ventricular Pulse Width"])
            self.ventricular_sensitivity = tk.DoubleVar(value=username_data["VVIR"]["Ventricular Sensitivity"])
            self.vrp = tk.DoubleVar(value=username_data["VVIR"]["VRP"])
            self.hysteresis = tk.DoubleVar(value=username_data["VVIR"]["Hysteresis"])
            self.rate_smoothing = tk.DoubleVar(value=username_data["VVIR"]["Rate Smoothing"])
            self.activity_threshold = tk.DoubleVar(value=username_data["VVIR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["VVIR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["VVIR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["VVIR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Ventricular Amplitude", 0.5, 5.0, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
                ("Ventricular Sensitivity", 0, 5.0, self.ventricular_sensitivity, 0.5),
                ("VRP", 100, 500, self.vrp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3),
                ("Activity Threshold", 0, 5.0, self.activity_threshold, 0.5),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
            ]
            
        else:
            variables = []

        # Loop through the variable definitions to create labels and sliders
        for label, min_val, max_val, var, increment in variables:
            # Create and pack the label for the slider
            input_label = ctk.CTkLabel(self.edit_frame, text=f"{label}: {var.get()}")
            input_label.pack(pady=2, padx=2, anchor="w")

            # Calculate the number of steps based on the increment
            num_steps = int((max_val - min_val) / increment)

            # Create and pack the slider with specified range, default value, and steps
            slider = ctk.CTkSlider(self.edit_frame, from_=min_val, to=max_val, number_of_steps=num_steps, variable=var)
            slider.pack(pady=2, padx=2, fill="x")

            # Bind the slider movement event to update the label with the current slider value
            slider.bind("<B1-Motion>", lambda event, lbl=input_label, lbl_text=label, sldr=slider: self.update_label_and_print(lbl, lbl_text, sldr))

            # Disable the slider if admin mode is off
            if not self.admin_mode.get():
                slider.configure(state="disabled")

    def update_label_and_print(self, label, label_text, slider):
        label.configure(text=f"{label_text}: {slider.get():.1f}")  # Update the label text with the slider's current value, formatted to one decimal place

    def update_user_data_check(self):
         # Create a popup frame and store it as an instance attribute
        self.popup_frame = ctk.CTkFrame(self.master, corner_radius=10)  
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
        # Create BooleanVar for checkboxes
        self.checkbox1_var = ctk.BooleanVar()
        self.checkbox2_var = ctk.BooleanVar()
        self.check = ctk.CTkLabel(self.popup_frame, text="Are you sure you want to save the data?", font=("Arial", 16, "bold"))
        self.check.pack(pady=10, padx=10)
        # Create checkboxes
        self.checkbox1 = ctk.CTkCheckBox(self.popup_frame, text="Yes", variable=self.checkbox1_var, command=self.update_user_data)
        self.checkbox1.pack(side="left", pady=10, padx=(50, 10))

        self.checkbox2 = ctk.CTkCheckBox(self.popup_frame, text="No", variable=self.checkbox2_var, command=self.update_user_data)
        self.checkbox2.pack(side="right", pady=10, padx=10)

    def update_user_data(self):
        if self.checkbox1_var.get() and not self.checkbox2_var.get():
            self.popup_frame.destroy()
            username_data = self.user_manager.read_user(self.username)
            if self.initial_state.get() == "AOO":
                username_data["AOO"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AOO"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AOO"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AOO"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()

            elif self.initial_state.get() == "VOO":
                username_data["VOO"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VOO"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VOO"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VOO"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()

            elif self.initial_state.get() == "AAI":
                username_data["AAI"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AAI"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AAI"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AAI"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()
                username_data["AAI"]["Atrial Sensitivity"] = self.atrial_sensitivity.get()
                username_data["AAI"]["ARP"] = self.arp.get()
                username_data["AAI"]["Hysteresis"] = self.hysteresis.get()
                username_data["AAI"]["Rate Smoothing"] = self.rate_smoothing.get()

            elif self.initial_state.get() == "VVI":
                username_data["VVI"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VVI"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VVI"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VVI"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()
                username_data["VVI"]["Ventricular Sensitivity"] = self.ventrical_sensitivity.get()
                username_data["VVI"]["VRP"] = self.vrp.get()
                username_data["VVI"]["Hysteresis"] = self.hysteresis.get()

            elif self.initial_state.get() == "AOOR":
                username_data["AOOR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AOOR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AOOR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["AOOR"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AOOR"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()
                username_data["AOOR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["AOOR"]["Reaction Time"] = self.reaction_time.get()
                username_data["AOOR"]["Response Factor"] = self.response_factor.get()
                username_data["AOOR"]["Recovery Time"] = self.recovery_time.get()
            elif self.initial_state.get() == "VOOR":
                username_data["VOOR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VOOR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VOOR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["VOOR"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VOOR"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()
                username_data["VOOR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["VOOR"]["Reaction Time"] = self.reaction_time.get()
                username_data["VOOR"]["Response Factor"] = self.response_factor.get()
                username_data["VOOR"]["Recovery Time"] = self.recovery_time.get()
            elif self.initial_state.get() == "AAIR":
                username_data["AAIR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AAIR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AAIR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["AAIR"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AAIR"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()
                username_data["AAIR"]["Atrial Sensitivity"] = self.atrial_sensitivity.get()
                username_data["AAIR"]["ARP"] = self.arp.get()
                username_data["AAIR"]["PVARP"] = self.pvarp.get()
                username_data["AAIR"]["Hysteresis"] = self.hysteresis.get()
                username_data["AAIR"]["Rate Smoothing"] = self.rate_smoothing.get()
                username_data["AAIR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["AAIR"]["Reaction Time"] = self.reaction_time.get()
                username_data["AAIR"]["Response Factor"] = self.response_factor.get()
                username_data["AAIR"]["Recovery Time"] = self.recovery_time.get()
            elif self.initial_state.get() == "VVIR":
                username_data["VVIR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VVIR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VVIR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["VVIR"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VVIR"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()
                username_data["VVIR"]["Ventricular Sensitivity"] = self.ventricular_sensitivity.get()
                username_data["VVIR"]["VRP"] = self.vrp.get()
                username_data["VVIR"]["Hysteresis"] = self.hysteresis.get()
                username_data["VVIR"]["Rate Smoothing"] = self.rate_smoothing.get()
                username_data["VVIR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["VVIR"]["Reaction Time"] = self.reaction_time.get()
                username_data["VVIR"]["Response Factor"] = self.response_factor.get()
                username_data["VVIR"]["Recovery Time"] = self.recovery_time.get()
                
            username_data["password"] = self.user_manager._encrypt_password(username_data["password"])
            self.user_manager.update_user_data(self.username, username_data)
        else:
            self.popup_frame.destroy()
       
class App:
    def __init__(self, root):
        self.root = root  # Store the root window (Tkinter root) in self.root
        self.root.geometry("1100x700")  # Set the initial size of the window
        self.user_manager = UserManager("users")  # Initialize the UserManager class, providing the user data file path
        self.root.configure(bg="#333333")
        # Initialize the page variables as None (they will hold references to page instances)
        self.login_page = None  
        self.create_user_page = None
        self.main_page = None

        self.open_login_page()  # Open the login page as the default page when the app starts
        #self.open_main_page("aidan")  # Open the main page as the default page when the app starts
    def open_login_page(self, success_message=False):
        self.clear_page()  # Clear any existing widgets from the root window
        self.login_page = LoginPage(self.root, self.user_manager, self, success_message)  # Initialize and display the LoginPage, passing the root, user manager, app instance, and optional success message

    def open_create_user_page(self):
        self.clear_page()  # Clear any existing widgets from the root window
        self.create_user_page = CreateUserPage(self.root, self.user_manager, self)  # Initialize and display the CreateUserPage, passing the root, user manager, and app instance

    def open_main_page(self, username):
        self.clear_page()  # Clear any existing widgets from the root window
        # Initialize and display the MainPage, passing the root, app instance, username, and user manager
        self.main_page = MainPage(self.root, self, username, self.user_manager)  # Pass the username to the main page so it can be used in the main interface

    def clear_page(self):
        # Destroy all widgets (clear the entire root window) to ensure a fresh page is loaded
        for widget in self.root.winfo_children():  # Iterate over all child widgets in the root window
            widget.destroy()  # Destroy each widget, effectively clearing the page

if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter root window
    app = App(root)  # Instantiate the App class, passing the root window as an argument
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue") 
    root.mainloop()  # Start the Tkinter event loop, which keeps the app running and responsive
    