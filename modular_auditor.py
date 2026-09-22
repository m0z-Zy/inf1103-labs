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

def main():
    total_inventory = 0
    failed_entries = 0

    while True:
        result = get_valid_input()

        # Exit condition
        if result == "quit":
            break

        # Handle invalid input
        if result is None:
            failed_entries += 1
            continue

        quantity = result

        total_inventory = process_delivery(total_inventory, quantity)

        # Calculate tax for this delivery
        tax_owed = calculate_tax(quantity)
        print(f"Tax owed on this delivery: {tax_owed}")

        # Trigger overstock alert (loop exit)
        if total_inventory > 500:
            break

    # Reporting
    print("\n--- Final Report ---")
    print(f"Total Units Processed: {total_inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")


if __name__ == "__main__":
    main()