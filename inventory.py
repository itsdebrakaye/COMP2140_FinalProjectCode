import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

# Load inventory from the JSON file
def load_inventory():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Save inventory to the JSON file
def save_inventory(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

# Function to add an item to the inventory
def add_item(inventory_window, tree):
    def submit():
        name = name_entry.get()
        quantity = quantity_entry.get()
        user_id = user_id_entry.get()
        passcode = passcode_entry.get()

        if passcode == "1234":  # Use a fixed passcode for simplicity
            inventory = load_inventory()
            inventory.append({
                "name": name,
                "quantity": int(quantity),
                "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": user_id,
            })
            save_inventory(inventory)
            messagebox.showinfo("Success", "Item added successfully!")
            inventory_window.destroy()
            open_inventory_section()  # Refresh inventory section
        else:
            messagebox.showerror("Error", "Invalid passcode!")

    frame = tk.Frame(inventory_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Add Item to Inventory", font=("Arial", 18)).pack(pady=10)
    tk.Label(frame, text="Item Name:").pack()
    name_entry = tk.Entry(frame, font=("Arial", 14))
    name_entry.pack()

    tk.Label(frame, text="Quantity:").pack()
    quantity_entry = tk.Entry(frame, font=("Arial", 14))
    quantity_entry.pack()

    tk.Label(frame, text="User ID:").pack()
    user_id_entry = tk.Entry(frame, font=("Arial", 14))
    user_id_entry.pack()

    tk.Label(frame, text="Passcode:").pack()
    passcode_entry = tk.Entry(frame, font=("Arial", 14), show="*")
    passcode_entry.pack()

    tk.Button(frame, text="Submit", command=submit, font=("Arial", 14)).pack(pady=10)

# Function to modify an item in the inventory
def modify_item(inventory_window, tree):
    def submit_modification():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected for modification!")
            return

        item_id = selected_item[0]
        inventory = load_inventory()

        name = name_entry.get()
        quantity = quantity_entry.get()
        user_id = user_id_entry.get()

        for item in inventory:
            if item["name"] == tree.item(item_id, "values")[0]:
                item["name"] = name
                item["quantity"] = int(quantity)
                item["user_id"] = user_id
                item["date_added"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_inventory(inventory)
        messagebox.showinfo("Success", "Item modified successfully!")
        inventory_window.destroy()
        open_inventory_section()  # Refresh inventory section

    frame = tk.Frame(inventory_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Modify Item in Inventory", font=("Arial", 18)).pack(pady=10)
    tk.Label(frame, text="New Item Name:").pack()
    name_entry = tk.Entry(frame, font=("Arial", 14))
    name_entry.pack()

    tk.Label(frame, text="New Quantity:").pack()
    quantity_entry = tk.Entry(frame, font=("Arial", 14))
    quantity_entry.pack()

    tk.Label(frame, text="New User ID:").pack()
    user_id_entry = tk.Entry(frame, font=("Arial", 14))
    user_id_entry.pack()

    tk.Button(frame, text="Submit", bg="#4a8dfb", fg="white", command=submit_modification).pack(pady=10)

# Function to delete an item from the inventory
def delete_item(inventory_window, tree):
    def submit_deletion():
        item_name = name_entry.get()
        quantity_to_delete = int(quantity_entry.get())

        inventory = load_inventory()

        if item_name in [item["name"] for item in inventory]:
            for item in inventory:
                if item["name"] == item_name:
                    if item["quantity"] >= quantity_to_delete:
                        item["quantity"] -= quantity_to_delete
                        if item["quantity"] == 0:
                            inventory.remove(item)
                        save_inventory(inventory)
                        messagebox.showinfo("Success", f"Item '{item_name}' deleted successfully!")
                        open_inventory_section()  # Refresh inventory section
                    else:
                        messagebox.showerror("Error", f"Not enough quantity to delete. Current quantity: {item['quantity']}")
                    return
            messagebox.showinfo("Success", f"Item '{item_name}' deleted successfully!")
            open_inventory_section()  # Refresh inventory section
        else:
            messagebox.showerror("Error", f"Item '{item_name}' not found in inventory!")

    def confirm_deletion():
        item_name = name_entry.get()
        quantity_to_delete = quantity_entry.get()

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {quantity_to_delete} of '{item_name}'?"):
            submit_deletion()

    frame = tk.Frame(inventory_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Delete Item from Inventory", font=("Arial", 18)).pack(pady=10)
    tk.Label(frame, text="Item Name:").pack()
    name_entry = tk.Entry(frame, font=("Arial", 14))
    name_entry.pack()

    tk.Label(frame, text="Quantity to Delete:").pack()
    quantity_entry = tk.Entry(frame, font=("Arial", 14))
    quantity_entry.pack()

    tk.Button(frame, text="Delete", bg="#ff4b4b", fg="white", command=confirm_deletion).pack(pady=10)

# Open the inventory section
def open_inventory_section():
    inventory_window = tk.Toplevel()
    inventory_window.geometry("600x500")
    inventory_window.title("Inventory Management")

    tk.Label(inventory_window, text="Inventory Management", font=("Helvetica", 16)).pack(pady=20)

    tree = ttk.Treeview(inventory_window, columns=("Item Name", "Quantity", "Date Added", "User ID"), show="headings")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Date Added", text="Date Added")
    tree.heading("User ID", text="User ID")
    tree.pack(fill=tk.BOTH, expand=True)

    # Buttons for managing the inventory
    tk.Button(inventory_window, text="Add Item", font=("Helvetica", 12), command=lambda: add_item(inventory_window, tree)).pack(pady=10)
    tk.Button(inventory_window, text="Modify Item", font=("Helvetica", 12), command=lambda: modify_item(inventory_window, tree)).pack(pady=10)
    tk.Button(inventory_window, text="Delete Item", font=("Helvetica", 12), command=lambda: delete_item(inventory_window, tree)).pack(pady=10)

    # Load and display the inventory
    inventory_data = load_inventory()
    for item in inventory_data:
        if isinstance(item, dict):
            tree.insert("", "end", values=(item["name"], item["quantity"], item["date_added"], item["user_id"]))
        else:
            messagebox.showerror("Error", "Invalid inventory data format")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    open_inventory_section()
    root.mainloop()
