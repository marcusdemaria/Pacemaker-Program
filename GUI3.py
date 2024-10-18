from multiprocessing import connection
from pdb import run
from tracemalloc import stop
import customtkinter as ctk
import tkinter as tk
import os
import random
from collections import deque
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

import colours

USER_DATA_FILE = "users.txt"

class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_users(self):
        if not os.path.exists(self.file_path):  # If the file does not exist, return an empty dictionary
            return {}

        with open(self.file_path, "r") as file:
            users = {}
            for line in file:
                username, password = line.strip().split(":")
                users[username] = password
            return users

    def save_user(self, username, password):
        with open(self.file_path, "a") as file:
            file.write(f"{username}:{password}\n")


class LoginPage:
    def __init__(self, master, user_manager, app):  # Added app argument
        self.master = master
        self.user_manager = user_manager
        self.app = app  # Store the app reference
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to contain the login form
        container_frame = ctk.CTkFrame(self.master)
        container_frame.pack(fill="both", expand=True)

        # Configure grid for the container_frame to manage resizing
        container_frame.columnconfigure(0, weight=1)
        container_frame.rowconfigure(0, weight=1)
        container_frame.rowconfigure(1, weight=1)
        container_frame.rowconfigure(2, weight=1)
        container_frame.rowconfigure(3, weight=1)
        container_frame.rowconfigure(4, weight=1)

        # Center Frame for the login form
        center_frame = ctk.CTkFrame(container_frame)
        center_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Resize and increase font size for labels, entry, and buttons
        login_label = ctk.CTkLabel(center_frame, text="Welcome to the LeTron James PACEMAKER Login Page!!", font=("Arial", 24))
        login_label.pack(pady=(20, 10), padx=10, fill="both")

        username_label = ctk.CTkLabel(center_frame, text="Username:", font=("Arial", 18))
        username_label.pack(pady=(5, 2))

        self.username_entry = ctk.CTkEntry(center_frame, height=40, width=300, font=("Arial", 18))  # Increased height and width
        self.username_entry.pack(pady=10)

        password_label = ctk.CTkLabel(center_frame, text="Password:", font=("Arial", 18))
        password_label.pack(pady=(5, 2))

        self.password_entry = ctk.CTkEntry(center_frame, show="*", height=40, width=300, font=("Arial", 18))  # Increased height and width
        self.password_entry.pack(pady=10)

        self.login_error_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent", font=("Arial", 16))
        self.login_error_label.pack(pady=(5, 2))

        login_button = ctk.CTkButton(center_frame, text="Login", command=self.handle_login, height=50, width=300, font=("Arial", 18))  # Adjusted size
        login_button.pack(pady=(20, 10))

        create_user_button = ctk.CTkButton(center_frame, text="Create New User", command=self.open_create_user_page, height=50, width=300, font=("Arial", 18))  # Adjusted size
        create_user_button.pack(pady=(10, 20))

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login(username, password)

    def login(self, username, password):
        users = self.user_manager.read_users()
        self.login_error_label.configure(text="")

        if username in users and users[username] == password:
            self.app.open_main_page()  # Correct reference to the app's method
        else:
            self.login_error_label.configure(text="Incorrect username or password.", fg_color="red")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_create_user_page(self):
        self.app.open_create_user_page()  # Correct reference to the app's method

