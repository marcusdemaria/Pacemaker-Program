from multiprocessing import connection  # Import the connection module from the multiprocessing library for handling inter-process communication
from pdb import run  # Import the run function from the pdb (Python Debugger) module to facilitate debugging
from tracemalloc import stop  # Import the stop function from tracemalloc to stop memory tracking
import customtkinter as ctk  # Import the CustomTkinter library, which provides custom themed widgets for Tkinter, as 'ctk'
import tkinter as tk  # Import the standard Tkinter library for creating GUI applications, as 'tk'
import os  # Import the os module for interacting with the operating system (file and directory management)
import random  # Import the random module to generate random numbers
from collections import deque  # Import deque from collections for creating a double-ended queue, useful for managing a sequence of items
from PIL import Image, ImageTk  # Import the Image and ImageTk classes from the Pillow library for image processing and display
from matplotlib.figure import Figure  # Import the Figure class from matplotlib for creating figures for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import the FigureCanvasTkAgg class to integrate Matplotlib figures into Tkinter
from datetime import datetime  # Import the datetime class to handle date and time operations
import time  # Import the time module for time-related functions (e.g., sleep)
import serial.tools.list_ports  # Import the list_ports module from serial.tools to list available serial ports
from cryptography.fernet import Fernet  # Import the Fernet class from the cryptography library for secure encryption and decryption, particularly for handling passwords

USER_DATA_FILE = "users.txt" # Reference file for handling user data

class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path # Path to the file that stores user data
        self.key = self._get_or_generate_key() # Generate a key for encryption/decryption, fetching keys, and retrieval of existing key
        self.cipher = Fernet(self.key) # In a production setting, this key should be stored securely and not regenerated every time

    def _get_or_generate_key(self):
        # Name of the file where the encryption key is stored
        key_file = "secret.key"
        
        # If the key file already exists, read and return the key
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:  # Open the key file in binary read mode
                return f.read()  # Return the key

        # If the key file doesn't exist, generate a new key
        else:
            key = Fernet.generate_key()  # Generate a new encryption key
            with open(key_file, "wb") as f:  # Save the key in binary write mode
                f.write(key)  # Write the generated key to the file
            return key  # Return the newly generated key

    def _encrypt_password(self, password):
        """Encrypt the password."""
        return self.cipher.encrypt(password.encode()).decode() # Use the cipher to encrypt the password, then decode to store as text

    def _decrypt_password(self, encrypted_password):
        """Decrypt the password."""
        return self.cipher.decrypt(encrypted_password.encode()).decode() # Use the cipher to decrypt the password (which was stored as text)

    def read_users(self):
        if not os.path.exists(self.file_path):  # If the file does not exist, return an empty dictionary (no users stored)
            return {}

        # Open the file in read mode to load user data
        with open(self.file_path, "r") as file:
            users = {}  # Dictionary to store users
            # Read each line of the file (username:encrypted_password format)
            for line in file:
                username, encrypted_password = line.strip().split(":")  # Split into username and password
                decrypted_password = self._decrypt_password(encrypted_password)  # Decrypt the password
                users[username] = decrypted_password  # Store username and decrypted password in the dictionary
            return users  # Return the dictionary of users

    def save_user(self, username, password):
        encrypted_password = self._encrypt_password(password) # Encrypt the password before saving it
        with open(self.file_path, "a") as file: # Open the file in append mode to add the new user
            file.write(f"{username}:{encrypted_password}\n") # Write the username and encrypted password to the file

