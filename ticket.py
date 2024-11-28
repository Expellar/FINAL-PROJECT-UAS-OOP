# ticket.py
class Ticket:
    def __init__(self, price):
        self.price = price

    def get_price(self):
        return self.price


class RegularTicket(Ticket):
    def get_price(self):
        return super().get_price()


class VIPTicket(Ticket):
    def get_price(self):
        return super().get_price() * 1.5
