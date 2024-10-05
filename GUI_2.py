import customtkinter as ctk
import tkinter as tk

import os
from PIL import Image, ImageTk

# for plotting
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

USER_DATA_FILE = "users.txt" # Path to store the users' information

# function to clear current entry fields
def clear_entries(entry):
    entry.delete(0, 'end')

# function to clear the current page deleting widgits       
def clear_page():
    for widget in root.winfo_children(): #Loops through all widgets and destroys them 
        widget.destroy()

#function to read users from file
def read_users():
    if not os.path.exists(USER_DATA_FILE): #if the file does not exist return an empty dictionary
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

def login(username, password, login_error_label, username_entry, password_entry):
    users = read_users()
    login_error_label.configure(text="")

    if username in users and users[username] == password:
        open_main_page()
    else:
        
        login_error_label.configure(text="", fg_color="transparent")
        root.after(100,lambda: login_error_label.configure(text="Incorrect username or password.", fg_color="red"))
        clear_entries(username_entry)
        clear_entries(password_entry)
        

def create_new_user(create_user_error_label, new_username_entry, new_password_entry):
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    users = read_users()

    if new_username in users:
        create_user_error_label.configure(text="", fg_color="transparent")
        root.after(100,lambda: create_user_error_label.configure(text="Error: Username already exists! Choose a different one.", fg_color="red"))
        clear_entries(new_username_entry)
        clear_entries(new_password_entry)
    elif len(users) >= 10:
        create_user_error_label.configure(text="", fg_color="transparent")
        root.after(100,lambda: create_user_error_label.configure(text="Error: Max Number of users reached.", fg_color="red"))
        clear_entries(new_username_entry)
        clear_entries(new_password_entry)
    elif " " in new_username or ":" in new_username or " " in new_password or ":" in new_password:
        create_user_error_label.configure(text="", fg_color="transparent")
        root.after(100,lambda: create_user_error_label.configure(text="Error: Usernames and passwords cannot contain spaces or colons..", fg_color="red"))
        clear_entries(new_username_entry)
        clear_entries(new_password_entry)
    elif "" == new_username or "" == new_password:
        create_user_error_label.configure(text="", fg_color="transparent")
        root.after(100,lambda: create_user_error_label.configure(text="Must create both a username and password", fg_color="red"))
        clear_entries(new_username_entry)
        clear_entries(new_password_entry)
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

    create_user_error_label = ctk.CTkLabel(root, text="", fg_color="transparent")  # Initially empty
    create_user_error_label.pack(pady=5)

    create_user_button = ctk.CTkButton(root, text="Create User", command= lambda: create_new_user(create_user_error_label, new_username_entry, new_password_entry))
    create_user_button.pack(pady=20)
    root.unbind('<Return>')
    root.bind('<Return>', lambda event: create_new_user(create_user_error_label, new_username_entry, new_password_entry))

    back_button = ctk.CTkButton(root, text="Back", command=open_login_page)
    back_button.pack(pady=10)


