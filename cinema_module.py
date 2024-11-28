# cinema.py
class Cinema:
    def __init__(self, name):
        self.name = name
        self.theaters = []

    def add_theater(self, theater):
        self.theaters.append(theater)


class Theater:
    def __init__(self, number, seats):
        self.number = number
        self.seats = seats
        self.available_seats = seats
        self.showtimes = []

    def add_showtime(self, showtime):
        self.showtimes.append(showtime)

    def book_seat(self, num_seats):
        if num_seats > self.available_seats:
            raise ValueError("Not enough seats available")
        self.available_seats -= num_seats
        print(f"Successfully booked {num_seats} seats.")

    def is_fully_booked(self):
        """Returns True if all seats are booked."""
        return self.available_seats <= 0