class LoginPage:
    def __init__(self, master, user_manager, app, success_message=False):  # Initialize the login page
        self.master = master # The main window that contains everything
        self.user_manager = user_manager # UserManager instance to handle user data
        self.app = app  # Store the app reference to the main application
        self.success_message = success_message  # Whether to show a success message
        self.create_widgets()  #Call the function to create the interface elements

    def create_widgets(self):
        # Create a frame to contain the login form
        container_frame = ctk.CTkFrame(self.master)
        container_frame.pack(fill="both", expand=True) # Make it expand to fill the window

        # Configure grid for the container_frame to manage resizing
        container_frame.columnconfigure(0, weight=1)
        container_frame.rowconfigure(0, weight=1) # For login label
        container_frame.rowconfigure(1, weight=1) # For username entry
        container_frame.rowconfigure(2, weight=1) # For password entry
        container_frame.rowconfigure(3, weight=1) # For login button
        container_frame.rowconfigure(4, weight=1) # For exit button

        # Create a frame to center the login form
        center_frame = ctk.CTkFrame(container_frame)
        center_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Login label (header) with custom font size
        login_label = ctk.CTkLabel(center_frame, text="Welcome to the LeTron James PACEMAKER Login Page!!", font=("Arial", 24))
        login_label.pack(pady=(20, 10), padx=10, fill="both")

        # Username label
        username_label = ctk.CTkLabel(center_frame, text="Username:", font=("Arial", 18))
        username_label.pack(pady=(5, 2))

        # Entry box for the username (adjusted height and width)
        self.username_entry = ctk.CTkEntry(center_frame, height=40, width=300, font=("Arial", 18))
        self.username_entry.pack(pady=10)

        # Password label
        password_label = ctk.CTkLabel(center_frame, text="Password:", font=("Arial", 18))
        password_label.pack(pady=(5, 2))

        # Entry box for the password (shows '*' instead of actual characters)
        self.password_entry = ctk.CTkEntry(center_frame, show="*", height=40, width=300, font=("Arial", 18))
        self.password_entry.pack(pady=10)

        # Label to show error messages if login fails (initially empty)
        self.login_error_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent", font=("Arial", 16))
        self.login_error_label.pack(pady=(5, 2))

        # If a user was successfully created, display a success message
        if self.success_message:
            success_label = ctk.CTkLabel(center_frame, text="User successfully created!", fg_color="green", font=("Arial", 16))
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

        # Exit button, positioned at the bottom of the window
        exit_button = ctk.CTkButton(container_frame, text="Exit", command=self.master.destroy, fg_color="red", hover_color="#bd1809")
        exit_button.grid(row=4, column=0, pady=(10, 20))  # At the bottom row
        
    def handle_login(self):
        # Get the username and password from the entry boxes entered by user
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Call the login function to check if credentials are correct
        self.login(username, password)

    def login(self, username, password):
        users = self.user_manager.read_users() # Read the list of users from the file
        self.login_error_label.configure(text="") # Clear any previous error messages

        if username in users and users[username] == password: # If the username and password match what's stored
            self.app.open_main_page(username)  # Pass the username to open_main_page, and open the main page
        else:
            # Show an error message if login fails
            self.login_error_label.configure(text="", fg_color="transparent")
            self.master.after(100, lambda: self.login_error_label.configure(text="Incorrect username or password.", fg_color="red"))
            # Clear the input fields after an unsuccessful login
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_create_user_page(self):
        self.app.open_create_user_page() # Open the page to create a new user

