import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S01", "TechSource Ltd", "sales@techsource.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P01", "Laptop", 1200.0, 15, self.supplier, 2.1)
        self.assertIsInstance(product, PhysicalProduct)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D01", "Antivirus", 50.0, 25, self.supplier, 10000.0)
        self.assertIsInstance(product, DigitalProduct)

    def test_returns_the_product_type(self):
        product = ProductFactory.create("physical", "P01", "Laptop", 1200.0, 15, self.supplier, 2.1)
        self.assertIsInstance(product, Product)

    def test_unknown_product_type_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S01", "Installation", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type: service", str(context.exception))


if __name__ == "__main__":
    unittest.main()