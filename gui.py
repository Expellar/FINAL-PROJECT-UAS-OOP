# gui.py
import pygame
from cinema_module import Cinema, Theater
from movie import Movie
from showtime import Showtime

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 128)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Cinema Management System")

# Initialize cinema data
cinema = Cinema("Grand Cinema")
theater1 = Theater(number=1, seats=30)
theater2 = Theater(number=2, seats=20)
movie1 = Movie("The Great Harding", "Action", 120)
movie2 = Movie("Sensen's Milk", "Romance", 90)
showtime1 = Showtime(movie=movie1, time="18:00")
showtime2 = Showtime(movie=movie2, time="20:00")
theater1.add_showtime(showtime1)
theater2.add_showtime(showtime2)
cinema.add_theater(theater1)
cinema.add_theater(theater2)


# Food and Beverage items with prices
fnb_items = {
    "Popcorn": 5.00,
    "Soda": 2.50,
    "Nachos": 4.00,
    "Hot Dog": 3.50,
}
cart = {}  # Dictionary to store cart items
checkout_total = 0.0  # Total cost for checkout
total_sales = {"tickets": 0, "fnb": {item: 0 for item in fnb_items}} #total sales consisting of ticket and food&beverage

# Screen states
MAIN_SCREEN = "main"
MOVIE_LIST_SCREEN = "movie_list"
SEAT_CHART_SCREEN = "seat_chart"
FOOD_SCREEN = "food"
CHECKOUT_SCREEN = "checkout"
SALES_SUMMARY_SCREEN = 5  # Tambahkan ini di bagian konstanta layar
current_screen = MAIN_SCREEN
selected_movie = None
selected_theater = None
seat_status = {}

def draw_button(screen, rect, text, color=BLUE, hover_color=GREEN):
    """Draws a button with hover effect."""
    mouse_pos = pygame.mouse.get_pos()
    current_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, current_color, rect)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_movie_list_screen():
    screen.fill(WHITE)
    title = font.render("Select a Movie:", True, BLACK)
    screen.blit(title, (200, 20))

    small_font = pygame.font.Font(None, 24)
    movie_buttons = []
    y_offset = 100

    for theater in cinema.theaters:
        for showtime in theater.showtimes:
            # Check if fully booked
            fully_booked = theater.is_fully_booked()

            # Movie button
            title_button_rect = pygame.Rect(150, y_offset, 300, 50)
            draw_button(screen, title_button_rect, showtime.movie.title, GRAY)

            # Additional info
            genre_text = small_font.render(f"Genre: {showtime.movie.genre}", True, BLACK)
            time_text = small_font.render(f"Showtime: {showtime.time}", True, BLACK)

            screen.blit(genre_text, (160, y_offset + 55))
            screen.blit(time_text, (160, y_offset + 75))

            # Show "Fully Booked" if theater is full
            if fully_booked:
                fb_text = small_font.render("Fully Booked", True, RED)
                screen.blit(fb_text, (400, y_offset + 20))

            movie_buttons.append((title_button_rect, showtime.movie, theater))
            y_offset += 100

    back_button = pygame.Rect(50, 400, 100, 40)
    draw_button(screen, back_button, "Back", BLUE)
    return movie_buttons, back_button

def draw_main_screen():
    screen.fill(WHITE)
    view_movies_button = pygame.Rect(175, 150, 250, 50)
    food_bev_button = pygame.Rect(175, 250, 250, 50)
    exit_button = pygame.Rect(175, 350, 250, 50)
    draw_button(screen, view_movies_button, "View Movies")
    draw_button(screen, food_bev_button, "Food & Beverages")
    draw_button(screen, exit_button, "Exit", RED)
    return view_movies_button, food_bev_button, exit_button

