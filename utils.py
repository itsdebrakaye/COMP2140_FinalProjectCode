import customtkinter as ctk
from tkinter import messagebox
import json
import random

# Initialize the data with defaults in case loading fails
data = {
    "monthly_revenue": 50000,
    "daily_revenue": 2000,
    "total_orders_completed": 150,
    "pending_orders": 20,
    "inventory": {
        "Item A": 120,
        "Item B": 250,
        "Item C": 300,
        "Item D": 150,
        "Item E": 100
    }
}

# Initialize the orders data with defaults in case loading fails
orders_data = {
    "orders": [
        {"id": 1, "name": "John Doe", "address": "123 Main St, San Francisco, CA", "fragility": True, "express": False, "location": [37.7749, -122.4194]},
        {"id": 2, "name": "Jane Smith", "address": "456 Elm St, Paris, France", "fragility": False, "express": True, "location": [48.8566, 2.3522]},
        {"id": 3, "name": "Alice Johnson", "address": "789 Oak St, New York, NY", "fragility": True, "express": True, "location": [40.7128, -74.0060]},
        {"id": 4, "name": "Bob Brown", "address": "101 Pine St, London, UK", "fragility": False, "express": False, "location": [51.5074, -0.1278]},
        {"id": 5, "name": "Carol White", "address": "202 Maple St, Tokyo, Japan", "fragility": True, "express": True, "location": [35.6895, 139.6917]}
    ],
    "shipping_labels": []
}

def save_data():
    with open("data.json", "w") as file:
        json.dump(data, file)

def save_orders_data():
    with open("orders.json", "w") as file:
        json.dump(orders_data, file)

def load_data():
    global data
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        save_data()

def load_orders_data():
    global orders_data
    try:
        with open("orders.json", "r") as file:
            orders_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        save_orders_data()

def save_users_data(): 
    with open("users.json", "w") as file: 
        json.dump(users, file) 

def load_users_data(): 
    global users 
    try: 
        with open("users.json", "r") as file: 
            users = json.load(file) 
    except (FileNotFoundError, json.JSONDecodeError): 
        save_users_data()

def show_dashboard(permissions):
    load_data()
    load_orders_data()

    dashboard = ctk.CTkToplevel()
    dashboard.geometry("800x600")
    dashboard.title("Dashboard")

    # Adding widgets to the dashboard
    add_kpi(dashboard, "Monthly Revenue", f"${data['monthly_revenue']}")
    add_kpi(dashboard, "Daily Revenue", f"${data['daily_revenue']}")
    add_kpi(dashboard, "Total Orders Completed", data["total_orders_completed"])
    add_kpi(dashboard, "Pending Orders", data["pending_orders"])

    # Adding Production Chart and World Map
    add_chart(dashboard)
    add_world_map(dashboard)

    if permissions["inventory_adding"] or permissions["inventory_editing"] or permissions["inventory_deleting"]:
        ctk.CTkButton(dashboard, text="Inventory", font=("Arial", 14), command=inventory_gui).pack(pady=20)
    ctk.CTkButton(dashboard, text="Print Shipping Labels", font=("Arial", 14), command=print_shipping_labels).pack(pady=20)
    ctk.CTkButton(dashboard, text="Generate Order Labels", font=("Arial", 14), command=generate_order_labels).pack(pady=20)

def add_kpi(parent, label, value):
    frame = ctk.CTkFrame(master=parent)
    frame.pack(pady=10)
    ctk.CTkLabel(master=frame, text=label, font=("Arial", 12)).pack(side=ctk.LEFT)
    ctk.CTkLabel(master=frame, text=value, font=("Arial", 12)).pack(side=ctk.LEFT)

def add_chart(parent):
    frame = ctk.CTkFrame(master=parent)
    frame.pack(pady=20)
    ctk.CTkLabel(master=frame, text="Production Chart (February 2017)", font=("Arial", 14)).pack()
    # Here you can use Matplotlib or another library to create actual charts

def add_world_map(parent):
    frame = ctk.CTkFrame(master=parent)
    frame.pack(pady=20)
    ctk.CTkLabel(master=frame, text="World Map", font=("Arial", 14)).pack()
    # Here you can use a library to add a world map visualization

def inventory_gui():
    load_data()
    
    inventory = ctk.CTkToplevel()
    inventory.geometry("800x600")
    inventory.title("Inventory Management")

    # Inventory management functionality
    ctk.CTkLabel(inventory, text="Inventory Management", font=("Arial", 16)).pack(pady=20)
    ctk.CTkButton(inventory, text="Add Item", command=add_item).pack(pady=10)
    ctk.CTkButton(inventory, text="View Inventory", command=view_inventory).pack(pady=10)

