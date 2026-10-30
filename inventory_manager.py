import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

# Build the correct Product subclass from a dictionary read from the JSON file.
# Raises KeyError or ValueError if the entry is missing data or has an unknown type.
def create_product(item):
    product_type = item["type"]
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], item["weight"])
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item["download_size"])
    raise ValueError(f"unknown product type '{product_type}'")

# Load inventory.json if it exists and return an Inventory of Product objects.
# If the file does not exist, return an empty Inventory.
def load_inventory():
    inventory = Inventory()
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as f:
            data = json.load(f)
        for item in data:
            try:
                inventory.add_product(create_product(item))
            except (KeyError, ValueError) as error:
                print(f"Skipped an entry in inventory.json: missing or invalid value {error}.")    
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory
    print("inventory.json not found. Starting with empty inventory.")
    return inventory

# Write the inventory to inventory.json
def save_inventory(inventory):
    with open("inventory.json", "w") as f:
        json.dump(inventory.to_dict_list(), f, indent=4)

# Ask for product details and add a new physical or digital product
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return
    print("\nProduct Type")
    print("1. Physical Product")
    print("2. Digital Product")
    type_choice = input("Choose type (1-2): ").strip()
    if type_choice not in ("1", "2"):
        print("\nInvalid product type. Product not added.")
        return
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if type_choice == "1":
            weight = float(input("Weight (kg): "))
            if weight < 0:
                raise ValueError("negative weight")
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            if download_size < 0:
                raise ValueError("negative download size")
            product = DigitalProduct(product_id, name, price, stock, download_size)
        product.update_stock(stock)  # reuse the Product's own stock validation
    except ValueError:
        print("\nInvalid input. Price, weight/size must be numbers (not negative) "
              "and stock a non-negative whole number. Product not added.")
        return
    inventory.add_product(product)
    print("\nProduct added successfully!")

# Ask for a product ID, then set a new stock quantity
def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        product.update_stock(int(input("\nNew Stock Quantity: ")))
    except ValueError:
        print("\nInvalid quantity. Stock must be a non-negative whole number. "
              "Stock not changed.")
        return
    print("\nStock updated successfully!")

# Ask for a product ID and display the product if found
def search_menu(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print("-" * 47)
    product.display_information()
    print(product.get_fulfilment_info())
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

    # Create starter products if the inventory is empty
    if inventory.is_empty():
        inventory.add_product(PhysicalProduct("P01", "Laptop", 1200.00, 15, 2.1))
        inventory.add_product(PhysicalProduct("P02", "Mouse", 25.50, 40, 0.1))
        inventory.add_product(DigitalProduct("D01", "Operating System", 99.00, 100, 4500.0))

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
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