import json
import os

from product_factory import ProductFactory
from input_helpers import get_positive_float
from inventory import Inventory
from product import Product
from supplier import Supplier

# Load inventory.json if it exists and return an Inventory of Product objects.
# If the file does not exist, return an empty Inventory.
def load_inventory() -> Inventory:
    inventory = Inventory()
    if os.path.exists("inventory.json"):
        try:
            with open("inventory.json", "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"inventory.json is empty or invalid. Starting with empty inventory.")
            return inventory
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
def save_inventory(inventory: Inventory) -> None:
    with open("inventory.json", "w") as f:
        json.dump(inventory.to_dict_list(), f, indent=4)

# Ask for product details and add a new physical or digital product
def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if inventory.find_product(product_id) is not None:
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
    supplier = Supplier(input("Supplier ID: ").strip(),
                        input("Supplier Name: ").strip(),
                        input("Supplier Email: ").strip())
    product: Product
    try:
        price = get_positive_float("Price: ")
        stock = int(input("Stock Quantity: "))
        if type_choice == "1":
            product_type = "physical"
            extra_value = float(input("Weight (kg): "))
            if extra_value < 0:
                raise ValueError("negative weight")
        else:
            product_type = "digital"
            extra_value = float(input("Download Size (MB): "))
            if extra_value < 0:
                raise ValueError("negative download size")
        product = ProductFactory.create(product_type, product_id, name, price, stock, supplier, extra_value)
        product.update_stock(stock)
    except ValueError:
        print("\nInvalid input. Price, weight/size must be numbers (not negative) "
              "and stock a non-negative whole number. Product not added.")
        return
    inventory.add_product(product)
    print("\nProduct added successfully!")

# Ask for a product ID, then set a new stock quantity
def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
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
def search_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print("-" * 47)
    product.display_information()
    print(product.get_fulfilment_info())
    print("-" * 47)

# Build the correct Product subclass from a dictionary read from the JSON file.
# Raises KeyError or ValueError if the entry is missing data or has an unknown type.
def create_product(item: dict) -> Product:
    product_type = item["type"]
    supplier = create_supplier(item.get("supplier"))
    extra_value = item.get("weight", item.get("download_size"))
    if extra_value is None:
        raise ValueError("missing weight or download_size")
    return ProductFactory.create(product_type, item["id"], item["name"], item["price"], item["stock"], supplier, extra_value)

# Build a Supplier from a dictionary in inventory.json.
# Older files without supplier data get an "Unassigned" supplier.
def create_supplier(data: dict | None) -> Supplier:
    if data is None:
        return Supplier("S00", "Unassigned", "none@example.com")
    return Supplier(data["id"], data["name"], data["email"])

# Print the menu options
def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 26)

def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40 + "\n")

    inventory = load_inventory()

    # Create starter products if the inventory is empty
    if inventory.is_empty():
        starter_supplier = Supplier("S01", "TechSource Ltd", "sales@techsource.com")
        inventory.add_product(ProductFactory.create("physical", "P01", "Laptop", 1200.00, 15, starter_supplier, 2.1))
        inventory.add_product(ProductFactory.create("physical", "P02", "Mouse", 25.50, 40, starter_supplier, 0.1))
        inventory.add_product(ProductFactory.create("digital", "D01", "Operating System", 99.00, 100, starter_supplier, 4500.0))

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

if __name__ == "__main__":
    main()