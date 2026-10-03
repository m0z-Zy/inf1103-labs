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

print("Current Inventory:")
for item in inventory:
    print(f"ID: {item['id']}, Name: {item['name']}, Price: ${item['price']:.2f}, Stock: {item['stock']}")