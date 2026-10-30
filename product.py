class Product:
 
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # New function: get_product_id
    def get_product_id(self):
        return self.__product_id

    # New function: get_name
    def get_name(self):
        return self.__name

    # New function: get_price
    def get_price(self):
        return self.__price

    # New function: get_stock
    def get_stock(self):
        return self.__stock

    # New function: update_stock
    def update_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    # New function: display_information
    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # New function: to_dict
    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
