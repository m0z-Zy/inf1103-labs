import unittest

from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount_strategy import (DiscountStrategy, NoDiscount,
                               PercentageDiscount, BulkDiscount)
from student_discount import StudentDiscount


def make_order_of_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S01", "TechSource Ltd", "sales@techsource.com")
    item = PhysicalProduct("P01", "Item", 50.00, 10, 1.0, supplier)
    order = Order("O1", discount)
    order.add_order_line(item, 5)   # 5 x 50 = 250
    return order


class TestDiscountStrategies(unittest.TestCase):

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount_takes_percent_off(self):
        self.assertEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_applies_at_or_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)

    def test_bulk_discount_not_applied_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199), 199)

    def test_student_discount_takes_5_percent_off(self):
        self.assertAlmostEqual(StudentDiscount().apply(200), 190)


class TestOrderUsesStrategy(unittest.TestCase):

    def test_order_defaults_to_no_discount(self):
        self.assertEqual(make_order_of_250().calculate_total(), 250)

    def test_order_uses_the_strategy_it_is_given(self):
        order = make_order_of_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order_of_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_new_strategy_works_without_changing_order(self):
        order = make_order_of_250(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)


if __name__ == "__main__":
    unittest.main()