def draw_movie_list_screen():
    screen.fill(WHITE)
    title = font.render("Select a Movie:", True, BLACK)
    screen.blit(title, (200, 20))

    # Define a smaller font for genre and showtime information
    small_font = pygame.font.Font(None, 24)

    movie_buttons = []
    y_offset = 100  # Starting y position for movie entries

    # Loop through the theaters and showtimes to list all movies
    for theater in cinema.theaters:
        for showtime in theater.showtimes:
            # Movie button for title
            title_button_rect = pygame.Rect(150, y_offset, 300, 50)
            draw_button(screen, title_button_rect, showtime.movie.title, GRAY)

            # Render genre and showtime in smaller font below the title
            genre_text = small_font.render(f"Genre: {showtime.movie.genre}", True, BLACK)
            time_text = small_font.render(f"Showtime: {showtime.time}", True, BLACK)

            # Position genre and time below the title button
            screen.blit(genre_text, (160, y_offset + 55))
            screen.blit(time_text, (160, y_offset + 75))

            # Store the button and details for click detection
            movie_buttons.append((title_button_rect, showtime.movie, theater))
            y_offset += 100  # Increase y_offset to space out each movie entry

    # Draw a back button at the bottom
    back_button = pygame.Rect(50, 400, 100, 40)
    draw_button(screen, back_button, "Back", BLUE)
    return movie_buttons, back_button

def draw_seat_chart_screen(theater):
    screen.fill(WHITE)
    title = font.render(f"Seating Chart - Theater {theater.number}", True, BLACK)
    screen.blit(title, (150, 20))

    seat_buttons = []
    cols, rows = 6, theater.seats // 6  # Example seating arrangement
    global seat_status

    # Initialize seat status if not done already
    if theater.number not in seat_status:
        seat_status[theater.number] = {seat_num: None for seat_num in range(1, theater.seats + 1)}  # None means unbooked

    for row in range(rows):
        for col in range(cols):
            seat_num = row * cols + col + 1
            if seat_status[theater.number][seat_num] is None:
                seat_color = GREEN  # Available seat
            elif seat_status[theater.number][seat_num] == "current_user":
                seat_color = BLUE  # Seat booked by current user
            else:
                seat_color = RED  # Seat booked by another user

            seat_rect = pygame.Rect(50 + col * 50, 100 + row * 50, 40, 40)
            pygame.draw.rect(screen, seat_color, seat_rect)
            seat_buttons.append((seat_rect, seat_num))

    back_button = pygame.Rect(50, 400, 100, 40)
    draw_button(screen, back_button, "Back", BLUE)
    return seat_buttons, back_button

def draw_food_screen():
    screen.fill(WHITE)
    title = font.render("Food & Beverages", True, BLACK)
    screen.blit(title, (200, 20))

    item_buttons = []
    y_offset = 100
    for item, price in fnb_items.items():
        item_button = pygame.Rect(150, y_offset, 300, 50)
        draw_button(screen, item_button, f"{item} - ${price:.2f}", GRAY)
        item_buttons.append((item_button, item))
        y_offset += 80

    checkout_button = pygame.Rect(200, 400, 200, 50)
    draw_button(screen, checkout_button, "Checkout", GREEN)
    back_button = pygame.Rect(50, 400, 100, 40)
    draw_button(screen, back_button, "Back", BLUE)
    return item_buttons, checkout_button, back_button

def draw_checkout_screen():
    screen.fill(WHITE)
    title = font.render("Checkout", True, BLACK)
    screen.blit(title, (250, 20))

    # Display cart items and quantities
    y_offset = 100
    delete_buttons = []  # Store delete buttons for each item
    for item, quantity in cart.items():
        item_text = f"{item} x{quantity} - ${fnb_items[item] * quantity:.2f}"
        item_label = font.render(item_text, True, BLACK)
        screen.blit(item_label, (150, y_offset))

        # Add delete button for each item
        delete_button = pygame.Rect(450, y_offset, 100, 30)
        draw_button(screen, delete_button, "Remove", RED)
        delete_buttons.append((delete_button, item))
        
        y_offset += 50

    # Display total
    total_label = font.render(f"Total: ${checkout_total:.2f}", True, RED)
    screen.blit(total_label, (200, y_offset + 50))

    # Add back button
    back_button = pygame.Rect(50, 400, 100, 40)
    draw_button(screen, back_button, "Back", BLUE)

    # Tombol untuk melihat Sales Summary
    sales_summary_button = pygame.Rect(250, 400, 200, 40)
    draw_button(screen, sales_summary_button, "View Sales", GREEN)
    return delete_buttons, back_button, sales_summary_button


def calculate_total():
    global checkout_total
    checkout_total = sum(fnb_items[item] * quantity for item, quantity in cart.items())

