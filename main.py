import customtkinter as ctk
import tkinter as tk
from loginscreen import create_admin_gui, login_screen
import json
import ctypes

# Set DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print(f"Could not set DPI awareness: {e}")

def setup_admin(root):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    if "admin" not in users:
        create_admin_gui(root, main)
    else:
        login_screen(root, main)

def main():
    ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

    root = ctk.CTk()
    root.tk.call('tk', 'scaling', 1.0)
    root.geometry("800x600")
    root.title("User Management System")
    setup_admin(root)
    root.mainloop()

if __name__ == "__main__":
    main()
