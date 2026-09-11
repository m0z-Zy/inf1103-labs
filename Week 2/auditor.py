def main():
    total_inventory = 0
    failed_entries = 0

    while True:
        user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()

        # Exit condition
        if user_input.lower() == "quit":
            break

        # Strip a leading '-' so we can still validate the digits,
        # but remember whether the original value was negative.
        is_negative = user_input.startswith('-')
        digits_only = user_input[1:] if is_negative else user_input

        # Handle invalid input (e.g. "ten") using isdigit()
        if digits_only == "" or not digits_only.isdigit():
            print(f"Error: '{user_input}' is not a valid integer. Entry rejected.")
            failed_entries += 1
            continue

        quantity = int(user_input)

        # Enforce business rules: no negative numbers
        if quantity < 0:
            print(f"Error: Negative quantities are not allowed ({quantity}). Entry rejected.")
            failed_entries += 1
            continue

        # Manage state: running total
        total_inventory += quantity
        print(f"Added {quantity} units. Current total inventory: {total_inventory}")

        # Trigger overstock alert
        if total_inventory > 500:
            print(f"ALERT: Overstock! Total inventory ({total_inventory}) exceeds 500 units.")
            break

    # Reporting
    print("\n--- Final Report ---")
    print(f"Total Units Processed: {total_inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")


if __name__ == "__main__":
    main()