def add_item():
    load_data()
    
    add_window = ctk.CTkToplevel()
    add_window.geometry("400x300")
    add_window.title("Add Item")

    ctk.CTkLabel(add_window, text="Item Name:").pack(pady=5)
    item_name = ctk.CTkEntry(add_window)
    item_name.pack(pady=5)

    ctk.CTkLabel(add_window, text="Quantity:").pack(pady=5)
    item_quantity = ctk.CTkEntry(add_window)
    item_quantity.pack(pady=5)

    def save_item():
        name = item_name.get()
        quantity = int(item_quantity.get())
        if name in data["inventory"]:
            data["inventory"][name] += quantity
        else:
            data["inventory"][name] = quantity
        save_data()
        messagebox.showinfo("Success", f"Item {name} with quantity {quantity} added to inventory!")
        add_window.destroy()

    ctk.CTkButton(add_window, text="Save", command=save_item).pack(pady=10)

def view_inventory():
    load_data()
    
    inventory_window = ctk.CTkToplevel()
    inventory_window.geometry("400x300")
    inventory_window.title("Inventory List")
    ctk.CTkLabel(inventory_window, text="Inventory List", font=("Arial", 14)).pack(pady=20)

    for item, quantity in data["inventory"].items():
        item_frame = ctk.CTkFrame(inventory_window)
        item_frame.pack(pady=5)
        ctk.CTkLabel(item_frame, text=f"Name: {item}, Quantity: {quantity}", font=("Arial", 12)).pack()

def generate_order_labels():
    load_orders_data()
    
    label_window = ctk.CTkToplevel()
    label_window.geometry("400x300")
    label_window.title("Generate Order Labels")

    ctk.CTkLabel(label_window, text="Enter Order ID:").pack(pady=5)
    order_id_entry = ctk.CTkEntry(label_window)
    order_id_entry.pack(pady=5)

    def create_label():
        order_id = int(order_id_entry.get())
        order = next((order for order in orders_data["orders"] if order["id"] == order_id), None)
        if order:
            label_id = f"LBL{random.randint(1000, 9999)}"
            order_label = {
                "label_id": label_id,
                "name": order["name"],
                "address": order["address"],
                "fragility": order["fragility"],
                "express": order["express"],
                "order_id": order_id
            }
            orders_data["shipping_labels"].append(order_label)
            save_orders_data()
            messagebox.showinfo("Success", f"Order label with ID {label_id} generated!")
        else:
            messagebox.showerror("Error", f"Order ID {order_id} not found!")

    ctk.CTkButton(label_window, text="Generate Label", command=create_label).pack(pady=10)

