import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    def __init__(self, master, user_manager, app):
        self.master = master
        self.user_manager = user_manager
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        container_frame = ctk.CTkFrame(self.master)
        container_frame.pack(fill="both", expand=True)

        center_frame = ctk.CTkFrame(container_frame)
        center_frame.pack(side="left", fill="both", expand=True)

        login_label = ctk.CTkLabel(center_frame, text="Welcome to the LeTron James PACEMAKER Login Page!!", font=("Arial", 20))
        login_label.pack(pady=(20, 10))

        username_label = ctk.CTkLabel(center_frame, text="Username:")
        username_label.pack(pady=(5, 2))

        self.username_entry = ctk.CTkEntry(center_frame)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(center_frame, text="Password:")
        password_label.pack(pady=(5, 2))

        self.password_entry = ctk.CTkEntry(center_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_error_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent")
        self.login_error_label.pack(pady=(5, 2))

        login_button = ctk.CTkButton(center_frame, text="Login", command=self.handle_login)
        login_button.pack(pady=(10, 5))

        create_user_button = ctk.CTkButton(center_frame, text="Create New User", command=self.open_create_user_page)
        create_user_button.pack(pady=(5, 10))

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login(username, password)

    def login(self, username, password):
        users = self.user_manager.read_users()
        self.login_error_label.configure(text="")

        if username in users and users[username] == password:
            self.app.open_main_page()
        else:
            self.login_error_label.configure(text="Incorrect username or password.", fg_color="red")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_create_user_page(self):
        self.app.open_create_user_page()


class CreateUserPage:
    def __init__(self, master, user_manager, app):
        self.master = master
        self.user_manager = user_manager
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Create New User")
        new_username_label = ctk.CTkLabel(self.master, text="New Username:")
        new_username_label.pack(pady=5)

        self.new_username_entry = ctk.CTkEntry(self.master)
        self.new_username_entry.pack(pady=5)

        new_password_label = ctk.CTkLabel(self.master, text="New Password:")
        new_password_label.pack(pady=5)

        self.new_password_entry = ctk.CTkEntry(self.master, show="*")
        self.new_password_entry.pack(pady=5)

        self.create_user_error_label = ctk.CTkLabel(self.master, text="", fg_color="transparent")
        self.create_user_error_label.pack(pady=5)

        create_user_button = ctk.CTkButton(self.master, text="Create User", command=self.handle_create_user)
        create_user_button.pack(pady=20)

        back_button = ctk.CTkButton(self.master, text="Back", command=self.app.open_login_page)
        back_button.pack(pady=10)

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

    def create_widgets(self):
        # Setting up the Grid Layout
        self.master.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=2)
        self.master.columnconfigure((7, 8), weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure((1, 2, 3, 4, 5), weight=2)

        # Main page widgets
        pacemaker_state_options = ["AOO", "VOO", "AAI", "VVI"]
        self.initial_state = tk.StringVar(value="AOO")
        pacemaker_state_optionmenu = ctk.CTkOptionMenu(self.master, values=pacemaker_state_options, variable=self.initial_state)
        pacemaker_state_optionmenu.grid(row=0, column=0, columnspan=2, sticky="nw", pady=10, padx=10)

        logout_button = ctk.CTkButton(self.master, text="Logout", command=self.app.open_login_page)
        logout_button.grid(row=0, column=7, sticky="new", pady=10, padx=(10, 1))
        exit_button = ctk.CTkButton(self.master, text="Exit", command=self.master.destroy, fg_color="red", hover_color="#bd1809")
        exit_button.grid(row=0, column=8, sticky="new", pady=10, padx=(1, 10))

        frame = ctk.CTkScrollableFrame(master=self.master, width=200, height=400)
        frame.grid(row=1, column=0, rowspan=4, sticky="nsew", pady=10, padx=10)

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
            input_label = ctk.CTkLabel(frame, text=input_text)
            input_label.pack(pady=2, padx=2, anchor="w")

        # Create a figure and a canvas for the plot
        fig = Figure(figsize=(5, 4), dpi=100)  # Adjust size for better visibility
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Example plot

        # Embed the figure in a tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=3, rowspan=3, columnspan=6, sticky='nesw', padx=10, pady=10)


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