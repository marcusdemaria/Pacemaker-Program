def update_plot_atrial(self):
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

    # Generate a new random y-value between 0 and 1
    new_y_value = random.uniform(0, 1)

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
    self.ax.set_ylim(0, 1)  # Set Y-axis range

    # Redraw the canvas with the updated plot
    self.canvas.draw()

    # Schedule the next update after 200 ms
    if self.plot_running:
        self.master.after(200, self.update_plot_atrial)

def update_plot_ventrical(self):
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
    # Generate a new random y-value between 0 and 1
    new_y_value = random.uniform(0, 1)

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
    self.ax.set_ylim(0, 1)  # Set Y-axis range

    # Redraw the canvas with the updated plot
    self.canvas.draw()

    # Schedule the next update after 200 ms
    if self.plot_running:
        self.master.after(200, self.update_plot_ventrical)

def update_plot_both(self):
    # Label the graph
    self.ax.set_title("Both")  # Set the title of the plot
    self.ax.set_xlabel("Time (ms)")   # Label for the x-axis
    self.ax.set_ylabel("Amplitude (V)")  # Label for the y-axis
    # Update the legend for Ventricular mode only
    self.update_legend(["Atrial", "Ventrical"])
    if not self.plot_running:
        return
    if self.initial_graphing_state.get() != "Both":
        return self.choose_plotting_mode()
    # Generate a new random y-value between 0 and 1
    new_y_value1 = random.uniform(0, 1)
    new_y_value2 = random.uniform(0, 1)

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
    self.ax.set_ylim(0, 1)  # Set Y-axis range

    # Redraw the canvas with the updated plot
    self.canvas.draw()

    # Schedule the next update after 200 ms
    if self.plot_running:
        self.master.after(200, self.update_plot_ventrical)

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
