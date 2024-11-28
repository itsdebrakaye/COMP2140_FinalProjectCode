from tkinter import Tk
from loginscreen import create_admin_gui, login_screen
from utils import show_dashboard, show_login  # Import from utils

def setup_admin(root):
    import json
    from tkinter import messagebox

    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    if "admin" not in users:
        create_admin_gui(root)
    else:
        login_screen(root)

def main():
    root = Tk()
    setup_admin(root)
    root.mainloop()