class CreateUserPage:
    def __init__(self, master, user_manager, app): # Initialize the create user page
        self.master = master  # Reference to the main window (the parent window)
        self.user_manager = user_manager  # Reference to the user manager for saving and reading user data
        self.app = app  # Reference to the main application
        self.create_widgets()  # Call the function to create the interface elements

    def create_widgets(self):
        # Create a frame that will fill the window screen
        container_frame = ctk.CTkFrame(self.master)
        container_frame.pack(fill="both", expand=True) # Make it expand to fill the screen

        # Configure a grid system inside the container for proper resizing
        container_frame.columnconfigure(0, weight=1)  # Allow column to stretch
        container_frame.rowconfigure(0, weight=1)  # For title
        container_frame.rowconfigure(1, weight=1)  # For username label
        container_frame.rowconfigure(2, weight=1)  # For password label
        container_frame.rowconfigure(3, weight=1)  # For error label
        container_frame.rowconfigure(4, weight=1)  # For buttons
        container_frame.rowconfigure(5, weight=1)  # For the exit button

        # Center Frame to contain the create user form
        center_frame = ctk.CTkFrame(container_frame)
        center_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew") # Positioned at the center

        # Label for the create user page
        create_user_label = ctk.CTkLabel(center_frame, text="Create a New User", font=("Arial", 24))
        create_user_label.pack(pady=(20, 10), padx=10, fill="both") # Add padding and fill horizontally

        # Label for the new username input
        new_username_label = ctk.CTkLabel(center_frame, text="New Username:", font=("Arial", 18))
        new_username_label.pack(pady=(5, 2))

        # Entry box for the new username (with increased size)
        self.new_username_entry = ctk.CTkEntry(center_frame, height=40, width=300, font=("Arial", 18))  # Increased size
        self.new_username_entry.pack(pady=10) # Add padding around the entry field

        # New Password label and entry
        new_password_label = ctk.CTkLabel(center_frame, text="New Password:", font=("Arial", 18))
        new_password_label.pack(pady=(5, 2)) # Add padding between label and entry field

        # Entry box for the new password (hidden characters with '*')
        self.new_password_entry = ctk.CTkEntry(center_frame, show="*", height=40, width=300, font=("Arial", 18))  # Password hidden
        self.new_password_entry.pack(pady=10)  # Add padding around the entry field

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

        # Exit button at the bottom to close the window
        exit_button = ctk.CTkButton(container_frame, text="Exit", command=self.master.destroy, fg_color="red", hover_color="#bd1809")
        exit_button.grid(row=5, column=0, pady=(10, 20))  # Position the exit button at the bottom

    def handle_create_user(self):
        # Retrieve the new username and password from the entry fields
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        users = self.user_manager.read_users() # Read the current users from the file

        if new_username in users: # Check if the username already exists
            self.show_error("Error: Username already exists! Choose a different one.")
        elif len(users) >= 10: # Check if the maximum number of users has been reached
            self.show_error("Error: Max Number of users reached.") 
        elif " " in new_username or ":" in new_username or " " in new_password or ":" in new_password: # Check for spaces or colons in the username or password
            self.show_error("Error: Usernames and passwords cannot contain spaces or colons.")
        elif "" == new_username or "" == new_password: # Check if the username or password is empty
            self.show_error("Must create both a username and password.")
        else: # If all checks pass, save the new user
            self.user_manager.save_user(new_username, new_password) # Save the new user in the file
            self.app.open_login_page(success_message=True)  # Show success message on login page and return to it

    def show_error(self, message):
        self.create_user_error_label.configure(text="", fg_color="transparent") # Clear any previous error messages
        self.master.after(100, lambda: self.create_user_error_label.configure(text=message, fg_color="red")) # After 100 ms, show the error message
        self.new_username_entry.delete(0, tk.END) # Clear the new username entry field
        self.new_password_entry.delete(0, tk.END) # Clear the new password entry field

