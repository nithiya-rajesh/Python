"""
main.py
User-facing menu system for the Library Management System.
Run with: python -m library_system.main
"""

from library import Library


def print_header():
    print("=" * 32)
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("=" * 32)


def print_menu():
    print("\n1. Add New Book")
    print("2. Register New Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. View All Books")
    print("7. View All Members")
    print("8. View Overdue Books")
    print("9. Save & Exit")
    print("0. Exit Without Saving")


def prompt(text):
    return input(text).strip()


def prompt_int(text, default=None):
    raw = input(text).strip()
    if raw == '' and default is not None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


# ----------------------------------------------------------------------
# Menu actions
# ----------------------------------------------------------------------
def action_add_book(library):
    print("\n--- Add New Book ---")
    title = prompt("Title: ")
    author = prompt("Author: ")
    isbn = prompt("ISBN: ")
    year_raw = prompt("Year (optional): ")
    year = int(year_raw) if year_raw.isdigit() else None

    if not title or not author or not isbn:
        print("Title, author, and ISBN are required.")
        return

    success, message = library.add_book(title, author, isbn, year)
    print(message)


def action_register_member(library):
    print("\n--- Register New Member ---")
    name = prompt("Name: ")
    member_id = prompt("Member ID: ")
    max_books = prompt_int("Max books allowed (default 5): ", default=5)

    if not name or not member_id:
        print("Name and Member ID are required.")
        return

    success, message = library.register_member(name, member_id, max_books)
    print(message)


def action_borrow_book(library):
    print("\n--- Borrow Book ---")
    isbn = prompt("Book ISBN: ")
    member_id = prompt("Member ID: ")
    loan_period = prompt_int("Loan period in days (default 14): ", default=14)

    success, message = library.borrow_book(isbn, member_id, loan_period)
    print(message)


def action_return_book(library):
    print("\n--- Return Book ---")
    isbn = prompt("Book ISBN: ")

    success, message = library.return_book(isbn)
    print(message)


def action_search_books(library):
    print("\nSearch books by:")
    print("1. Title")
    print("2. Author")
    print("3. ISBN")
    print("4. Show all available books")
    choice = prompt("\nEnter search option: ")

    if choice == '4':
        results = library.available_books()
        print(f"\n{len(results)} book(s) currently available")
        display_books(results)
        return

    field_map = {'1': 'title', '2': 'author', '3': 'isbn'}
    field = field_map.get(choice)
    if not field:
        print("Invalid option.")
        return

    query = prompt(f"\nEnter {field} to search: ")
    results = library.search_books(query, field)

    print(f"\nSearch Results for '{query}':")
    print("-" * 40)
    if not results:
        print("No matches found.")
    else:
        display_books(results)
    print(f"\nFound {len(results)} book(s) matching '{query}'")


def action_view_all_books(library):
    print("\n--- All Books ---")
    books = list(library.books.values())
    if not books:
        print("No books in the library yet.")
        return
    display_books(books)


def action_view_all_members(library):
    print("\n--- All Members ---")
    members = list(library.members.values())
    if not members:
        print("No members registered yet.")
        return
    for i, member in enumerate(members, 1):
        print(f"{i}. {member}")


def action_view_overdue(library):
    print("\n--- Overdue Books ---")
    overdue = library.overdue_books()
    if not overdue:
        print("No overdue books. Nice!")
        return
    for i, book in enumerate(overdue, 1):
        print(f"{i}. {book.title} (ISBN: {book.isbn}) - "
              f"{book.days_overdue()} day(s) overdue, borrowed by {book.borrowed_by}")


def display_books(books):
    for i, book in enumerate(books, 1):
        print(f"\n{i}. {book.title}")
        print(f"   Author: {book.author}")
        print(f"   ISBN: {book.isbn}")
        if book.year:
            print(f"   Year: {book.year}")
        status = "Available" if book.available else f"Borrowed by {book.borrowed_by} (Due: {book.due_date})"
        print(f"   Status: {status}")


def display_statistics(library):
    stats = library.get_statistics()
    print("\nLibrary Statistics:")
    print(f"- Total Books: {stats['total_books']}")
    print(f"- Available Books: {stats['available_books']}")
    print(f"- Total Members: {stats['total_members']}")
    print(f"- Books Borrowed: {stats['books_borrowed']}")
    print(f"- Overdue Books: {stats['overdue_books']}")


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------
def main():
    print_header()

    library = Library()
    ok, message = library.load_all()
    print(message)

    actions = {
        '1': action_add_book,
        '2': action_register_member,
        '3': action_borrow_book,
        '4': action_return_book,
        '5': action_search_books,
        '6': action_view_all_books,
        '7': action_view_all_members,
        '8': action_view_overdue,
    }

    while True:
        print_menu()
        choice = prompt("\nEnter your choice: ")

        if choice in actions:
            actions[choice](library)
        elif choice == '9':
            library.backup_data()
            ok, message = library.save_all()
            print(message)
            display_statistics(library)
            print("\nGoodbye!")
            break
        elif choice == '0':
            print("\nExiting without saving. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()
