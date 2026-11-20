import unittest

from supplier import Supplier
from product_factory import ProductFactory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from order_line import OrderLine


class TestProductValidation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S01", "TechSource Ltd", "sales@techsource.com")

    def test_zero_price_is_rejected(self):
        with self.assertRaises(ValueError) as context:
            PhysicalProduct("P01", "Laptop", 0, 5, 2.1, self.supplier)
        self.assertIn("Price must be greater than zero", str(context.exception))

    def test_negative_price_is_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P01", "Laptop", -10.0, 5, 2.1, self.supplier)

    def test_negative_stock_is_rejected(self):
        with self.assertRaises(ValueError) as context:
            PhysicalProduct("P01", "Laptop", 10.0, -1, 2.1, self.supplier)
        self.assertIn("Stock quantity cannot be negative", str(context.exception))

    def test_zero_stock_is_allowed(self):
        product = PhysicalProduct("P01", "Laptop", 10.0, 0, 2.1, self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_digital_product_follows_the_same_rules(self):
        with self.assertRaises(ValueError):
            DigitalProduct("D01", "Antivirus", -1.0, 5, 100.0, self.supplier)
        with self.assertRaises(ValueError):
            DigitalProduct("D01", "Antivirus", 5.0, -5, 100.0, self.supplier)

    def test_factory_passes_validation_through(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D01", "Antivirus", 0, 5, self.supplier, 100.0)

    def test_update_stock_rejects_negative(self):
        product = DigitalProduct("D01", "Antivirus", 5.0, 5, 100.0, self.supplier)
        with self.assertRaises(ValueError):
            product.update_stock(-1)
        self.assertEqual(product.get_stock(), 5)


class TestOrderLineValidation(unittest.TestCase):

    def setUp(self):
        supplier = Supplier("S01", "TechSource Ltd", "sales@techsource.com")
        self.product = PhysicalProduct("P01", "Laptop", 10.0, 5, 2.1, supplier)

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(ValueError) as context:
            OrderLine(self.product, 0)
        self.assertIn("Quantity must be greater than zero", str(context.exception))

    def test_negative_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            OrderLine(self.product, -3)

    def test_valid_quantity_is_accepted(self):
        self.assertEqual(OrderLine(self.product, 2).calculate_subtotal(), 20.0)

    def test_order_rejects_invalid_line_and_stays_unchanged(self):
        order = Order("O1")
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, 0)
        self.assertEqual(len(order.order_lines), 0)


if __name__ == "__main__":
    unittest.main()