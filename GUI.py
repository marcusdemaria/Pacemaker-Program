import tkinter as tk
from tkinter import messagebox
import os

# Path to store the users' information
USER_DATA_FILE = "users.txt"

# Helper function to read users from file
def read_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    
    with open(USER_DATA_FILE, "r") as file:
        users = {}
        for line in file:
            username, password = line.strip().split(":")
            users[username] = password
        return users

# Helper function to save new user to file
def save_user(username, password):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username}:{password}\n")  # Write user info properly

# Function for login validation
def login(username, password, login_window):
    users = read_users()
    
    if username in users and users[username] == password:
        login_window.destroy()  # Close the login window on success
        main_page()  # Go to main page
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to create a new user
def create_new_user():
    new_username = entry_new_username.get().strip()
    new_password = entry_new_password.get().strip()
    
    users = read_users()

    if new_username in users:
        messagebox.showerror("Error", "Username already exists! Choose a different one.")
    elif len(users) >= 10:
        messagebox.showerror("Error", "Max Number of users reached.")
    elif " " in new_username or ":" in new_username or " " in new_password or ":" in new_password:
        messagebox.showerror("Error", "Usernames and passwords cannot contain spaces or colons.")
    else:
        save_user(new_username, new_password)
        messagebox.showinfo("Success", f"User {new_username} created successfully!")
        create_user_window.destroy()  # Close the new user window

# Function to open the new user creation window
def open_create_user_window():
    global create_user_window, entry_new_username, entry_new_password
    
    create_user_window = tk.Toplevel(root)
    create_user_window.title("Create New User")
    create_user_window.geometry("700x700")
    
    tk.Label(create_user_window, text="New Username:").pack(pady=5)
    entry_new_username = tk.Entry(create_user_window)
    entry_new_username.pack(pady=5)
    
    tk.Label(create_user_window, text="New Password:").pack(pady=5)
    entry_new_password = tk.Entry(create_user_window, show="*")
    entry_new_password.pack(pady=5)
    
    tk.Button(create_user_window, text="Create User", command=create_new_user).pack(pady=20)

# Function to open the main page after successful login
def main_page():
    main_window = tk.Toplevel(root)
    main_window.title("Main Page")
    main_window.geometry("700x700")
    
    tk.Label(main_window, text="Welcome to the Main Page!", font=("Arial", 16)).pack(pady=50)
    tk.Button(main_window, text="Exit", command=root.destroy).pack(pady=20)
    tk.Button(main_window, text="LogOut", command=lambda: [main_window.destroy(), open_login_window()]).pack(pady=20)

def open_login_window():
    global entry_username, entry_password  # Declare as global
    
    # Create a new top-level window for login
    login_window = tk.Toplevel(root)
    login_window.title("Login System")
    login_window.geometry("700x700")

    tk.Label(login_window, text="Login", font=("Arial", 20)).pack(pady=20)

    # Username input
    tk.Label(login_window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    # Password input
    tk.Label(login_window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    # Buttons for login and new user creation
    tk.Button(login_window, text="Login", command=lambda: login(entry_username.get(), entry_password.get(), login_window)).pack(pady=10)
    tk.Button(login_window, text="Create New User", command=open_create_user_window).pack(pady=5)

# Main application window
root = tk.Tk()
root.withdraw() # Hides the root window
open_login_window()  # Automatically open the login window

# Start the Tkinter loop
root.mainloop()
