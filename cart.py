# cart.py

class FoodAndBeverageItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.items = []  # Aggregation: Cart "has-a" FoodAndBeverageItem

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.price for item in self.items)

    def show_items(self):
        if not self.items:
            print("Keranjang kosong.")
        else:
            print("Items in cart:")
            for item in self.items:
                print(f"- {item.name}: ${item.price:.2f}")
