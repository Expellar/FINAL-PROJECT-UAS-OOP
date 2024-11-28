from cinema_module import Cinema, Theater
from person import Manager, Customer
from movie import Movie
from showtime import Showtime
from ticket import RegularTicket, VIPTicket
from cart import Cart, FoodAndBeverageItem

# Data Global
cart = Cart()
total_sales = {"tickets": 0}

# Contoh Inheritance
manager = Manager("Alice", 35, "M101")
customer = Customer("Bob", 28)

# Composition Example
cinema = Cinema("Grand Cinema")
theater1 = Theater(1, 50)
cinema.add_theater(theater1)

# Tambahkan Film
movie1 = Movie("The Great Adventure", "Action", 120)
showtime1 = Showtime(movie=movie1, time="18:00")
theater1.add_showtime(showtime1)

# Menu Utama
def main_menu():
    while True:
        print("\n=== Cinema Management System ===")
        print("1. Lihat Daftar Film")
        print("2. Pesan Kursi")
        print("3. Beli Makanan/Minuman")
        print("4. Lihat Ringkasan Penjualan")
        print("5. Keluar")
        choice = input("Pilih opsi (1-5): ")

        if choice == "1":
            view_movies()
        elif choice == "2":
            book_seat()
        elif choice == "3":
            buy_fnb()
        elif choice == "4":
            view_sales_summary()
        elif choice == "5":
            print("Terima kasih telah menggunakan sistem ini!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Fungsi Melihat Daftar Film
def view_movies():
    print("\n=== Daftar Film ===")
    for theater in cinema.theaters:
        print(f"\nTheater {theater.number}:")
        for showtime in theater.showtimes:
            print(f"- {showtime.movie.title} ({showtime.movie.genre}, {showtime.movie.duration} menit) - {showtime.time}")

# Fungsi Pemesanan Kursi
def book_seat():
    theater_number = int(input("Masukkan nomor theater: "))
    theater = next((t for t in cinema.theaters if t.number == theater_number), None)

    if not theater:
        print("Theater tidak ditemukan!")
        return

    print(f"\n=== Pesan Kursi di Theater {theater.number} ===")
    if theater.is_fully_booked():
        print("Semua kursi telah dipesan!")
        return

    num_seats = int(input(f"Jumlah kursi yang ingin dipesan (tersedia: {theater.available_seats}): "))
    try:
        theater.book_seat(num_seats)
        total_sales["tickets"] += num_seats
        print(f"Berhasil memesan {num_seats} kursi!")
    except ValueError as e:
        print(e)

# Fungsi Pembelian Makanan/Minuman
def buy_fnb():
    fnb_items = {
        "Popcorn": 5.00,
        "Soda": 2.50,
        "Nachos": 4.00,
        "Hot Dog": 3.50,
    }
    print("\n=== Menu Makanan/Minuman ===")
    for i, (item, price) in enumerate(fnb_items.items(), start=1):
        print(f"{i}. {item} - ${price:.2f}")

    choice = int(input("Pilih item (1-4): "))
    item_name = list(fnb_items.keys())[choice - 1]
    item_price = fnb_items[item_name]
    quantity = int(input(f"Jumlah {item_name} yang ingin dibeli: "))

    # Tambahkan item ke Cart
    for _ in range(quantity):
        cart.add_item(FoodAndBeverageItem(item_name, item_price))

    print(f"{quantity} {item_name} berhasil ditambahkan ke keranjang!")

# Fungsi Melihat Ringkasan Penjualan
def view_sales_summary():
    print("\n=== Ringkasan Penjualan ===")
    print(f"Total Tiket Terjual: {total_sales['tickets']} tiket")
    print("Makanan/Minuman Terjual:")
    cart.show_items()
    print(f"Total Harga Makanan/Minuman: ${cart.calculate_total():.2f}")

# Menjalankan Menu Utama
if __name__ == "__main__":
    print(manager.get_details())
    print(customer.get_details())
    main_menu()
