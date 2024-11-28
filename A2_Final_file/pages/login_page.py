# pages/login_page.py
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import os


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
            pacemaker_icon_path = "A2_Final_file/icons/connected.png"
        else:
            pacemaker_icon_path = "A2_Final_file/icons/disconnected.png"  # Path to the saved pacemaker icon
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
        battery_icon_path = "A2_Final_file/icons/battery.png"  # Path to the saved battery icon
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
