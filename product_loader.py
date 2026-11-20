import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

# Expected columns: product_type,product_id,name,price,stock_quantity
def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                try:
                    product = ProductFactory.create(row[0].strip(), row[1].strip(),
                                                    row[2].strip(), float(row[3]),
                                                    int(row[4]), supplier)
                except (ValueError, IndexError) as error:
                    # ValueError: unknown type, bad number, or a failed validation rule
                    # IndexError: the row has fewer columns than expected
                    print(f"Skipped row {line_number}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipped row {line_number}: duplicate product ID {row[1].strip()}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")