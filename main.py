# main.py
from cinema_module import Cinema, Theater
from movie import Movie
from showtime import Showtime
from ticket import RegularTicket, VIPTicket
import gui

def main():
    # Initialize cinema, theaters, movies, and showtimes
    cinema = Cinema("Sensen's Milk")

    theater1 = Theater(number=1, seats=100)
    theater2 = Theater(number=2, seats=80)
    cinema.add_theater(theater1)
    cinema.add_theater(theater2)

    # Add movies and showtimes
    movie1 = Movie("The Great Adventure", "Action", 120)
    movie2 = Movie("Love Story", "Romance", 90)

    showtime1 = Showtime(movie=movie1, time="18:00")
    showtime2 = Showtime(movie=movie2, time="20:00")
    theater1.add_showtime(showtime1)
    theater2.add_showtime(showtime2)

    # Start the GUI
    gui.run_gui()

if __name__ == "__main__":
    main()
