import tkinter as tk
from tkinter import messagebox, ttk
import json

# Function to load user data (users.json)
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save user data (users.json)
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Function to update a user's permissions
def update_permissions(username, permissions):
    users = load_users()
    if username in users:
        users[username]["permissions"] = permissions
        save_users(users)
        messagebox.showinfo("Success", f"Permissions for {username} updated!")
    else:
        messagebox.showerror("Error", f"User {username} not found!")

# Function to open the user permissions management page
def manage_user_permissions():
    from inventory import open_inventory_section
    users = load_users()
    
    def save_user_permissions():
        selected_user = user_listbox.get(tk.ACTIVE)
        if not selected_user:
            messagebox.showerror("Error", "No user selected!")
            return

        permissions = {
            "order_editing": order_editing_var.get(),
            "inventory_adding": inventory_adding_var.get(),
            "inventory_editing": inventory_editing_var.get(),
            "inventory_deleting": inventory_deleting_var.get(),
            "user_permissions": user_permissions_var.get()
        }
        
        update_permissions(selected_user, permissions)

    # Create a new window for user permissions
    permissions_window = tk.Toplevel(root)
    permissions_window.title("Manage User Permissions")
    permissions_window.geometry("600x400")

    tk.Label(permissions_window, text="Manage User Permissions", font=("Helvetica", 16)).pack(pady=10)

    # List of users
    user_listbox = tk.Listbox(permissions_window, height=10, width=50)
    for user in users.keys():
        user_listbox.insert(tk.END, user)
    user_listbox.pack(pady=10)

    tk.Label(permissions_window, text="Permissions", font=("Helvetica", 14)).pack(pady=10)

    # Permissions Checkboxes
    order_editing_var = tk.BooleanVar()
    inventory_adding_var = tk.BooleanVar()
    inventory_editing_var = tk.BooleanVar()
    inventory_deleting_var = tk.BooleanVar()
    user_permissions_var = tk.BooleanVar()

    tk.Checkbutton(permissions_window, text="Order Editing", variable=order_editing_var).pack()
    tk.Checkbutton(permissions_window, text="Inventory Adding", variable=inventory_adding_var).pack()
    tk.Checkbutton(permissions_window, text="Inventory Editing", variable=inventory_editing_var).pack()
    tk.Checkbutton(permissions_window, text="Inventory Deleting", variable=inventory_deleting_var).pack()
    tk.Checkbutton(permissions_window, text="User Permissions", variable=user_permissions_var).pack()

    # Save button
    tk.Button(permissions_window, text="Save Permissions", command=save_user_permissions).pack(pady=10)

# Adding the new button in the Dashboard
def dashboardpage():
    global root
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("600x400")

    from inventory import open_inventory_section  # Moved import here
    from loginscreen import login  # Moved import here

    tk.Button(root, text="Open Inventory Section", font=("Helvetica", 12), command=open_inventory_section).pack(pady=10)
    tk.Button(root, text="Generate Shipping Label", font=("Helvetica", 12), command=lambda: messagebox.showinfo("Generate Shipping", "Shipping label generated")).pack(pady=10)
    tk.Button(root, text="Print Inventory", font=("Helvetica", 12), command=lambda: messagebox.showinfo("Print Inventory", "Inventory printed")).pack(pady=10)
    tk.Button(root, text="User Permissions", font=("Helvetica", 12), command=manage_user_permissions).pack(pady=10)
    tk.Button(root, text="Logout", font=("Helvetica", 12), command=lambda: (root.destroy(), login())).pack(pady=10)

    root.mainloop()
