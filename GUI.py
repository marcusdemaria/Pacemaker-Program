import tkinter as tk
from tkinter import font
from tkinter import messagebox
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        root.deiconify()  # Go to main page
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

def open_login_window():
    global entry_username, entry_password  # Declare as global
    
    # Create a new top-level window for login
    login_window = tk.Toplevel(root)
    login_window.title("Login System")
    login_window.geometry("300x300")

    tk.Label(login_window, text="Login", font=("Arial", 20)).pack(pady=20)

    # Username input
    tk.Label(login_window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)
    

    # Password input
    tk.Label(login_window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    
# Main application window
root = tk.Tk()

root.title("Main Page")
root.attributes('-fullscreen', True)  # Set the window to fullscreen mode

# Bind the Escape key to exit fullscreen mode
root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

# Configure the grid layout
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

# Create a larger button and place it in the top right corner
exit_button = tk.Button(root, text="Exit", command=root.destroy, width=15, height=4)
exit_button.grid(row=0, column=3, sticky='ne', padx=10, pady=10)  # Adjusted column

# Create the logout button and place it right below the exit button
logout_button = tk.Button(root, text="LogOut", command=lambda: [root.withdraw(), open_login_window()], width=15, height=4)
logout_button.grid(row=1, column=3, sticky='ne', padx=10, pady=0)  # Adjusted column

options = ["AOO", "VOO", "AAI", "VVI"]
selected_option = tk.StringVar()
selected_option.set(options[0])  # Set default value

label = tk.Label(root, text="Selected option: AOO")
label.grid(row=1, column=2, sticky='sw', pady=10)  # Adjusted row

def update_label(option):
    label.config(text=f"Selected option: {option}")


# Create a larger font for the dropdown menu
large_font = font.Font(size=14)

dropdown = tk.OptionMenu(root, selected_option, *options, command=update_label)
dropdown.config(font=large_font)
dropdown.grid(row=0, column=0, columnspan=2, sticky='nw', pady=20, padx=20)  # Adjusted row

# Create a figure for the graph
fig = Figure(figsize=(8,6), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Example plot

# Embed the figure in a tkinter canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=2, column=2, rowspan=3, columnspan=2, sticky='nesw', padx=10, pady=10)

# Start the Tkinter loop
root.mainloop()