class MainPage:
    def __init__(self, master, app, username, user_manager): # Initialize the main page
        self.master = master # Reference to the main window
        self.app = app # Reference to the main application
        self.username = username # Store the username for the current user
        self.create_widgets() # Call the function to create the interface elements
        self.user_manager = user_manager  # Ensure user_manager is passed to the main page
        self.y_values = deque([0] * 30, maxlen=30)  # Y-axis values for the plot
        self.x_values = deque(range(0, 3000, 100), maxlen=30)  # X-axis values for the plot

        # Create a figure and axis for the plot
        self.fig = Figure(figsize=(3, 3), dpi=100)  # Adjust size for better visibility
        self.ax = self.fig.add_subplot(111)

        # Label the graph
        self.ax.set_title("Electrogram")  # Set the title of the plot
        self.ax.set_xlabel("Time (ms)")   # Label for the x-axis
        self.ax.set_ylabel("Amplitude (V)")  # Label for the y-axis

        self.line, = self.ax.plot(self.x_values, self.y_values)  #Plot the initial x and y values (empty or default data)

        # Create a canvas widget to display the matplotlib figure within the tkinter frame.
        self.electrogram_frame = ctk.CTkFrame(self.master)
        self.electrogram_frame.grid(row=2, column=2, rowspan=8, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create the canvas for the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.electrogram_frame)
        
        # Attach the canvas to the tkinter grid, center it within the frame with padding.
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Configure grid for the electrogram frame to allow for padding
        self.electrogram_frame.columnconfigure(0, weight=1)
        self.electrogram_frame.rowconfigure(0, weight=1)

        # Initialize by hiding the electrogram frame
        self.electrogram_frame.grid_forget()
        self.show_edit_frame()

        # Microcontroller status label
        self.microcontroller_status_label = ctk.CTkLabel(self.master, text="Pacemaker Status: Checking...", font=("Arial", 16), fg_color="transparent")
        self.microcontroller_status_label.grid(row=1, column=3, pady=2)

        # Start checking for microcontroller connection
        self.check_microcontroller()

    def check_microcontroller(self):
        # Define a function to continuously check for connected serial ports (microcontroller).
        def check_ports():
            ports = serial.tools.list_ports.comports() # Get a list of all connected serial ports.
            # If any ports are found, update the status label to "Connected".
            if len(ports) > 0:
                if self.microcontroller_status_label.winfo_exists():
                    self.microcontroller_status_label.configure(text="Pacemaker Status: Connected", fg_color="transparent")
            else:
                # If no ports are found, update the status label to "Not Connected".
                if self.microcontroller_status_label.winfo_exists():
                    self.microcontroller_status_label.configure(text="Pacemaker Status: Not Connected", fg_color="transparent")
            self.master.after(1000, check_ports) # Check again after 1 second (1000 ms).
        check_ports() # Start the check_ports function for the first time.

    def create_widgets(self):
        # Setting up the Grid Layout
        self.master.columnconfigure((0, 1), weight=1)
        self.master.columnconfigure((2, 3), weight=2)
        self.master.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        formatted_datetime = datetime.now().strftime("%Y-%m-%d - %H:%M:%S") # Get the current date and time and format it as a string.
        date_time_label = ctk.CTkLabel(self.master, text=f"{formatted_datetime}", font=("Arial", 16)) # Create a label to display the date and time.
        date_time_label.grid(row=0, column=0, columnspan=2, pady=2) # Place the date-time label in the grid at the specified position.

        username_label = ctk.CTkLabel(self.master, text=f"Logged in as: {self.username}", font=("Arial", 16))  # Create a label that shows the username of the logged-in user.
        username_label.grid(row=0, column=3, columnspan=2, pady=2)  # Place the username label in the grid.

        select_mode_label = ctk.CTkLabel(self.master, text="Select Mode", font=("Arial", 16)) # Create a label for selecting pacemaker modes.
        select_mode_label.grid(row=1, column=0, columnspan=2, pady=2) # Place the mode label in the grid.

        pacemaker_state_options = ["AOO", "VOO", "AAI", "VVI"] # Define the options for pacemaker modes (AOO, VOO, AAI, VVI)
        self.initial_state = tk.StringVar(value="AOO")  # Initialize the pacemaker mode variable with a default value of "AOO".
        pacemaker_state_optionmenu = ctk.CTkOptionMenu(self.master, values=pacemaker_state_options, variable=self.initial_state, command=self.update_edit_frame) # Create an option menu for selecting the pacemaker mode.
        pacemaker_state_optionmenu.grid(row=2, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1)) # Place the option menu in the grid.

        # Segmented Button for Show Electrogram and Edit Parameters
        self.segmented_button = ctk.CTkSegmentedButton(self.master, values=["Edit Parameters", "Show Electrogram"], command=self.segment_button_callback)
        self.segmented_button.grid(row=3, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))  # Place the segmented button in the grid
        self.segmented_button.set("Edit Parameters") # Set the default selection to "Edit Parameters"

        edit_data_button = ctk.CTkButton(self.master, text="Export Data") # Create a button to export data
        edit_data_button.grid(row=4, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        send_data_button = ctk.CTkButton(self.master, text="Send to Pacemaker") # Create a button to send data to the pacemaker
        send_data_button.grid(row=5, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        logout_button = ctk.CTkButton(self.master, text="Logout", command=self.app.open_login_page) # Create a button to log out
        logout_button.grid(row=6, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        delete_user_button = ctk.CTkButton(self.master, text="Delete User", command=self.delete_current_user) # Create a button to delete the current user
        delete_user_button.grid(row=7, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        exit_button = ctk.CTkButton(self.master, text="Exit", command=self.master.destroy, fg_color="red", hover_color="#bd1809") # Create an exit button to close the app
        exit_button.grid(row=9, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        # Admin Mode Toggle Button
        self.admin_mode = tk.BooleanVar(value=False) # Initialize a Boolean variable to track the state of admin mode (OFF by default)
        admin_mode_button = ctk.CTkButton(self.master, text="Admin Mode: OFF", command=self.toggle_admin_mode) # Create a button labeled "Admin Mode: OFF" that calls toggle_admin_mode when clicked
        admin_mode_button.grid(row=8, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1)) # Place the button in the grid layout at row 8, column 0, spanning 2 columns with padding
        self.admin_mode_button = admin_mode_button # Store the reference to the button in self.admin_mode_button for later use

        # Frame for editing parameters
        self.edit_frame = ctk.CTkScrollableFrame(self.master)

        # Initialize variables for the sliders
        self.lower_rate_limit = tk.DoubleVar(value=60)
        self.upper_rate_limit = tk.DoubleVar(value=120)
        self.atrial_amplitude = tk.DoubleVar(value=3.5)
        self.atrial_pulse_width = tk.DoubleVar(value=1)
        self.ventricular_amplitude = tk.DoubleVar(value=3.5)
        self.ventricular_pulse_width = tk.DoubleVar(value=1)
        self.atrial_sensitivity = tk.DoubleVar(value=2.5) 
        self.ventrical_sensitivity = tk.DoubleVar(value=2.5) 
        self.arp = tk.DoubleVar(value=250) 
        self.vrp = tk.DoubleVar(value=250)  
        self.hysteresis = tk.DoubleVar(value=3.0)  
        self.rate_smoothing = tk.DoubleVar(value=12)  

    def toggle_admin_mode(self):
        self.admin_mode.set(not self.admin_mode.get()) # Change the admin_mode variable to its opposite value (toggle it)
        if self.admin_mode.get(): # Update the button text based on the new state of admin mode
            self.admin_mode_button.configure(text="Admin Mode: ON") # Change text of button to ON
        else:  # If admin mode is OFF
            self.admin_mode_button.configure(text="Admin Mode: OFF") # Change text of button to OFF
        self.update_edit_frame(self.initial_state.get())

    def delete_current_user(self):
        # Step 1: Read all users from the file
        users = self.user_manager.read_users()  # Get a dictionary of all users and their passwords
        # Step 2: Store the current user's username
        current_username = self.username  # Get the current user's username
        # Step 3: Check if the current user exists in the user list
        if current_username in users:  # If the current user's username is in the list of users
            # Step 4: Delete the current user from the users dictionary
            del users[current_username]  # Remove the current user from the dictionary
            # Step 5: Open the file in write mode and save the updated user list
            with open(self.user_manager.file_path, "w") as f:  # Open the user file in write mode
                for username, password in users.items():  # Iterate over the remaining users
                    # Re-encrypt each user's password before saving
                    encrypted_password = self.user_manager._encrypt_password(password)  # Encrypt the password
                    f.write(f"{username}:{encrypted_password}\n")  # Write the username and encrypted password to the file
        # Step 6: Return to the login page after deletion
        self.app.open_login_page()  # Open the login page after deleting the user

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
            self.show_electrogram() # Call the function to show the electrogram frame
            self.reset_plot() # Reset the plot when electrogram is shown
        elif value == "Edit Parameters":
            self.show_edit_frame() # Call the function to show the parameter editing frame

    def show_electrogram(self):
        # Hide edit frame and show electrogram frame
        self.edit_frame.grid_forget() # Remove the edit frame from the grid layout (not destroyed, just hidden)

        # Display electrogram frame with the plot
        self.electrogram_frame.grid(row=2, column=2, rowspan=8, columnspan=2, padx=10, pady=10, sticky="nsew") # Show the electrogram plot frame in a specific grid position
        self.update_plot() # Call the function to update the plot with new values or refreshed data

    def show_edit_frame(self):
        # Hide the electrogram frame to make the edit frame visible
        self.electrogram_frame.grid_forget()

        # Display the edit frame in the specified grid position with padding
        self.edit_frame.grid(row=2, column=2, rowspan=8, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Clear existing widgets in the edit frame before adding new ones (optional for cleanliness)
        for widget in self.edit_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame

        self.update_edit_frame(self.initial_state.get())

    def update_edit_frame(self, mode):
        # Clear existing widgets in the edit frame before adding new ones (optional for cleanliness)
        for widget in self.edit_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame (to avoid duplication or clutter)

        # Define the variables and their values based on the selected mode
        if mode == "AOO":
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Atrial Amplitude", 0.5, 5.0, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1)
            ]
        elif mode == "VOO":
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Ventricular Amplitude", 0.5, 5.0, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
            ]
        elif mode == "AAI":
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
        
class App:
    def __init__(self, root):
        self.root = root  # Store the root window (Tkinter root) in self.root
        self.user_manager = UserManager(USER_DATA_FILE)  # Initialize the UserManager class, providing the user data file path

        # Initialize the page variables as None (they will hold references to page instances)
        self.login_page = None  
        self.create_user_page = None
        self.main_page = None

        self.open_login_page()  # Open the login page as the default page when the app starts

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
    root.attributes('-fullscreen', True)  # Set the window to fullscreen mode when the app starts
    root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))  # Bind the Escape key to exit fullscreen mode
    root.mainloop()  # Start the Tkinter event loop, which keeps the app running and responsive