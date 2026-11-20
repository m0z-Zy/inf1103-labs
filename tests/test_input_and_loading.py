import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from inventory import Inventory
from supplier import Supplier
from input_helpers import get_positive_float
from product_loader import load_products

CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


def run_and_capture(function, *args) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        function(*args)
    return buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):

    def test_asks_again_until_value_is_valid(self):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with contextlib.redirect_stdout(buffer):
                result = get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        output = buffer.getvalue().splitlines()
        self.assertEqual(output, ["Please enter a valid number, e.g. 12.50",
                                  "Please enter a number greater than zero."])

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 3.0)


class TestLoadProducts(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S01", "TechSource Ltd", "sales@techsource.com")
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "products.csv")
        with open(self.path, "w", newline="") as f:
            f.write(CSV_TEXT)

    def tearDown(self):
        self.folder.cleanup()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        inventory = Inventory()
        output = run_and_capture(load_products, self.path, inventory, self.supplier)
        ids = sorted(p.get_product_id() for p in inventory.get_products())
        self.assertEqual(ids, ["D001", "P001", "P003"])
        self.assertIn("3 products loaded.", output)

    def test_bad_rows_are_reported(self):
        output = run_and_capture(load_products, self.path, Inventory(), self.supplier)
        self.assertIn("Skipped row 4: Unknown product type: service", output)
        self.assertIn("Skipped row 5:", output)

    def test_finally_message_prints_last(self):
        output = run_and_capture(load_products, self.path, Inventory(), self.supplier)
        self.assertEqual(output.splitlines()[-1], "Load attempt finished.")

    def test_missing_file_is_handled_without_crashing(self):
        inventory = Inventory()
        output = run_and_capture(load_products, "no_such_file.csv", inventory, self.supplier)
        self.assertIn("Products file not found: no_such_file.csv", output)
        self.assertNotIn("products loaded", output)
        self.assertIn("Load attempt finished.", output)
        self.assertTrue(inventory.is_empty())

    def test_short_row_is_skipped(self):
        with open(self.path, "a", newline="") as f:
            f.write("physical,P004\n")
        inventory = Inventory()
        output = run_and_capture(load_products, self.path, inventory, self.supplier)
        self.assertIn("Skipped row 7:", output)
        self.assertIn("3 products loaded.", output)

    def test_duplicate_id_is_skipped(self):
        with open(self.path, "a", newline="") as f:
            f.write("physical,P001,Copy,5.00,1\n")
        output = run_and_capture(load_products, self.path, Inventory(), self.supplier)
        self.assertIn("duplicate product ID P001", output)
        self.assertIn("3 products loaded.", output)


if __name__ == "__main__":
    unittest.main()