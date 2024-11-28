# app.py
from pages.login_page import LoginPage
from pages.create_user_page import CreateUserPage
from pages.main_page import MainPage
from user_manager import UserManager

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

