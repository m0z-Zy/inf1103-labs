from product import Product

class PhysicalProduct(Product):
   
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    # New function: get_weight
    def get_weight(self):
        return self.__weight

    # New function: get_fulfilment_info
    def get_fulfilment_info(self):
        return "Physical product: requires physical shipping."

    # New function: display_information
    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")