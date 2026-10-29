import json
import os

from product import Product
from inventory import Inventory


# Load inventory.json if it exists and return an Inventory of Product objects.
# If the file does not exist, return an empty Inventory.
def load_inventory():
    inventory = Inventory()
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as f:
            data = json.load(f)
        for item in data:
            inventory.add_product(
                Product(item["id"], item["name"], item["price"], item["stock"])
            )
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory
    print("inventory.json not found. Starting with empty inventory.")
    return inventory


# Write the inventory to inventory.json
def save_inventory(inventory):
    with open("inventory.json", "w") as f:
        json.dump(inventory.to_dict_list(), f, indent=4)


# Ask for product details and add a new product to the inventory
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        product = Product(product_id, name, price, stock)
        product.update_stock(stock)  # reuse the Product's own stock validation
    except ValueError:
        print("\nInvalid input. Price must be a number and stock a "
              "non-negative whole number. Product not added.")
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
    print(f"ID: {product.get_product_id()}")
    print(f"Name: {product.get_name()}")
    print(f"Price: ${product.get_price():.2f}")
    print(f"Stock: {product.get_stock()}")
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
        inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
        inventory.add_product(Product("P002", "Mouse", 25.50, 40))
        inventory.add_product(Product("P003", "Keyboard", 45.00, 25))

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