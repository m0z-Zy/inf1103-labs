from abc import ABC, abstractmethod

class CanBeShipped(ABC):

    # New function: calculate_shipping_cost
    @abstractmethod
    def calculate_shipping_cost(self):
        pass