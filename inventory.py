from product import Product

class Inventory:

    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 47)
        for product in self.__products:
            product.display_information()
        print("-" * 47)

    def is_empty(self):
        return len(self.__products) == 0

    def to_dict_list(self):
        return [product.to_dict() for product in self.__products]