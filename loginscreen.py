import customtkinter as ctk
from tkinter import messagebox
import json
from utils import show_dashboard

def create_admin_gui(root, restart_callback):
    def save_admin():
        password = password_entry.get()

        if password:
            users = {
                "admin": {
                    "password": password,
                    "role": "admin",
                    "permissions": {
                        "order_editing": True,
                        "inventory_adding": True,
                        "inventory_editing": True,
                        "inventory_deleting": True,
                        "user_permissions": True
                    }
                }
            }
            with open("users.json", "w") as file:
                json.dump(users, file)
            messagebox.showinfo("Success", "Admin created successfully!")
            root.destroy()
            restart_callback()  # Call the callback function to restart the main application
        else:
            messagebox.showerror("Error", "All fields are required!")

    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="Create Admin User", font=("Arial", 20))
    label.pack(pady=12, padx=10)

    password_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="Save", command=save_admin)
    button.pack(pady=12, padx=10)

def login_screen(root, restart_callback):
    def authenticate(username, password):
        with open("users.json", "r") as file:
            users = json.load(file)

        user = users.get(username)
        if user and user["password"] == password:
            messagebox.showinfo("Success", "Logged in successfully!")
            root.destroy()
            show_dashboard(user["permissions"])  # Pass permissions to the dashboard
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="My-Jamaica-Island-System", font=("Arial", 20))
    label.pack(pady=12, padx=10)

    username_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
    username_entry.pack(pady=12, padx=10)

    password_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)

    login_button = ctk.CTkButton(master=frame, text="Login", command=lambda: authenticate(username_entry.get(), password_entry.get()))
    login_button.pack(pady=12, padx=10)

    remember_me_checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    remember_me_checkbox.pack(pady=12, padx=10)

    ctk.CTkButton(master=frame, text="Create New Profile", command=lambda: create_new_profile(root, restart_callback)).pack(pady=10)

def create_new_profile(root, restart_callback):
    def save_profile():
        username = username_entry.get()
        password = password_entry.get()

        if username and password:
            with open("users.json", "r") as file:
                users = json.load(file)
            users[username] = {
                "password": password,
                "role": "user",
                "permissions": {
                    "order_editing": False,
                    "inventory_adding": False,
                    "inventory_editing": False,
                    "inventory_deleting": False,
                    "user_permissions": False
                }
            }
            with open("users.json", "w") as file:
                json.dump(users, file)
            messagebox.showinfo("Success", "Profile created successfully!")
            root.destroy()
            restart_callback()  # Call the callback function to restart the main application
        else:
            messagebox.showerror("Error", "All fields are required!")

    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="Create New Profile", font=("Arial", 20))
    label.pack(pady=12, padx=10)

    username_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
    username_entry.pack(pady=12, padx=10)

    password_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="Save", command=save_profile)
    button.pack(pady=12, padx=10)
