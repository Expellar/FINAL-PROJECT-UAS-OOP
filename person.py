# person.py

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_details(self):
        return f"{self.name}, {self.age} years old"

class Manager(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id

    def get_details(self):
        return f"Manager {super().get_details()}, ID: {self.employee_id}"

class Customer(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.tickets = []  # List of tickets bought by the customer

    def buy_ticket(self, ticket):
        self.tickets.append(ticket)
        print(f"{self.name} bought a ticket for {ticket.showtime.movie.title}")
