import json
import os

# Load inventory.json if it exists, otherwise return an empty list
def load_inventory():
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory
    print("inventory.json not found. Starting with empty inventory.")
    return []

# Write the inventory list to inventory.json
def save_inventory(inventory):
    with open("inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)

# Return the product dictionary with a matching ID, or None if not found
def search_product(inventory, product_id):
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None

# Print every product in the inventory
def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 47)
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | "
              f"Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 47)

# Ask for product details and add a new product to the list
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if search_product(inventory, product_id) is not None:
        print("A product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")

# Ask for a product ID, then set a new stock quantity
def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    product["stock"] = int(input("\nNew Stock Quantity: "))
    print("\nStock updated successfully!")

# Ask for a product ID and display the product if found
def search_menu(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print("-" * 47)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 47)

# Print the menu options
def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 26)

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40 + "\n")

    inventory = load_inventory()

    # Create new inventory with starter products if the inventory is empty
    if not inventory:
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
        ]

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_menu(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please choose 1-6.")

main()