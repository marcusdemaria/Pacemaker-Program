import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os

USER_DATA_FILE = "users.txt"
global new_username_entry, new_password_entry

def clear_page():
    for widget in root.winfo_children(): #Loops through all widgets and destroys them 
        widget.destroy()


def read_users():
    if not os.path.exists(USER_DATA_FILE): #need explination for why this works
        return{}

    with open(USER_DATA_FILE, "r") as file:
        users = {}
        for line in file:
            username, password = line.strip().split(":")
            users[username] = password
        return users

def save_user(username, password):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username}:{password}\n")

def login(username, password, error_label):
    users = read_users()
    error_label.configure(text="")

    if username in users and users[username] == password:
        open_main_page()
    else:
        
        error_label.configure(text="", fg_color="transparent")
        root.after(100,lambda: error_label.configure(text="Incorrect username or password.", fg_color="red"))
        
        

def create_new_user():
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    users = read_users()

    if new_username in users:
        messagebox.showerror("Error", "Username already exists! Choose a different one.")
    elif len(users) >= 10:
        messagebox.showerror("Error", "Max Number of users reached.")
    elif " " in new_username or ":" in new_username or " " in new_password or ":" in new_password:
        messagebox.showerror("Error", "Usernames and passwords cannot contain spaces or colons.")
    else:
        save_user(new_username, new_password)
        open_login_page()



def open_create_user_page():
    clear_page()
    root.title("Create New User")
    

    new_username_label = ctk.CTkLabel(root, text="New Username:")
    new_username_label.pack(pady=5)

    new_username_entry = ctk.CTkEntry(root)
    new_username_entry.pack(pady=5)

    new_password_label = ctk.CTkLabel(root, text="New Password:")
    new_password_label.pack(pady=5)

    new_password_entry = ctk.CTkEntry(root, show="*")
    new_password_entry.pack(pady=5)

    create_user_button = ctk.CTkButton(root, text="Create User", command=create_new_user)
    create_user_button.pack(pady=20)

    back_button = ctk.CTkButton(root, text="Back", command=open_login_page)
    back_button.pack(pady=10)

def open_login_page():
    clear_page()
    root.title("Login Page")

    login_label = ctk.CTkLabel(root, text="Login", font=("Arial", 20))
    login_label.pack(pady=50)

    username_label = ctk.CTkLabel(root, text="Username:")
    username_label.pack(pady=5)

    username_entry = ctk.CTkEntry(root)
    username_entry.pack(pady=5)

    password_label = ctk.CTkLabel(root, text="Password:")
    password_label.pack(pady=5)

    password_entry = ctk.CTkEntry(root, show="*")
    password_entry.pack(pady=5)

    error_label = ctk.CTkLabel(root, text="", fg_color="transparent")  # Initially empty
    error_label.pack(pady=5)

    login_button = ctk.CTkButton(root, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), error_label))
    login_button.pack(pady=20)
    # Bind the "Enter" key to the login function
    root.bind('<Return>', lambda event: login(username_entry.get(), password_entry.get(), error_label))

    create_user_button = ctk.CTkButton(root, text="Create New User", command=open_create_user_page)
    create_user_button.pack(pady=10)

def open_main_page():
    clear_page()

    root.title("Main Page")

    # Main page widgets
    pacemaker_state_options = ["AOO", "VOO", "AAI", "VVI"]
    initial_state = tk.StringVar(value="AOO")
    pacemaker_state_optionmenu = ctk.CTkOptionMenu(root, values=pacemaker_state_options, variable=initial_state)
    pacemaker_state_optionmenu.grid(row=0, column=0, columnspan=2, sticky="nw", pady=10, padx=10)


    logout_button = ctk.CTkButton(root, text="Logout", command=open_login_page)
    logout_button.grid(row=0, column=3, sticky="nsew", pady=10, padx=10)
    exit_button = ctk.CTkButton(root, text="Exit", command=root.destroy)
    exit_button.grid(row=0, column=4, sticky="nsew", pady=10, padx=10)

    frame = ctk.CTkScrollableFrame(master=root, width=200, height=400)
    frame.grid(row=1, column=0, rowspan=5, sticky="nsew", pady=10, padx=10)

    lower_limit= "60bpm"
    variables = {
        (f"Lower Rate Limit: {lower_limit}"),
        ("Upper Rate Limit: 120 bpm"),
        ("Atrial Amplitude: 3.5V"),
        ("Ventricular Amplitude: 2.8V"),
        ("Mode: AOO")
    }

    for input_text in variables:
        input = ctk.CTkLabel(frame, text=input_text)
        input.pack(pady=2, padx=2, anchor="w")
    

root = ctk.CTk()

#open_login_page() 
open_main_page() # for testing purposes
root.attributes('-fullscreen', True)  # Set the window to fullscreen mode

# Bind the Escape key to exit fullscreen mode
root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

root.mainloop()