class CreateUserPage:
    def __init__(self, master, user_manager, app):
        self.master = master
        self.user_manager = user_manager
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Create a frame that will fill the window screen
        container_frame = ctk.CTkFrame(self.master)
        container_frame.pack(fill="both", expand=True)

        # Configure grid for resizing
        container_frame.columnconfigure(0, weight=1)
        container_frame.rowconfigure(0, weight=1)
        container_frame.rowconfigure(1, weight=1)
        container_frame.rowconfigure(2, weight=1)
        container_frame.rowconfigure(3, weight=1)
        container_frame.rowconfigure(4, weight=1)
        container_frame.rowconfigure(5, weight=1)

        # Center Frame to contain the create user form
        center_frame = ctk.CTkFrame(container_frame)
        center_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Label for the create user page
        create_user_label = ctk.CTkLabel(center_frame, text="Create a New User", font=("Arial", 24))
        create_user_label.pack(pady=(20, 10), padx=10, fill="both")

        # New Username label and entry
        new_username_label = ctk.CTkLabel(center_frame, text="New Username:", font=("Arial", 18))
        new_username_label.pack(pady=(5, 2))

        self.new_username_entry = ctk.CTkEntry(center_frame, height=40, width=300, font=("Arial", 18))  # Increased size
        self.new_username_entry.pack(pady=10)

        # New Password label and entry
        new_password_label = ctk.CTkLabel(center_frame, text="New Password:", font=("Arial", 18))
        new_password_label.pack(pady=(5, 2))

        self.new_password_entry = ctk.CTkEntry(center_frame, show="*", height=40, width=300, font=("Arial", 18))  # Increased size
        self.new_password_entry.pack(pady=10)

        # Label for error messages
        self.create_user_error_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent", font=("Arial", 16))
        self.create_user_error_label.pack(pady=(5, 2))

        # Create User button
        create_user_button = ctk.CTkButton(center_frame, text="Create User", command=self.handle_create_user, height=50, width=300, font=("Arial", 18))  # Adjusted size
        create_user_button.pack(pady=(20, 10))

        # Back button
        back_button = ctk.CTkButton(center_frame, text="Back", command=self.app.open_login_page, height=50, width=300, font=("Arial", 18))  # Adjusted size
        back_button.pack(pady=(10, 20))

    def handle_create_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        users = self.user_manager.read_users()

        if new_username in users:
            self.show_error("Error: Username already exists! Choose a different one.")
        elif len(users) >= 10:
            self.show_error("Error: Max Number of users reached.")
        elif " " in new_username or ":" in new_username or " " in new_password or ":" in new_password:
            self.show_error("Error: Usernames and passwords cannot contain spaces or colons.")
        elif "" == new_username or "" == new_password:
            self.show_error("Must create both a username and password.")
        else:
            self.user_manager.save_user(new_username, new_password)
            self.app.open_login_page()

    def show_error(self, message):
        self.create_user_error_label.configure(text=message, fg_color="red")
        self.new_username_entry.delete(0, tk.END)
        self.new_password_entry.delete(0, tk.END)


