import json
from datetime import datetime, timedelta

class LibraryManager:
    def __init__(self, database_file='library_database.json'):
        self.database_file = database_file
        self.books = self.load_data()

    def load_data(self):
        try:
            with open(self.database_file, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.database_file, 'w') as file:
            json.dump(self.books, file, indent=2)

    def add_book(self, title, author, copies_available=1):
        book_id = len(self.books) + 1
        self.books[book_id] = {
            'title': title,
            'author': author,
            'copies_available': copies_available,
            'checkout_history': []
        }
        self.save_data()

    def get_book_info(self, book_id):
        return self.books.get(book_id, None)

    def check_out_book(self, book_id):
        if book_id in self.books and self.books[book_id]['copies_available'] > 0:
            self.books[book_id]['copies_available'] -= 1
            self.books[book_id]['checkout_history'].append(datetime.now().isoformat())
            self.save_data()
            return True
        else:
            return False

    def return_book(self, book_id):
        if book_id in self.books:
            self.books[book_id]['copies_available'] += 1
            self.save_data()
            return True
        else:
            return False

    def list_all_books(self):
        return self.books

    def search_books(self, query):
        results = {}
        for book_id, book_info in self.books.items():
            if query.lower() in book_info['title'].lower() or query.lower() in book_info['author'].lower():
                results[book_id] = book_info
        return results

    def get_overdue_books(self, days=7):
        overdue_books = {}
        for book_id, book_info in self.books.items():
            if 'checkout_history' in book_info:
                last_checkout_date = book_info['checkout_history'][-1]
                last_checkout_datetime = datetime.fromisoformat(last_checkout_date)
                if datetime.now() - last_checkout_datetime > timedelta(days=days):
                    overdue_books[book_id] = book_info
        return overdue_books

# Simple terminal-based GUI
def display_menu():
    print("Library Management System")
    print("1. Add a Book")
    print("2. Check Out a Book")
    print("3. Return a Book")
    print("4. Get Book Information")
    print("5. List All Books")
    print("6. Search for Books")
    print("7. Check Overdue Books")
    print("0. Exit")

if __name__ == "__main__":
    library = LibraryManager()

    while True:
        display_menu()
        choice = input("Enter your choice (0-7): ")

        if choice == "1":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            copies = int(input("Enter the number of copies available: "))
            library.add_book(title, author, copies)

        elif choice == "2":
            book_id = int(input("Enter the ID of the book to check out: "))
            if library.check_out_book(book_id):
                print(f"Book {book_id} checked out successfully.")
            else:
                print(f"Failed to check out Book {book_id}.")

        elif choice == "3":
            book_id = int(input("Enter the ID of the book to return: "))
            if library.return_book(book_id):
                print(f"Book {book_id} returned successfully.")
            else:
                print(f"Failed to return Book {book_id}.")

        elif choice == "4":
            book_id = int(input("Enter the ID of the book to get information: "))
            book_info = library.get_book_info(book_id)
            if book_info:
                print(f"Book {book_id} information: {book_info}")
            else:
                print(f"Book {book_id} not found.")

        elif choice == "5":
            all_books = library.list_all_books()
            print("All Books:")
            for book_id, book_info in all_books.items():
                print(f"ID: {book_id}, Title: {book_info['title']}, Author: {book_info['author']}, Copies Available: {book_info['copies_available']}")

        elif choice == "6":
            search_query = input("Enter a title or author to search for: ")
            search_results = library.search_books(search_query)
            print("Search Results:")
            for book_id, book_info in search_results.items():
                print(f"ID: {book_id}, Title: {book_info['title']}, Author: {book_info['author']}, Copies Available: {book_info['copies_available']}")

        elif choice == "7":
            overdue_books = library.get_overdue_books()
            print("Overdue Books:")
            for book_id, book_info in overdue_books.items():
                print(f"ID: {book_id}, Title: {book_info['title']}, Author: {book_info['author']}, Copies Available: {book_info['copies_available']}")

        elif choice == "0":
            print("Exiting the Library Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 7.")