def delete_item():
    load_data()
    delete_window = ctk.CTkToplevel()
    delete_window.geometry("400x300")
    delete_window.title("Delete Item")

    ctk.CTkLabel(delete_window, text="Item Name:").pack(pady=5)
    item_name = ctk.CTkEntry(delete_window)
    item_name.pack(pady=5)

    ctk.CTkLabel(delete_window, text="Quantity to Delete:").pack(pady=5)
    item_quantity = ctk.CTkEntry(delete_window)
    item_quantity.pack(pady=5)

    def confirm_deletion():
        name = item_name.get()
        try:
            quantity_to_delete = int(item_quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity!")
            return

        if name in data["inventory"] and data["inventory"][name] >= quantity_to_delete:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {quantity_to_delete} of '{name}'?"):
                data["inventory"][name] -= quantity_to_delete
                if data["inventory"][name] == 0:
                    del data["inventory"][name]
                save_data()
                messagebox.showinfo("Success", f"Deleted {quantity_to_delete} of '{name}'!")
                delete_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid item name or insufficient quantity!")

    ctk.CTkButton(delete_window, text="Delete", command=confirm_deletion).pack(pady=10)



def update_user_permissions():
    load_users_data()

    update_window = ctk.CTkToplevel()
    update_window.geometry("400x400")
    update_window.title("Update User Permissions")

    ctk.CTkLabel(update_window, text="Update User Permissions", font=("Arial", 16)).pack(pady=20)

    ctk.CTkLabel(update_window, text="Username:").pack(pady=5)
    username_entry = ctk.CTkEntry(update_window)
    username_entry.pack(pady=5)

    def load_permissions():
        username = username_entry.get()

        if username in users:
            user = users[username]
            
            permissions_frame = ctk.CTkFrame(update_window)
            permissions_frame.pack(pady=10)

            var_order_editing = ctk.BooleanVar(value=user['permissions']['order_editing'])
            ctk.CTkCheckBox(permissions_frame, text="Order Editing", variable=var_order_editing).pack(anchor='w')

            var_inventory_adding = ctk.BooleanVar(value=user['permissions']['inventory_adding'])
            ctk.CTkCheckBox(permissions_frame, text="Inventory Adding", variable=var_inventory_adding).pack(anchor='w')

            var_inventory_editing = ctk.BooleanVar(value=user['permissions']['inventory_editing'])
            ctk.CTkCheckBox(permissions_frame, text="Inventory Editing", variable=var_inventory_editing).pack(anchor='w')

            var_inventory_deleting = ctk.BooleanVar(value=user['permissions']['inventory_deleting'])
            ctk.CTkCheckBox(permissions_frame, text="Inventory Deleting", variable=var_inventory_deleting).pack(anchor='w')

            var_user_permissions = ctk.BooleanVar(value=user['permissions']['user_permissions'])
            ctk.CTkCheckBox(permissions_frame, text="User Permissions", variable=var_user_permissions).pack(anchor='w')

            def save_user_permissions():
                user['permissions']['order_editing'] = var_order_editing.get()
                user['permissions']['inventory_adding'] = var_inventory_adding.get()
                user['permissions']['inventory_editing'] = var_inventory_editing.get()
                user['permissions']['inventory_deleting'] = var_inventory_deleting.get()
                user['permissions']['user_permissions'] = var_user_permissions.get()
                save_users_data()
                messagebox.showinfo("Success", f"Permissions for {username} updated successfully!")
                update_window.destroy()

            ctk.CTkButton(update_window, text="Save", command=save_user_permissions).pack(pady=10)
        else:
            messagebox.showerror("Error", "Username not found!")

    ctk.CTkButton(update_window, text="Load Permissions", command=load_permissions).pack(pady=10)


def print_shipping_labels():
    load_orders_data()
    
    shipping_window = ctk.CTkToplevel()
    shipping_window.geometry("400x300")
    shipping_window.title("Print Shipping Labels")

    ctk.CTkLabel(shipping_window, text="Enter Order ID or Label ID:").pack(pady=5)
    id_entry = ctk.CTkEntry(shipping_window)
    id_entry.pack(pady=5)

    def display_label():
        entered_id = id_entry.get()
        try:
            # Try to find by Label ID first
            shipping_label = next((label for label in orders_data["shipping_labels"] if label["label_id"] == entered_id), None)
            
            if not shipping_label:
                # If not found by Label ID, try by Order ID
                order_id = int(entered_id)
                shipping_label = next((label for label in orders_data["shipping_labels"] if any(order["id"] == order_id for order in orders_data["orders"] if order["id"] == order_id)), None)

            if shipping_label:
                messagebox.showinfo("Shipping Label", f"Shipping label ID: {shipping_label['label_id']}\nName: {shipping_label['name']}\nAddress: {shipping_label['address']}\nFragility: {shipping_label['fragility']}\nExpress: {shipping_label['express']}")
            else:
                messagebox.showerror("Error", f"Label or Order ID {entered_id} not found!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Order ID or Label ID")

    ctk.CTkButton(shipping_window, text="Display Label", command=display_label).pack(pady=10)

    def generate_label():
        entered_id = id_entry.get()
        shipping_label = next((label for label in orders_data["shipping_labels"] if label["label_id"] == entered_id), None)
        if not shipping_label:
            try:
                order_id = int(entered_id)
                order = next((order for order in orders_data["orders"] if order["id"] == order_id), None)
                if order:
                    shipping_label = {

                        "label_id": f"LBL{random.randint(1000, 9999)}",
                        "name": order["name"],
                        "address": order["address"],
                        "fragility": order["fragility"],
                        "express": order["express"]
                    }
                    orders_data["shipping_labels"].append(shipping_label)
                    save_orders_data()
                    messagebox.showinfo("Success", f"Shipping label for order ID {order_id} generated!")
                else:
                    messagebox.showerror("Error", f"Order ID {order_id} not found!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid Order ID or Label ID")
        else:
            messagebox.showinfo("Label Found", f"Shipping label ID: {shipping_label['label_id']}\nName: {shipping_label['name']}\nAddress: {shipping_label['address']}")

    ctk.CTkButton(shipping_window, text="Generate Label", command=generate_label).pack(pady=10)
