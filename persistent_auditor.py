def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()

    # Exit condition
    if user_input.lower() == "quit":
        return "quit"

    # Strip a leading '-' so we can still validate the digits,
    # but remember whether the original value was negative.
    is_negative = user_input.startswith('-')
    digits_only = user_input[1:] if is_negative else user_input

    # Handle invalid input (e.g. "ten") using isdigit()
    if digits_only == "" or not digits_only.isdigit():
        print(f"Error: '{user_input}' is not a valid integer. Entry rejected.")
        return None

    quantity = int(user_input)

    # Enforce business rules: no negative numbers
    if quantity < 0:
        print(f"Error: Negative quantities are not allowed ({quantity}). Entry rejected.")
        return None

    return quantity

def process_delivery(current_total, new_value):
    # Manage state: running total
    current_total += new_value
    print(f"Added {new_value} units. Current total inventory: {current_total}")

    # Trigger overstock alert
    if current_total > 500:
        print(f"ALERT: Overstock! Total inventory ({current_total}) exceeds 500 units.")

    return current_total

def calculate_tax(amount):
    # Tax is 10% of the delivery amount
    tax = amount * 0.10
    return tax

def generate_report(total_units, failed_attempts):
    # Reporting
    print("\n--- Final Report ---")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def load_inventory():
    #Read existing orders from orders.txt.
    #If the file doesn't exist, create it empty and
    #continue running without producing an error.
    orders = []
    try:
        with open("orders.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                order_id, name, qty = line.split(",")
                orders.append([order_id.strip(), name.strip(), int(qty.strip())])
    except FileNotFoundError:
        # File doesn't exist yet, create it empty
        open("orders.txt", "w").close()

    return orders

def get_next_order_id(orders):
    #Generate the next order ID based on existing orders (starts at 1001).
    if not orders:
        return 1001
    return max(int(order[0]) for order in orders) + 1

def main():
    orders = load_inventory()

    # Show current orders
    print("Current Orders:\n")
    for order_id, name, qty in orders:
        print(f"{order_id}, {name}, {qty}")

    # Prompt for new order details
    print()
    product_name = input("Enter Product Name: ").strip()
    quantity = int(input("Enter Quantity: ").strip())

    # Create and add the new order
    new_order_id = get_next_order_id(orders)
    orders.append([str(new_order_id), product_name, quantity])

    print("\nNew Order Added:")
    print(f"{new_order_id},{product_name},{quantity}\n")

if __name__ == "__main__":
    main()