from product import Product
from supplier import Supplier

class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> int:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered digitally via download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")