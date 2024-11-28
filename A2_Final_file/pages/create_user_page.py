# pages/create_user_page.py
import customtkinter as ctk
import tkinter as tk  # Import the standard Tkinter library for creating GUI applications, as 'tk'
from datetime import datetime  # Import the datetime module for working with dates and times
from PIL import Image, ImageTk  # Import the Python Imaging Library (PIL), now maintained as 'Pillow'
import os  # Import the os module for interacting with the operating system (file and directory management)

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
