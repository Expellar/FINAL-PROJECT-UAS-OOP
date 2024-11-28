from abc import ABC, abstractmethod

class AbstractTicket(ABC):
    """Abstract Base Class for Tickets"""
    def __init__(self, price):
        self.price = price

    @abstractmethod
    def get_price(self):
        """Abstract method to get the price of a ticket."""
        pass

class RegularTicket(AbstractTicket):
    def get_price(self):
        return self.price

class VIPTicket(AbstractTicket):
    def get_price(self):
        return self.price * 1.5
