import json
import os

# Check if the inventory file exists
if os.path.exists("inventory.json"):
    with open("inventory.json", "r") as f:
        inventory = json.load(f)
else:
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]

# Return the product dictionary with a matching ID, or None.
def search_product(inventory, product_id):
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None

# Print every product in the inventory.
def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 47)
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | "
              f"Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 47)

# Ask for product details and add a new product to the list.
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

# Ask for a product ID, then set a new stock quantity.
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

def main():
    while True:
        print("\nInventory Management System")
        print("1. Display All Products")
        print("2. Add New Product")
        print("3. Update Stock")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            with open("inventory.json", "w") as f:
                json.dump(inventory, f, indent=4)
            print("\nInventory saved. Exiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")

main()