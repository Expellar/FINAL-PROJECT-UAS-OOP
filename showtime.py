# showtime.py
from movie import Movie

class Showtime:
    def __init__(self, movie, time):
        if not isinstance(movie, Movie):
            raise TypeError("Invalid movie type.")
        self.movie = movie
        self.time = time