def open_login_page():
    clear_page()
    root.title("Login Page")

    # Create a frame to contain the left image, center login form, and right image
    container_frame = ctk.CTkFrame(root)
    container_frame.pack(fill="both", expand=True)  # Ensures full window usage

    # Left Frame for the left image
    left_frame = ctk.CTkFrame(container_frame, width=200)  # Fixed width for left frame
    left_frame.pack(side="left", fill="y")  # Fill vertically

    # Right Frame for the right image
    right_frame = ctk.CTkFrame(container_frame, width=200)  # Fixed width for right frame
    right_frame.pack(side="right", fill="y")  # Fill vertically

    # Center Frame for the login form
    center_frame = ctk.CTkFrame(container_frame)
    center_frame.pack(side="left", fill="both", expand=True)  # Expands to occupy available space

    

    # Resize and add an image to the left frame
    left_image_path = r"C:\Users\aidan\OneDrive - McMaster University\Third Year\First Semester\3K04 - Software Development\GUI\pacemaker_img.png"
    left_image = Image.open(left_image_path)
    left_image = left_image.resize((400, 400), Image.ANTIALIAS)  # Resize image to 100x100 pixels
    left_image = ImageTk.PhotoImage(left_image)
    
    left_image_label = tk.Label(left_frame, image=left_image, bg="light grey")
    left_image_label.pack(pady=70, padx=20)

    # Resize and add an image to the right frame
    right_image_path = r"C:\Users\aidan\OneDrive - McMaster University\Third Year\First Semester\3K04 - Software Development\GUI\heart1.png"
    right_image = Image.open(right_image_path)
    right_image = right_image.resize((400, 400), Image.ANTIALIAS)  # Resize image to 100x100 pixels
    right_image = ImageTk.PhotoImage(right_image)

    right_image_label = tk.Label(right_frame, image=right_image)
    right_image_label.pack(pady=70, padx=20)

    # Center Frame Content (login form)
    login_label = ctk.CTkLabel(center_frame, text="Welcome to the LeTron James PACEMAKER Login Page!!", font=("Arial", 20))
    login_label.pack(pady=(20, 10))  # Add more padding above

    username_label = ctk.CTkLabel(center_frame, text="Username:")
    username_label.pack(pady=(5, 2))

    username_entry = ctk.CTkEntry(center_frame)
    username_entry.pack(pady=5)

    password_label = ctk.CTkLabel(center_frame, text="Password:")
    password_label.pack(pady=(5, 2))

    password_entry = ctk.CTkEntry(center_frame, show="*")
    password_entry.pack(pady=5)

    login_error_label = ctk.CTkLabel(center_frame, text="", fg_color="transparent")  # Initially empty
    login_error_label.pack(pady=(5, 2))

    login_button = ctk.CTkButton(center_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), login_error_label, username_entry, password_entry))
    login_button.pack(pady=(10, 5))  # Adjusted padding

    # Bind the "Enter" key to the login function
    root.unbind('<Return>')
    root.bind('<Return>', lambda event: login(username_entry.get(), password_entry.get(), login_error_label, username_entry, password_entry))

    create_user_button = ctk.CTkButton(center_frame, text="Create New User", command=open_create_user_page)
    create_user_button.pack(pady=(5, 10))  # Adjusted padding

    # To prevent images from being garbage collected
    left_image_label.image = left_image
    right_image_label.image = right_image

def open_main_page():
    clear_page()

    root.title("Main Page")

    #Setting up the Gird Layout
    root.columnconfigure((0,1,2,3,4,5,6), weight=2)
    root.columnconfigure((7,8), weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure((1,2,3,4,5), weight=2)

    # Main page widgets
    pacemaker_state_options = ["AOO", "VOO", "AAI", "VVI"]
    initial_state = tk.StringVar(value="AOO")
    pacemaker_state_optionmenu = ctk.CTkOptionMenu(root, values=pacemaker_state_options, variable=initial_state)
    pacemaker_state_optionmenu.grid(row=0, column=0, columnspan=2, sticky="nw", pady=10, padx=10)


    logout_button = ctk.CTkButton(root, text="Logout", command=open_login_page)
    logout_button.grid(row=0, column=7, sticky="new", pady=10, padx=(10,1))
    exit_button = ctk.CTkButton(root, text="Exit", command=root.destroy, fg_color="red", hover_color="#bd1809")
    exit_button.grid(row=0, column=8, sticky="new", pady=10, padx=(1,10))

    frame = ctk.CTkScrollableFrame(master=root, width=200, height=400)
    frame.grid(row=1, column=0, rowspan=4, sticky="nsew", pady=10, padx=10)

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

    # Create a figure and a canvas for the plot
    fig = Figure(figsize=(1,2), dpi=200)
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Example plot

    # Embed the figure in a tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=3, rowspan=3, columnspan=6, sticky='nesw', padx=10, pady=10)
    


root = tk.Tk()
#open_login_page() 
open_main_page() # for testing purposes
root.attributes('-fullscreen', True)  # Set the window to fullscreen mode

# Bind the Escape key to exit fullscreen mode
root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

root.mainloop()