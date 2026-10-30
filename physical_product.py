from product import Product
from can_be_shipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    # New function: get_weight
    def get_weight(self):
        return self.__weight

    # New function: get_fulfilment_info
    def get_fulfilment_info(self):
        return "Physical product: requires physical shipping."

    # New function: calculate_shipping_cost
    def calculate_shipping_cost(self):
        return 5.00 + 2.00 * self.__weight

    # New function: display_information
    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")