class MainPage:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.create_widgets()
        # Grid the canvas into the electrogram_frame
        self.y_values = deque([0]*30, maxlen=30)  # Start with 30 zeros
        self.x_values = deque(range(0, 3000, 100), maxlen=30)  # X-axis values in milliseconds

        # Create a figure and axis for the plot
        self.fig = Figure(figsize=(5, 4), dpi=100)  # Adjust size for better visibility
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.x_values, self.y_values)

    def create_widgets(self):
        # Setting up the Grid Layout
        self.master.columnconfigure((0, 1), weight=1)
        self.master.columnconfigure((2, 3), weight=2)
        self.master.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        formatted_datetime = datetime.now().strftime("%Y-%m-%d - %H:%M:%S")
        date_time_label = ctk.CTkLabel(self.master, text=f"{formatted_datetime}", font=("Arial", 16))
        date_time_label.grid(row=0, column=0, columnspan=2, pady=2)

        username_label = ctk.CTkLabel(self.master, text="User Name", font=("Arial", 16))
        username_label.grid(row=1, column=0, columnspan=2, pady=2)

        select_mode_label = ctk.CTkLabel(self.master, text="Select Mode", font=("Arial", 16))
        select_mode_label.grid(row=2, column=0, columnspan=2, pady=2)

        pacemaker_state_options = ["AOO", "VOO", "AAI", "VVI"]
        self.initial_state = tk.StringVar(value="AOO")
        pacemaker_state_optionmenu = ctk.CTkOptionMenu(self.master, values=pacemaker_state_options, variable=self.initial_state)
        pacemaker_state_optionmenu.grid(row=3, column=0, columnspan=2, sticky="nw", pady=2, padx=2)

        admin_button = ctk.CTkButton(self.master, text="Admin Mode")
        admin_button.grid(row=4, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        # Show Electrogram button
        show_electrogram_button = ctk.CTkButton(self.master, text="Show Electrogram", command=self.show_electrogram)
        show_electrogram_button.grid(row=5, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        # Edit Parameters button
        edit_parameters_button = ctk.CTkButton(self.master, text="Edit Parameters", command=self.show_edit_frame)
        edit_parameters_button.grid(row=6, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        run_pacemaker_button = ctk.CTkButton(self.master, text="Run Pacemaker")
        run_pacemaker_button.grid(row=7, column=0, sticky="new", pady=10, padx=(10, 1))

        stop_pacemaker_button = ctk.CTkButton(self.master, text="Stop Pacemaker")
        stop_pacemaker_button.grid(row=7, column=1, sticky="new", pady=10, padx=(10, 1))

        logout_button = ctk.CTkButton(self.master, text="Logout", command=self.app.open_login_page)
        logout_button.grid(row=8, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        delete_user_button = ctk.CTkButton(self.master, text="Delete User")
        delete_user_button.grid(row=9, column=0, columnspan=2, sticky="new", pady=10, padx=(10, 1))

        connection_label = ctk.CTkLabel(self.master, text="Connection Status", font=("Arial", 16))
        connection_label.grid(row=0, column=2, sticky="new", pady=2)

        exit_button = ctk.CTkButton(self.master, text="Exit", command=self.master.destroy, fg_color="red", hover_color="#bd1809")
        exit_button.grid(row=0, column=3, sticky="new", pady=10, padx=(1, 10))
        
        # Frame for graph
        self.electrogram_frame = ctk.CTkFrame(self.master)
        
        # Frame for editing parameters
        self.edit_frame = ctk.CTkScrollableFrame(self.master)

        # Initialize by hiding both frames
        self.electrogram_frame.grid_forget()
        self.edit_frame.grid_forget()

        self.show_edit_frame()

    def show_electrogram(self):
        # Hide edit frame and show electrogram frame
        self.edit_frame.grid_forget()

        # Display electrogram frame with the plot
        self.electrogram_frame.grid(row=2, column=2, rowspan=8, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        

        # Embed the figure in a tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.electrogram_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nesw', padx=10, pady=10)
        self.electrogram_frame.columnconfigure(0, weight=1)  # Allow the column to expand
        self.electrogram_frame.rowconfigure(0, weight=1)     # Allow the row to expand

        self.update_plot()

    def show_edit_frame(self):
        # Hide electrogram frame and show edit frame
        self.electrogram_frame.grid_forget()
        
        self.edit_frame.grid(row=2, column=2, rowspan=8, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Clear existing widgets in the edit frame before adding new ones (optional)
        for widget in self.edit_frame.winfo_children():
            widget.destroy()

        variables = [
            "Lower Rate Limit (LRL): 60 bpm",
            "Upper Rate Limit (URL): 120 bpm",
            "Atrial Amplitude: 3.5V",
            "Atrial Pulse Width: 0.4ms",
            "Ventricular Pulse Width: 0.4ms",
            "Ventricular Amplitude: 2.8V",
            "Ventricular Refractory Period: 320ms",
            "Atrial Refractory Period: 250ms",
            "Mode: AOO"
        ]

        for input_text in variables:
            input_label = ctk.CTkLabel(self.edit_frame, text=input_text)  # Use self.edit_frame
            input_label.pack(pady=2, padx=2, anchor="w")  # Pack labels in the edit frame

    def update_plot(self):
        # Generate a new random y-value
        new_y_value = random.uniform(0, 1)

        # Update the y_values deque
        self.y_values.append(new_y_value)

        # Shift the x-values to create a moving window effect
        new_x_value = self.x_values[-1] + 100  # Increment the last x-value by 100 ms
        self.x_values.append(new_x_value)

        # Update the plot data
        self.line.set_ydata(self.y_values)
        self.line.set_xdata(self.x_values)

        # Set x-axis limits to show the last 3000 ms of data
        self.ax.set_xlim(max(0, new_x_value - 3000), new_x_value)  # Adjust x-limits to show last 3000 ms
        self.ax.set_ylim(0, 1)  # Set Y-axis range

        # Redraw the canvas with the updated plot
        self.canvas.draw()

        # Schedule the next update after 200 ms
        self.master.after(200, self.update_plot)



class App:
    def __init__(self, root):
        self.root = root
        self.user_manager = UserManager(USER_DATA_FILE)
        self.login_page = None
        self.create_user_page = None
        self.main_page = None
        self.open_login_page()
        

    def open_login_page(self):
        self.clear_page()
        self.login_page = LoginPage(self.root, self.user_manager, self)

    def open_create_user_page(self):
        self.clear_page()
        self.create_user_page = CreateUserPage(self.root, self.user_manager, self)

    def open_main_page(self):
        self.clear_page()
        self.main_page = MainPage(self.root, self)  # Correctly passing the app reference

    def clear_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))
    root.mainloop()