def display_sales_summary():
    screen.fill(WHITE)
    title = font.render("Sales Summary", True, BLACK)
    screen.blit(title, (200, 20))

    y_offset = 100
    for item, quantity in total_sales["fnb"].items():
        sales_text = f"{item}: {quantity} sold"
        sales_label = font.render(sales_text, True, BLACK)
        screen.blit(sales_label, (150, y_offset))
        y_offset += 50

    ticket_label = font.render(f"Tickets Sold: {total_sales['tickets']}", True, BLACK)
    screen.blit(ticket_label, (150, y_offset + 50))

    back_button = pygame.Rect(50, 400, 100, 40)
    draw_button(screen, back_button, "Back", BLUE)
    return back_button


def run_gui():
    global current_screen, selected_movie, selected_theater, seat_status, checkout_total
    running = True

    while running:
        screen.fill(WHITE)

        # Draw appropriate screen based on current state
        if current_screen == MAIN_SCREEN:
            view_movies_button, food_bev_button, exit_button = draw_main_screen()
        
        elif current_screen == MOVIE_LIST_SCREEN:
            movie_buttons, back_button = draw_movie_list_screen()
        
        elif current_screen == SEAT_CHART_SCREEN and selected_theater:
            seat_buttons, back_button = draw_seat_chart_screen(selected_theater)
        
        elif current_screen == FOOD_SCREEN:
            item_buttons, checkout_button, back_button = draw_food_screen()

        elif current_screen == CHECKOUT_SCREEN:
            delete_buttons, back_button, sales_summary_button = draw_checkout_screen()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == MAIN_SCREEN:
                    if view_movies_button.collidepoint(event.pos):
                        current_screen = MOVIE_LIST_SCREEN
                    elif food_bev_button.collidepoint(event.pos):
                        current_screen = FOOD_SCREEN
                    elif exit_button.collidepoint(event.pos):
                        running = False

                elif current_screen == MOVIE_LIST_SCREEN:
                    for button_rect, movie, theater in movie_buttons:
                        if button_rect.collidepoint(event.pos):
                            selected_movie = movie
                            selected_theater = theater
                            current_screen = SEAT_CHART_SCREEN
                    if back_button.collidepoint(event.pos):
                        current_screen = MAIN_SCREEN

                elif current_screen == SEAT_CHART_SCREEN:
                    for seat_rect, seat_num in seat_buttons:
                        if seat_rect.collidepoint(event.pos) and seat_status[selected_theater.number][seat_num] is None:
                            seat_status[selected_theater.number][seat_num] = "current_user"  # Mark seat as booked by current user
                            selected_theater.book_seat(1)
                    if back_button.collidepoint(event.pos):
                        current_screen = MOVIE_LIST_SCREEN

                elif current_screen == FOOD_SCREEN:
                    for item_button, item in item_buttons:
                        if item_button.collidepoint(event.pos):
                            cart[item] = cart.get(item, 0) + 1
                    if checkout_button.collidepoint(event.pos):
                        calculate_total()
                        current_screen = CHECKOUT_SCREEN
                    elif back_button.collidepoint(event.pos):
                        current_screen = MAIN_SCREEN

                elif current_screen == CHECKOUT_SCREEN:
                    delete_buttons, back_button, sales_summary_button = draw_checkout_screen()

                    for button, item in delete_buttons:
                        if button.collidepoint(event.pos):
                            cart[item] -= 1
                            if cart[item] == 0:
                                del cart[item]  # Remove item if quantity is 0
                            calculate_total()  # Recalculate total
                            break  # Keluar dari loop setelah perubahan cart

                    if back_button.collidepoint(event.pos):
                        current_screen = FOOD_SCREEN  # Kembali ke layar sebelumnya
                    elif sales_summary_button.collidepoint(event.pos):
                        current_screen = SALES_SUMMARY_SCREEN  # Pindah ke layar Sales Summary

                    elif current_screen == SALES_SUMMARY_SCREEN:
                            back_button = display_sales_summary()
                            if back_button.collidepoint(event.pos):
                                current_screen = CHECKOUT_SCREEN  # Kembali ke layar Checkout



        pygame.display.flip()

    pygame.quit()

# Run the GUI
run_gui()
