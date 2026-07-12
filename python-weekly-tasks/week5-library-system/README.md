# Library Management System

## Project Description
A comprehensive library management system built using Object-Oriented Programming (OOP) principles. This system allows librarians to manage books, members, and borrowing operations efficiently through a simple command-line interface, with all data persisted to JSON files between sessions.

## What I Learned
- **OOP Principles**: Classes, objects, and encapsulation
- **Class Design**: How to design classes for real-world systems (`Book`, `Member`, `Library`)
- **Class Relationships**: How the `Library` class composes and coordinates `Book` and `Member` objects
- **Method Implementation**: Creating methods that model real behaviors (checking out, returning, searching)
- **Data Persistence**: Saving and loading object data to/from JSON files
- **Testing**: Writing unit tests with `unittest` to verify each class independently

## Features
- ✅ Add, remove, and search for books
- ✅ Register and manage library members
- ✅ Borrow and return books with due dates
- ✅ Track overdue books and calculate days overdue
- ✅ Search books by title, author, or ISBN
- ✅ Limit maximum books per member (default: 5)
- ✅ Save/load data to JSON files
- ✅ Timestamped backups of data files
- ✅ User-friendly menu interface
- ✅ Comprehensive error handling (missing files, invalid input, duplicate records)

## Project Structure
```
week5-library-system/
│── library_system/
│   ├── __init__.py
│   ├── book.py        # Book class
│   ├── member.py       # Member class
│   ├── library.py      # Library class (manages books, members, persistence)
│   └── main.py          # CLI menu system (entry point)
│── data/
│   ├── books.json       # Sample book data
│   ├── members.json     # Sample member data
│   └── backup/          # Timestamped backups saved here
│── tests/
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
│── requirements.txt
│── README.md
└── .gitignore
```

## Class Structure

### `Book`
Attributes: `title`, `author`, `isbn`, `year`, `available`, `borrowed_by`, `due_date`, `date_added`
Key methods: `check_out()`, `return_book()`, `is_overdue()`, `days_overdue()`, `to_dict()` / `from_dict()`

### `Member`
Attributes: `name`, `member_id`, `borrowed_books`, `max_books` (default 5), `date_joined`
Key methods: `borrow_book()`, `return_book()`, `can_borrow()`, `to_dict()` / `from_dict()`

### `Library`
Attributes: `books` (dict keyed by ISBN), `members` (dict keyed by member ID)
Key methods: `add_book()`, `remove_book()`, `find_book()`, `search_books()`, `register_member()`, `find_member()`, `borrow_book()`, `return_book()`, `get_statistics()`, `save_all()` / `load_all()`, `backup_data()`

The `Library` class coordinates between `Book` and `Member`: when a book is borrowed, `Library.borrow_book()` calls `Book.check_out()` **and** `Member.borrow_book()` together, keeping both objects in sync.

## Setup Instructions
1. Make sure you have **Python 3.8+** installed.
2. No external dependencies are required — the project uses only the Python standard library.
3. (Optional) create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   ```

## How to Run
From the `week5-library-system` directory:
```bash
python -m library_system.main
```

## How to Run Tests
```bash
python -m unittest discover -s tests -v
```
All 33 unit tests should pass, covering `Book`, `Member`, and `Library` (including borrowing/returning workflows, search, statistics, and JSON persistence).

## Sample Menu
```
================================
    LIBRARY MANAGEMENT SYSTEM
================================
1. Add New Book
2. Register New Member
3. Borrow Book
4. Return Book
5. Search Books
6. View All Books
7. View All Members
8. View Overdue Books
9. Save & Exit
0. Exit Without Saving

Enter your choice:
```

## Sample Output
```
Search Results for 'python':
----------------------------------------
1. Python Crash Course
   Author: Eric Matthes
   ISBN: 9781593279288
   Year: 2019
   Status: Available

2. Automate the Boring Stuff with Python
   Author: Al Sweigart
   ISBN: 9781593275990
   Year: 2015
   Status: Borrowed by MEM001 (Due: 2024-02-15)

Found 2 book(s) matching 'python'

Library Statistics:
- Total Books: 3
- Available Books: 2
- Total Members: 2
- Books Borrowed: 1
- Overdue Books: 0
```

## Technical Notes
- **Data structures**: `books` and `members` are stored as dictionaries in `Library` (keyed by ISBN and member ID respectively) for O(1) lookup by ID.
- **Persistence**: Data is serialized to JSON via `to_dict()`/`from_dict()` class methods on `Book` and `Member`, keeping serialization logic close to the data it serializes.
- **Overdue calculation**: `Book.is_overdue()` compares the stored `due_date` string against the current date; `days_overdue()` returns the exact day count.
- **Error handling**: File operations are wrapped in try/except blocks for `IOError`/`OSError`/`json.JSONDecodeError`, and missing files are handled gracefully by starting with an empty collection rather than crashing.
- **Backups**: `Library.backup_data()` copies the current `books.json` and `members.json` into `data/backup/` with a timestamp in the filename, so previous save states aren't overwritten.

## Testing Evidence
See `tests/` for unit tests covering:
- Book checkout/return, overdue detection, and serialization round-trips
- Member borrowing limits and duplicate-borrow prevention
- Library-level search (by title/author/ISBN), statistics, save/load, and backups

Run `python -m unittest discover -s tests -v` to see all 33 tests pass.
