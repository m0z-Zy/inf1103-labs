# Prompts the user and validates their entry.
# Returns an int if valid, "quit" to stop, or None if rejected.
def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()

    if user_input.lower() == "quit":
        return "quit"

    is_negative = user_input.startswith('-')
    digits_only = user_input[1:] if is_negative else user_input

    if digits_only == "" or not digits_only.isdigit():
        print(f"Error: '{user_input}' is not a valid integer. Entry rejected.")
        return None

    quantity = int(user_input)

    if quantity < 0:
        print(f"Error: Negative quantities are not allowed ({quantity}). Entry rejected.")
        return None

    return quantity


# Adds a delivery to the running total and returns the new total.
def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


# Returns the tax on a single delivery (10% of the amount).
def calculate_tax(amount):
    tax = amount * 0.10
    return tax


# Prints the final summary of processed units and rejected entries.
def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


# Runs the input loop, tracks the counters, and calls the report.
def main():
    total_inventory = 0
    failed_entries = 0
    total_tax = 0.0

    while True:
        result = get_valid_input()

        if result == "quit":
            break

        if result is None:
            failed_entries += 1
            continue

        quantity = result

        total_inventory = process_delivery(total_inventory, quantity)
        delivery_tax = calculate_tax(quantity)
        total_tax += delivery_tax

        print(f"Added {quantity} units. Current total inventory: {total_inventory}")
        print(f"  Tax on this delivery: {delivery_tax:.2f}")

        if total_inventory > 500:
            print(f"ALERT: Overstock! Total inventory ({total_inventory}) exceeds 500 units.")
            break

    generate_report(total_inventory, failed_entries)
    print(f"Total Tax Collected: {total_tax:.2f}")


if __name__ == "__main__":
    main()