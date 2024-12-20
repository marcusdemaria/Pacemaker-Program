# pages/main_page.py
import customtkinter as ctk
import tkinter as tk  # Import the standard Tkinter library for creating GUI applications, as 'tk'
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from PIL import Image, ImageTk  # Import the Image and ImageTk classes from the Pillow library for image processing and display
from datetime import datetime  # Import the datetime class to handle date and time operations
import serial
import struct
import os

class MainPage:
    def __init__(self, master, app, username, user_manager): # Initialize the main page
        self.master = master # Reference to the main window
        self.app = app # Reference to the main application
        self.username = username # Store the username for the current user
        
        self.user_manager = user_manager  # Ensure user_manager is passed to the main page
        self.plot_running = False
        # Set up the serial connection
        self.ser = serial.Serial(port='COM8', baudrate=115200, timeout=1)
        
        #initial graphing data
        self.y_values_atrial = deque([0.5] * 30, maxlen=30)  # Y-axis values for the plot
        self.y_values_ventricular = deque([0.5] * 30, maxlen=30)
        self.x_values = deque(range(0, 3000, 100), maxlen=30)  # X-axis values for the plot

        # Create a figure and axis for the plot
        self.fig = Figure(figsize=(3, 5), dpi=100)  # Adjust size for better visibility
        self.ax = self.fig.add_subplot(111)

        

        self.line1, = self.ax.plot(self.x_values, self.y_values_atrial, label="Atrial Values")  #Plot the initial x and y values (empty or default data)
        self.line2, = self.ax.plot(self.x_values, self.y_values_ventricular, label="Ventrical Values")
       

        self.create_top_widgets()
        self.create_widgets() # Call the function to create the interface elements

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

        container_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        container_frame.pack(fill="both", expand=True)
        # Setting up the Grid Layout
        container_frame.columnconfigure(0, weight=1)
        container_frame.columnconfigure((1, 2, 3), weight=4)
        container_frame.rowconfigure(0, weight=1)
        container_frame.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9), weight=4)

        #setting up graph area
        # Create a canvas widget to display the matplotlib figure within the tkinter frame.
        self.electrogram_frame = ctk.CTkScrollableFrame(container_frame)
        self.electrogram_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=1, sticky="nsew")

        self.electrogram_control_frame = ctk.CTkFrame(container_frame)
        
        self.electrogram_control_frame.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")
        # Create the canvas for the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.electrogram_frame)
        
        # Attach the canvas to the tkinter grid, center it within the frame with padding.
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Frame for editing parameters
        self.edit_frame = ctk.CTkScrollableFrame(container_frame)
        self.edit_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew")
        
         
        #Setting up the rest of the area

        select_mode_label = ctk.CTkLabel(container_frame, text="Select Mode", font=("Arial", 16, "bold")) # Create a label for selecting pacemaker modes.
        select_mode_label.grid(row=0, column=0, pady=(10,1), padx=10, sticky="sw") # Place the mode label in the grid.

        pacemaker_state_options = ["AOO", "VOO", "AAI", "VVI", "AOOR", "VOOR", "AAIR", "VVIR"] # Define the options for pacemaker modes (AOO, VOO, AAI, VVI)
        self.initial_state = tk.StringVar(value="AOO")  # Initialize the pacemaker mode variable with a default value of "AOO".
        pacemaker_state_optionmenu = ctk.CTkOptionMenu(container_frame, values=pacemaker_state_options, variable=self.initial_state, command=self.update_edit_frame) # Create an option menu for selecting the pacemaker mode.
        pacemaker_state_optionmenu.grid(row=1, column=0, sticky="new", pady=1, padx=(10, 1)) # Place the option menu in the grid.

        # Segmented Button for Show Electrogram and Edit Parameters
        self.segmented_button = ctk.CTkSegmentedButton(container_frame, values=["Edit Parameters", "Show Electrogram"], command=self.segment_button_callback, font=("Arial", 16, "bold")) # Create a segmented button with two options
        self.segmented_button.grid(row=2, column=0, sticky="nesw", pady=1, padx=(10, 1))  # Place the segmented button in the grid
        self.segmented_button.set("Edit Parameters") # Set the default selection to "Edit Parameters"

        edit_data_button = ctk.CTkButton(container_frame, text="Save Data", command=self.update_user_data_check, font=("Arial", 22, "bold")) # Create a button to export data
        edit_data_button.grid(row=3, column=0, sticky="nesw", pady=1, padx=(10, 1))
        self.edit_data_button = edit_data_button # Store the reference to the button in self.edit_data_button for later use
        self.edit_data_button.configure(state="disabled") # Disable the edit data button
            
        # Admin Mode Toggle Button
        self.admin_mode = tk.BooleanVar(value=False) # Initialize a Boolean variable to track the state of admin mode (OFF by default)
        admin_mode_button = ctk.CTkButton(container_frame, text="Admin Mode: OFF", command=self.toggle_admin_mode, font=("Arial", 22, "bold")) # Create a button labeled "Admin Mode: OFF" that calls toggle_admin_mode when clicked
        admin_mode_button.grid(row=4, column=0, sticky="nesw", pady=1, padx=(10, 1)) # Place the button in the grid layout at row 8, column 0, spanning 2 columns with padding
        self.admin_mode_button = admin_mode_button # Store the reference to the button in self.admin_mode_button for later use

        logout_button = ctk.CTkButton(container_frame, text="Logout", command=self.app.open_login_page, font=("Arial", 22, "bold")) # Create a button to log out
        logout_button.grid(row=7, column=0, sticky="nesw", pady=1, padx=(10, 1))

        delete_user_button = ctk.CTkButton(container_frame, text="Delete User", command=self.delete_current_user_check, font=("Arial", 22, "bold")) # Create a button to delete the current user
        delete_user_button.grid(row=8, column=0, sticky="nesw", pady=(1,10), padx=(10, 1))
        self.delete_user_button = delete_user_button # Store the reference to the button in self.delete_user_button for later use
        self.delete_user_button.configure(state="disabled")
        
        
        
        
        # Initialize by hiding the electrogram frame
        self.electrogram_frame.grid_forget()
        self.electrogram_control_frame.configure(fg_color="transparent")
        self.show_edit_frame()


    def toggle_admin_mode(self):
        if not self.admin_mode.get():  # Admin Mode is OFF, prompt for a password
            # Create a popup frame and store it as an instance attribute
            self.popup_frame = ctk.CTkFrame(self.master, corner_radius=10)  
            self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
            
            # Create the label, entry, and submit button inside the popup frame
            self.admin_label = ctk.CTkLabel(self.popup_frame, text="Enter Admin Password:", font=("Arial", 16, "bold"))  
            self.admin_label.pack(pady=10, padx=15)  # Add padding to the label
            
            self.admin_password_entry = ctk.CTkEntry(self.popup_frame, show="*", font=("Arial", 16))  
            self.admin_password_entry.pack(pady=10)  # Add padding to the entry field
            
            self.submit_button = ctk.CTkButton(
                self.popup_frame, 
                text="Submit", 
                command=self.check_admin_password, 
                font=("Arial", 16, "bold")
            )  
            self.submit_button.pack(pady=10)  # Add padding to the submit button
        else:
            # Incorrect password: disable admin mode and show an error message
            self.admin_mode.set(False)
            self.admin_mode_button.configure(text="Admin Mode: OFF")
            self.edit_data_button.configure(state="disabled")
            self.delete_user_button.configure(state="disabled")
            self.update_edit_frame(self.initial_state.get())

    def check_admin_password(self):
        # Get the entered password
        entered_password = self.admin_password_entry.get()  
        
        # Validate the entered password
        if entered_password == "1234":  # Replace with a secure password
            # Correct password: enable admin mode
            self.admin_mode.set(True)
            self.admin_mode_button.configure(text="Admin Mode: ON")
            self.edit_data_button.configure(state="normal")
            self.delete_user_button.configure(state="normal")
            # Destroy the popup frame and its contents
            self.popup_frame.destroy()
            self.correct_password = ctk.CTkLabel(self.master, text="Correct Password", font=("Arial", 16, "bold"), text_color="green")
            self.correct_password.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
            self.master.after(3000, lambda: self.correct_password.destroy())
        else:
            # Incorrect password: disable admin mode and show an error message
            self.admin_mode.set(False)
            self.admin_mode_button.configure(text="Admin Mode: OFF")
            self.edit_data_button.configure(state="disabled")
            self.delete_user_button.configure(state="disabled")
            # Destroy the popup frame and its contents
            self.popup_frame.destroy()
            self.incorrect_password = ctk.CTkLabel(self.master, text="Incorrect Password", font=("Arial", 16, "bold"), text_color="red")
            self.incorrect_password.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
            self.master.after(3000, lambda: self.incorrect_password.destroy())
            

        

        # Update the frame with the new admin state
        self.update_edit_frame(self.initial_state.get())
    
    def delete_current_user_check(self):
         # Create a popup frame and store it as an instance attribute
        self.popup_frame = ctk.CTkFrame(self.master, corner_radius=10)  
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
        # Create BooleanVar for checkboxes
        self.checkbox1_var = ctk.BooleanVar()
        self.checkbox2_var = ctk.BooleanVar()
        self.check = ctk.CTkLabel(self.popup_frame, text="Are you sure you want to delete this account?", font=("Arial", 16, "bold"))
        self.check.pack(pady=10, padx=10)
        # Create checkboxes
        self.checkbox1 = ctk.CTkCheckBox(self.popup_frame, text="Yes", variable=self.checkbox1_var, command=self.delete_current_user)
        self.checkbox1.pack(side="left", pady=10, padx=(50, 10))

        self.checkbox2 = ctk.CTkCheckBox(self.popup_frame, text="No", variable=self.checkbox2_var, command=self.delete_current_user)
        self.checkbox2.pack(side="right", pady=10, padx=10)

    def delete_current_user(self):
        if self.checkbox1_var.get() and not self.checkbox2_var.get():
            self.popup_frame.destroy()
            current_user = self.username  # Get the username of the current user
            self.user_manager.delete_user(current_user)  # Delete the current user
            self.app.open_login_page()  # Open the login page after deleting the user
        else:
            self.popup_frame.destroy()

    def reset_plot(self):
        self.y_values_atrial.clear()  # Clear existing y-values
        self.y_values_ventricular.clear()
        self.x_values.clear()  # Clear existing x-values
        self.y_values_atrial.extend([0.5] * 30)  # Reset y-values to 30 zeros
        self.y_values_ventricular.extend([0.5] * 30)
        self.x_values.extend(range(0, 3000, 100))  # Reset x-values from 0 to 3000, with increments of 100

        # Update the line data
        if self.initial_graphing_state.get() == "Atrial":
            self.line1.set_ydata(self.y_values_atrial)  # Set the y-data of the plot line to the new y-values
        elif self.initial_graphing_state.get() == "Ventrical":
            self.line2.set_ydata(self.y_values_ventricular)
        else:
            self.line1.set_ydata(self.y_values_atrial)
            self.line2.set_ydata(self.y_values_ventricular)
        
        self.line1.set_xdata(self.x_values) # Set the x-data of the plot line to the new x-values
        self.line2.set_xdata(self.x_values) # Set the x-data of the plot line to the new x-values
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
    def send_packet(self, sync, command, mode, apw, vpw, a_amp, v_amp, a_sens, v_sens, arp, vrp, url, lrl, res_factor, rxn_time, rec_time, thresh):
        packet = struct.pack(  # Format the packet
            'BBBBBBBBBBBBBBBBB',
            sync, command, mode, apw, vpw, a_amp, v_amp, a_sens, v_sens, arp, vrp, url, lrl, res_factor, rxn_time, rec_time, thresh
        )
        self.ser.write(packet)  # Send the packet over serial

    def show_electrogram(self):
        # Hide edit frame and show electrogram frame
        self.edit_frame.grid_forget() # Remove the edit frame from the grid layout (not destroyed, just hidden)
        self.plot_running = True
        # Display electrogram frame with the plot

        

        for widget in self.electrogram_control_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame (to avoid duplication or clutter)
        self.electrogram_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew") # Show the electrogram plot frame in a specific grid position
        self.electrogram_control_frame.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        #stuff that goes in the electrogram control frame
        graphing_state_options = ["Atrial", "Ventrical", "Both"] 
        self.initial_graphing_state = tk.StringVar(value="Atrial")  # Initialize the pacemaker mode variable with a default value of "AOO".
        graphing_state_optionmenu = ctk.CTkOptionMenu(self.electrogram_control_frame, values=graphing_state_options, variable=self.initial_graphing_state) # Create an option menu for selecting the pacemaker mode.
        
        graphing_state_optionmenu.grid(row=0, column=0, sticky="new", pady=1, padx=(10, 1)) # Place the option menu in the grid.

        self.start_button = ctk.CTkButton(self.electrogram_control_frame, text="Start", font=("Arial", 12, "bold"), command=self.choose_plotting_mode) # Create a button to start the plot
        self.start_button.grid(row=0, column=1, sticky="nesw", pady=1, padx=(10, 1))

        self.stop_button = ctk.CTkButton(self.electrogram_control_frame, text="Stop", font=("Arial", 12, "bold"), command=self.stop_plot) # Create a button to stop the plot
        self.stop_button.grid(row=0, column=2, sticky="nesw", pady=1, padx=(10, 1))

        self.save_graph_button = ctk.CTkButton(self.electrogram_control_frame, text="Save Graph", font=("Arial", 12, "bold"), command=self.save_graph) # Create a button to save the graph
        self.save_graph_button.grid(row=0, column=3, sticky="nesw", pady=1, padx=(10, 1))
    
    def update_legend(self, labels):
        self.ax.legend(labels=labels, loc="upper right")  # Dynamically update the legend

    def stop_plot(self):
        self.plot_running = False

    def choose_plotting_mode(self):
        self.plot_running = True
        if self.initial_graphing_state.get() == "Atrial":
            self.update_plot_atrial(self.initial_state.get())
        elif self.initial_graphing_state.get() == "Ventrical":
            self.update_plot_ventrical(self.initial_state.get())
        else:
            self.update_plot_both(self.initial_state.get())

    def update_plot_atrial(self, mode):
        # Label the graph
        self.ax.set_title("Atrial")  # Set the title of the plot
        self.ax.set_xlabel("Time (ms)")   # Label for the x-axis
        self.ax.set_ylabel("Amplitude (V)")  # Label for the y-axis
        # Update the legend for Atrial mode only
        self.update_legend(["Atrial"])
        if not self.plot_running:
            return
        if self.initial_graphing_state.get() != "Atrial":
            return self.choose_plotting_mode()
        #send the data
        if mode == "AOO":
            self.send_packet(1, 1, 1, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)
            print(self.atrial_pulse_width.get())
        elif mode == "VOO":
                
            self.send_packet(1, 1, 2, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)

        elif mode == "AAI":
                
            self.send_packet(1, 1, 3, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)

        elif mode == "VVI":
                
            self.send_packet(1, 1, 4, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)

        elif mode == "AOOR":
                
            self.send_packet(1, 1, 5, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "VOOR":
            self.send_packet(1, 1, 6, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "AAIR":
            self.send_packet(1, 1, 7, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "VVIR":
            self.send_packet(1, 1, 8, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        # recieve the data
        raw_data = self.ser.read(32)  # Read exactly 32 bytes
        if len(raw_data) == 32:
            #unopacking the data
            format_string = '16Bdd'  # 16 unsigned bytes (B) and 2 double-precision floats (d)
            unpacked_data = struct.unpack(format_string, raw_data)

        
        # Generate a new random y-value between 0 and 1
        new_y_value = unpacked_data[16]  # Use the unpacked float variable as the new y-value
        print(new_y_value)
        # Update the y_values deque
        self.y_values_atrial.append(new_y_value)

        # Shift the x-values to create a moving window effect
        new_x_value = self.x_values[-1] + 100  # Increment the last x-value by 100 ms
        self.x_values.append(new_x_value) # Append the new x-value to the x_values deque

        # Update the plot data with the new x and y values
        self.line1.set_ydata(self.y_values_atrial) # Update the y-data of the plot line
        self.line1.set_xdata(self.x_values) # Update the x-data of the plot line
        self.line2.set_ydata([])
        self.line2.set_xdata([])
        # Set x-axis limits to show the last 3000 ms of data
        self.ax.set_xlim(max(0, new_x_value - 3000), new_x_value)  # Adjust x-limits to show last 3000 ms
        self.ax.set_ylim(0.2, 0.8)  # Set Y-axis range

        # Redraw the canvas with the updated plot
        self.canvas.draw()

        # Schedule the next update after 200 ms
        if self.plot_running:
            self.master.after(200, lambda: self.update_plot_atrial(mode))
    
    def update_plot_ventrical(self, mode):
        # Label the graph
        self.ax.set_title("Ventrical")  # Set the title of the plot
        self.ax.set_xlabel("Time (ms)")   # Label for the x-axis
        self.ax.set_ylabel("Amplitude (V)")  # Label for the y-axis
        # Update the legend for Ventricular mode only
        self.update_legend(["Ventrical"])
        if not self.plot_running:
            return
        
        if self.initial_graphing_state.get() != "Ventrical":
            return self.choose_plotting_mode()
        
        #send the data
        if mode == "AOO":
            self.send_packet(1, 1, 1, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)
            print(self.atrial_pulse_width.get())
        elif mode == "VOO":
                
            self.send_packet(1, 1, 2, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)

        elif mode == "AAI":
                
            self.send_packet(1, 1, 3, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)

        elif mode == "VVI":
                
            self.send_packet(1, 1, 4, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)

        elif mode == "AOOR":
                
            self.send_packet(1, 1, 5, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "VOOR":
            self.send_packet(1, 1, 6, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "AAIR":
            self.send_packet(1, 1, 7, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "VVIR":
            self.send_packet(1, 1, 8, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        # recieve the data
        raw_data = self.ser.read(32)  # Read exactly 32 bytes
        if len(raw_data) == 32:
            #unopacking the data
            format_string = '16Bdd'  # 16 unsigned bytes (B) and 2 double-precision floats (d)
            unpacked_data = struct.unpack(format_string, raw_data)

        
        # Generate a new random y-value between 0 and 1
        new_y_value = unpacked_data[17]  # Use the unpacked float variable as the new y-value
        print(new_y_value)
        # Update the y_values deque
        self.y_values_ventricular.append(new_y_value)

        # Shift the x-values to create a moving window effect
        new_x_value = self.x_values[-1] + 100  # Increment the last x-value by 100 ms
        self.x_values.append(new_x_value) # Append the new x-value to the x_values deque

        # Update the plot data with the new x and y values
        self.line2.set_ydata(self.y_values_ventricular) # Update the y-data of the plot line
        self.line2.set_xdata(self.x_values) # Update the x-data of the plot line
        self.line1.set_ydata([])
        self.line1.set_xdata([])
        # Set x-axis limits to show the last 3000 ms of data
        self.ax.set_xlim(max(0, new_x_value - 3000), new_x_value)  # Adjust x-limits to show last 3000 ms
        self.ax.set_ylim(0.2, 0.8)  # Set Y-axis range

        # Redraw the canvas with the updated plot
        self.canvas.draw()

        # Schedule the next update after 200 ms
        if self.plot_running:
            self.master.after(200, lambda: self.update_plot_ventrical(mode))
    
    def update_plot_both(self, mode):
        # Label the graph
        self.ax.set_title("Atrial and Ventrical")  # Set the title of the plot
        self.ax.set_xlabel("Time (ms)")   # Label for the x-axis
        self.ax.set_ylabel("Amplitude (V)")  # Label for the y-axis
        # Update the legend for Ventricular mode only
        self.update_legend(["Atrial", "Ventrical"])
        if not self.plot_running:
            return
        if self.initial_graphing_state.get() != "Both":
            return self.choose_plotting_mode()
        
        #send the data
        if mode == "AOO":
            self.send_packet(1, 1, 1, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)
            print(self.atrial_pulse_width.get())
        elif mode == "VOO":
                
            self.send_packet(1, 1, 2, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)

        elif mode == "AAI":
                
            self.send_packet(1, 1, 3, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)

        elif mode == "VVI":
                
            self.send_packet(1, 1, 4, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0, 0)

        elif mode == "AOOR":
                
            self.send_packet(1, 1, 5, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "VOOR":
            self.send_packet(1, 1, 6, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "AAIR":
            self.send_packet(1, 1, 7, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        elif mode == "VVIR":
            self.send_packet(1, 1, 8, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

        # recieve the data
        raw_data = self.ser.read(32)  # Read exactly 32 bytes
        if len(raw_data) == 32:
            #unopacking the data
            format_string = '16Bdd'  # 16 unsigned bytes (B) and 2 double-precision floats (d)
            unpacked_data = struct.unpack(format_string, raw_data)
        
        # Generate a new random y-value between 0 and 1
        new_y_value1 = unpacked_data[16]  # Use the unpacked float variable as the new y-value
        new_y_value2 = unpacked_data[17]
        print(new_y_value1)
        print(new_y_value2)
        # Update the y_values deque
        self.y_values_ventricular.append(new_y_value1)
        self.y_values_atrial.append(new_y_value2)

        # Shift the x-values to create a moving window effect
        new_x_value = self.x_values[-1] + 100  # Increment the last x-value by 100 ms
        self.x_values.append(new_x_value) # Append the new x-value to the x_values deque

        # Update the plot data with the new x and y values
        self.line1.set_ydata(self.y_values_atrial) # Update the y-data of the plot line
        self.line2.set_ydata(self.y_values_ventricular)
        self.line1.set_xdata(self.x_values) # Update the x-data of the plot line
        self.line2.set_xdata(self.x_values) # Update the x-data of the plot line
        # Set x-axis limits to show the last 3000 ms of data
        self.ax.set_xlim(max(0, new_x_value - 3000), new_x_value)  # Adjust x-limits to show last 3000 ms
        self.ax.set_ylim(0.2, 0.8)  # Set Y-axis range

        # Redraw the canvas with the updated plot
        self.canvas.draw()

        # Schedule the next update after 200 ms
        if self.plot_running:
            self.master.after(200, lambda: self.update_plot_both(mode))

    def save_graph(self):
        # Define the folder where you want to save the file
        folder_name = "graphs"  # Replace with your desired folder name
        directory = os.path.join(os.getcwd(), folder_name)  # Combine current working directory with folder name
        
        # Create the folder if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        file_name = self.username
        if self.initial_graphing_state.get() == "Atrial":
            file_path = os.path.join(directory, file_name + "_atrial.png")
        elif self.initial_graphing_state.get() == "Ventrical":
            file_path = os.path.join(directory, file_name + "_ventrical.png")
        else:
            file_path = os.path.join(directory, file_name + "_both.png")
        
        
        
        # Save the graph
        self.fig.savefig(file_path)
        print(f"Graph saved as '{file_path}'")
        
    def show_edit_frame(self):
        # Hide the electrogram frame to make the edit frame visible
        self.electrogram_frame.grid_forget()
        self.electrogram_control_frame.configure(fg_color="transparent")
        self.plot_running = False
        # Display the edit frame in the specified grid position with padding
        self.edit_frame.grid(row=1, column=1, rowspan=9, columnspan=3, padx=10, pady=10, sticky="nsew")

        for widget in self.electrogram_control_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame (to avoid duplication or clutter)
        self.format = ctk.CTkButton(self.electrogram_control_frame, text="", fg_color="transparent") # Create a button to save the graph
        self.format.grid(row=0,column=0, sticky="nsew", pady=1, padx=(10, 1)) # Place the button on the left side of the frame
        
        # Clear existing widgets in the edit frame before adding new ones (optional for cleanliness)
        for widget in self.edit_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame

        self.update_edit_frame(self.initial_state.get())

    def update_edit_frame(self, mode):
        # Clear existing widgets in the edit frame before adding new ones (optional for cleanliness)
        for widget in self.edit_frame.winfo_children(): # Iterate through each widget inside the edit frame
            widget.destroy() # Remove the widget from the frame (to avoid duplication or clutter)

        username_data = self.user_manager.read_user(self.username)
        if mode not in username_data:
            username_data[mode] = {}

        # Define the variables and their values based on the selected mode
        if mode == "AOO":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AOO"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AOO"]["Upper Rate Limit"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AOO"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AOO"]["Atrial Pulse Width"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Atrial Amplitude", 0.5, 10, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1)
            ]
            

        elif mode == "VOO":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VOO"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VOO"]["Upper Rate Limit"])
            self.ventricular_amplitude = tk.DoubleVar(value=username_data["VOO"]["Ventricular Amplitude"])
            self.ventricular_pulse_width = tk.DoubleVar(value=username_data["VOO"]["Ventricular Pulse Width"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Ventricular Amplitude", 0.5, 10, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
            ]
            

        elif mode == "AAI":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AAI"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AAI"]["Upper Rate Limit"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AAI"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AAI"]["Atrial Pulse Width"])

            self.atrial_sensitivity = tk.DoubleVar(value=username_data["AAI"]["Atrial Sensitivity"]) 
            self.arp = tk.DoubleVar(value=username_data["AAI"]["ARP"]) 
            self.hysteresis = tk.DoubleVar(value=username_data["AAI"]["Hysteresis"])  
            self.rate_smoothing = tk.DoubleVar(value=username_data["AAI"]["Rate Smoothing"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Atrial Amplitude", 0.5, 10, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1),
                ("Atrial Sensitivity", 6, 10, self.atrial_sensitivity, 1),
                ("ARP", 100, 500, self.arp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3)
            ]
            
        elif mode == "VVI":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VVI"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VVI"]["Upper Rate Limit"])
            self.ventricular_amplitude = tk.DoubleVar(value=username_data["VVI"]["Ventricular Amplitude"])
            self.ventricular_pulse_width = tk.DoubleVar(value=username_data["VVI"]["Ventricular Pulse Width"])
            self.ventricular_sensitivity = tk.DoubleVar(value=username_data["VVI"]["Ventricular Sensitivity"]) 
            self.vrp = tk.DoubleVar(value=username_data["VVI"]["VRP"])  
            self.hysteresis = tk.DoubleVar(value=username_data["VVI"]["Hysteresis"])  
            self.rate_smoothing = tk.DoubleVar(value=username_data["VVI"]["Rate Smoothing"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Ventricular Amplitude", 0.5, 10, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
                ("Ventrical Sensitivity", 6, 10, self.ventricular_sensitivity, 1),
                ("VRP", 100, 500, self.vrp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3)
            ]
        elif mode == "AOOR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AOOR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AOOR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["AOOR"]["Max Sensor Rate"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AOOR"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AOOR"]["Atrial Pulse Width"])
            self.activity_threshold = tk.DoubleVar(value=username_data["AOOR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["AOOR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["AOOR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["AOOR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Atrial Amplitude", 0.5, 10, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1),
                ("Activity Threshold", 60, 120, self.activity_threshold, 10),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
            ]
        elif mode == "VOOR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VOOR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VOOR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["VOOR"]["Max Sensor Rate"])
            self.ventricular_amplitude = tk.DoubleVar(value=username_data["VOOR"]["Ventricular Amplitude"])
            self.ventricular_pulse_width = tk.DoubleVar(value=username_data["VOOR"]["Ventricular Pulse Width"])
            self.activity_threshold = tk.DoubleVar(value=username_data["VOOR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["VOOR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["VOOR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["VOOR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Ventricular Amplitude", 0.5, 10, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
                ("Activity Threshold", 60, 120, self.activity_threshold, 10),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
            ]
        elif mode == "AAIR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["AAIR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["AAIR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["AAIR"]["Max Sensor Rate"])
            self.atrial_amplitude = tk.DoubleVar(value=username_data["AAIR"]["Atrial Amplitude"])
            self.atrial_pulse_width = tk.DoubleVar(value=username_data["AAIR"]["Atrial Pulse Width"])
            self.atrial_sensitivity = tk.DoubleVar(value=username_data["AAIR"]["Atrial Sensitivity"]) 
            self.arp = tk.DoubleVar(value=username_data["AAIR"]["ARP"]) 
            self.pvarp = tk.DoubleVar(value=username_data["AAIR"]["PVARP"])
            self.hysteresis = tk.DoubleVar(value=username_data["AAIR"]["Hysteresis"])  
            self.rate_smoothing = tk.DoubleVar(value=username_data["AAIR"]["Rate Smoothing"])
            self.activity_threshold = tk.DoubleVar(value=username_data["AAIR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["AAIR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["AAIR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["AAIR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Atrial Amplitude", 0.5, 10, self.atrial_amplitude, 0.5),
                ("Atrial Pulse Width", 1, 30, self.atrial_pulse_width, 1),
                ("Atrial Sensitivity", 6, 10, self.atrial_sensitivity, 1),
                ("ARP", 100, 500, self.arp, 10),
                ("PVARP", 150, 500, self.pvarp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3),
                ("Activity Threshold", 60, 120, self.activity_threshold, 10),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
            ]
        elif mode == "VVIR":
            # Initialize variables for the sliders
            self.lower_rate_limit = tk.DoubleVar(value=username_data["VVIR"]["Lower Rate Limit"])
            self.upper_rate_limit = tk.DoubleVar(value=username_data["VVIR"]["Upper Rate Limit"])
            self.max_sensor_rate = tk.DoubleVar(value=username_data["VVIR"]["Max Sensor Rate"])
            self.ventricular_amplitude = tk.DoubleVar(value=username_data["VVIR"]["Ventricular Amplitude"])
            self.ventricular_pulse_width = tk.DoubleVar(value=username_data["VVIR"]["Ventricular Pulse Width"])
            self.ventricular_sensitivity = tk.DoubleVar(value=username_data["VVIR"]["Ventricular Sensitivity"])
            self.vrp = tk.DoubleVar(value=username_data["VVIR"]["VRP"])
            self.hysteresis = tk.DoubleVar(value=username_data["VVIR"]["Hysteresis"])
            self.rate_smoothing = tk.DoubleVar(value=username_data["VVIR"]["Rate Smoothing"])
            self.activity_threshold = tk.DoubleVar(value=username_data["VVIR"]["Activity Threshold"])
            self.reaction_time = tk.DoubleVar(value=username_data["VVIR"]["Reaction Time"])
            self.response_factor = tk.DoubleVar(value=username_data["VVIR"]["Response Factor"])
            self.recovery_time = tk.DoubleVar(value=username_data["VVIR"]["Recovery Time"])
            variables = [
                ("Lower Rate Limit (LRL)", 30, 180, self.lower_rate_limit, 5),
                ("Upper Rate Limit (URL)", 50, 180, self.upper_rate_limit, 5),
                ("Max Sensor Rate", 50, 175, self.max_sensor_rate, 5),
                ("Ventricular Amplitude", 0.5, 10, self.ventricular_amplitude, 0.5),
                ("Ventricular Pulse Width", 1, 30, self.ventricular_pulse_width, 1),
                ("Ventricular Sensitivity", 6, 10, self.ventricular_sensitivity, 1),
                ("VRP", 100, 500, self.vrp, 10),
                ("Hysteresis", 0.5, 5.0, self.hysteresis, 0.5),
                ("Rate Smoothing", 3, 24, self.rate_smoothing, 3),
                ("Activity Threshold", 60, 120, self.activity_threshold, 10),
                ("Reaction Time", 10, 50, self.reaction_time, 5),
                ("Response Factor", 1, 16, self.response_factor, 1),
                ("Recovery Time", 2, 16, self.recovery_time, 1)
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

    def update_user_data_check(self):
         # Create a popup frame and store it as an instance attribute
        self.popup_frame = ctk.CTkFrame(self.master, corner_radius=10)  
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the popup frame
        # Create BooleanVar for checkboxes
        self.checkbox1_var = ctk.BooleanVar()
        self.checkbox2_var = ctk.BooleanVar()
        self.check = ctk.CTkLabel(self.popup_frame, text="Are you sure you want to save the data?", font=("Arial", 16, "bold"))
        self.check.pack(pady=10, padx=10)
        # Create checkboxes
        self.checkbox1 = ctk.CTkCheckBox(self.popup_frame, text="Yes", variable=self.checkbox1_var, command=self.update_user_data)
        self.checkbox1.pack(side="left", pady=10, padx=(50, 10))

        self.checkbox2 = ctk.CTkCheckBox(self.popup_frame, text="No", variable=self.checkbox2_var, command=self.update_user_data)
        self.checkbox2.pack(side="right", pady=10, padx=10)


    def update_user_data(self):
        if self.checkbox1_var.get() and not self.checkbox2_var.get():
            self.popup_frame.destroy()
            username_data = self.user_manager.read_user(self.username)
    
            if self.initial_state.get() == "AOO":
                username_data["AOO"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AOO"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AOO"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AOO"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()
                self.send_packet(1, 0, 1, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)
            elif self.initial_state.get() == "VOO":
                username_data["VOO"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VOO"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VOO"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VOO"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()
                self.send_packet(1, 0, 2, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)

            elif self.initial_state.get() == "AAI":
                username_data["AAI"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AAI"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AAI"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AAI"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()
                username_data["AAI"]["Atrial Sensitivity"] = self.atrial_sensitivity.get()
                username_data["AAI"]["ARP"] = self.arp.get()
                username_data["AAI"]["Hysteresis"] = self.hysteresis.get()
                username_data["AAI"]["Rate Smoothing"] = self.rate_smoothing.get()
                self.send_packet(1, 0, 3, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)

            elif self.initial_state.get() == "VVI":
                username_data["VVI"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VVI"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VVI"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VVI"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()
                username_data["VVI"]["Ventricular Sensitivity"] = self.ventricular_sensitivity.get()
                username_data["VVI"]["VRP"] = self.vrp.get()
                username_data["VVI"]["Hysteresis"] = self.hysteresis.get()
                self.send_packet(1, 0, 4, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), 0, 0, 0, 0)

            elif self.initial_state.get() == "AOOR":
                username_data["AOOR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AOOR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AOOR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["AOOR"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AOOR"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()
                username_data["AOOR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["AOOR"]["Reaction Time"] = self.reaction_time.get()
                username_data["AOOR"]["Response Factor"] = self.response_factor.get()
                username_data["AOOR"]["Recovery Time"] = self.recovery_time.get()
                self.send_packet(1, 0, 5, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

            elif self.initial_state.get() == "VOOR":
                username_data["VOOR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VOOR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VOOR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["VOOR"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VOOR"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()
                username_data["VOOR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["VOOR"]["Reaction Time"] = self.reaction_time.get()
                username_data["VOOR"]["Response Factor"] = self.response_factor.get()
                username_data["VOOR"]["Recovery Time"] = self.recovery_time.get()

                self.send_packet(1, 0, 6, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, 0, 0, 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

            elif self.initial_state.get() == "AAIR":
                username_data["AAIR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["AAIR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["AAIR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["AAIR"]["Atrial Amplitude"] = self.atrial_amplitude.get()
                username_data["AAIR"]["Atrial Pulse Width"] = self.atrial_pulse_width.get()
                username_data["AAIR"]["Atrial Sensitivity"] = self.atrial_sensitivity.get()
                username_data["AAIR"]["ARP"] = self.arp.get()
                username_data["AAIR"]["PVARP"] = self.pvarp.get()
                username_data["AAIR"]["Hysteresis"] = self.hysteresis.get()
                username_data["AAIR"]["Rate Smoothing"] = self.rate_smoothing.get()
                username_data["AAIR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["AAIR"]["Reaction Time"] = self.reaction_time.get()
                username_data["AAIR"]["Response Factor"] = self.response_factor.get()
                username_data["AAIR"]["Recovery Time"] = self.recovery_time.get()

                self.send_packet(1, 0, 7, int(self.atrial_pulse_width.get()), 0, int(self.atrial_amplitude.get()), 0, int(self.atrial_sensitivity.get()), 0, int(self.arp.get()), 0, int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

            elif self.initial_state.get() == "VVIR":
                username_data["VVIR"]["Lower Rate Limit"] = self.lower_rate_limit.get()
                username_data["VVIR"]["Upper Rate Limit"] = self.upper_rate_limit.get()
                username_data["VVIR"]["Max Sensor Rate"] = self.max_sensor_rate.get()
                username_data["VVIR"]["Ventricular Amplitude"] = self.ventricular_amplitude.get()
                username_data["VVIR"]["Ventricular Pulse Width"] = self.ventricular_pulse_width.get()
                username_data["VVIR"]["Ventricular Sensitivity"] = self.ventricular_sensitivity.get()
                username_data["VVIR"]["VRP"] = self.vrp.get()
                username_data["VVIR"]["Hysteresis"] = self.hysteresis.get()
                username_data["VVIR"]["Rate Smoothing"] = self.rate_smoothing.get()
                username_data["VVIR"]["Activity Threshold"] = self.activity_threshold.get()
                username_data["VVIR"]["Reaction Time"] = self.reaction_time.get()
                username_data["VVIR"]["Response Factor"] = self.response_factor.get()
                username_data["VVIR"]["Recovery Time"] = self.recovery_time.get()
                self.send_packet(1, 0, 8, 0, int(self.ventricular_pulse_width.get()), 0, int(self.ventricular_amplitude.get()), 0, int(self.ventricular_sensitivity.get()), 0, int(self.vrp.get()), int(self.upper_rate_limit.get()), int(self.lower_rate_limit.get()), int(self.response_factor.get()), int(self.reaction_time.get()), int(self.recovery_time.get()), int(self.activity_threshold.get()))

            username_data["password"] = self.user_manager._encrypt_password(username_data["password"])
            self.user_manager.update_user_data(self.username, username_data)
        else:
            self.popup_frame.destroy()


    