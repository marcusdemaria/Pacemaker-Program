# main.py
import tkinter as tk
from app import App
import customtkinter as ctk

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.mainloop()
