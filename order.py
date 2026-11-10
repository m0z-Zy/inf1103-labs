from product import Product
from order_line import OrderLine

class Order:
    
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.order_lines:
            if order_line.product.get_product_id() == product_id:
                self.order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_information(self) -> None:
        print(f"Order {self.order_id}")
        for line in self.order_lines:
            line.display_information()
        print(f"Total: ${self.calculate_total():.2f}")