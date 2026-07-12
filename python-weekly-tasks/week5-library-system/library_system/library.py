"""
library.py
Defines the Library class, which manages collections of Books and Members,
handles borrowing/returning, searching, statistics, and JSON persistence.
"""

import json
import os
import shutil
from datetime import datetime

from book import Book
from member import Member

class Library:
    """Manages the full collection of books and members for the library."""

    def __init__(self, books_file='data/books.json', members_file='data/members.json',
                 backup_dir='data/backup'):
        self.books = {}       # isbn -> Book
        self.members = {}     # member_id -> Member
        self.books_file = books_file
        self.members_file = members_file
        self.backup_dir = backup_dir

    # ------------------------------------------------------------------
    # Book management
    # ------------------------------------------------------------------
    def add_book(self, title, author, isbn, year=None):
        """Add a new book to the library.

        Returns:
            (bool, str): Success flag and a status message.
        """
        if isbn in self.books:
            return False, f"A book with ISBN {isbn} already exists"

        self.books[isbn] = Book(title, author, isbn, year)
        return True, f"'{title}' added successfully"

    def remove_book(self, isbn):
        """Remove a book from the library by ISBN.

        Returns:
            (bool, str): Success flag and a status message.
        """
        if isbn not in self.books:
            return False, "Book not found"

        book = self.books[isbn]
        if not book.available:
            return False, "Cannot remove a book that is currently checked out"

        del self.books[isbn]
        return True, f"'{book.title}' removed successfully"

    def find_book(self, isbn):
        """Find a single book by exact ISBN. Returns Book or None."""
        return self.books.get(isbn)

    def search_books(self, query, field='title'):
        """Search books by title, author, or ISBN (case-insensitive, partial match).

        Args:
            query (str): Search term.
            field (str): One of 'title', 'author', 'isbn'.

        Returns:
            list[Book]: Matching books.
        """
        query = query.lower().strip()
        results = []
        for book in self.books.values():
            value = getattr(book, field, '')
            if value and query in str(value).lower():
                results.append(book)
        return results

    def available_books(self):
        """Return a list of all currently available books."""
        return [b for b in self.books.values() if b.available]

    def overdue_books(self):
        """Return a list of all currently overdue books."""
        return [b for b in self.books.values() if b.is_overdue()]

    # ------------------------------------------------------------------
    # Member management
    # ------------------------------------------------------------------
    def register_member(self, name, member_id, max_books=5):
        """Register a new member.

        Returns:
            (bool, str): Success flag and a status message.
        """
        if member_id in self.members:
            return False, f"A member with ID {member_id} already exists"

        self.members[member_id] = Member(name, member_id, max_books)
        return True, f"'{name}' registered successfully with ID {member_id}"

    def find_member(self, member_id):
        """Find a member by ID. Returns Member or None."""
        return self.members.get(member_id)

    # ------------------------------------------------------------------
    # Borrowing / returning (orchestrates Book + Member)
    # ------------------------------------------------------------------
    def borrow_book(self, isbn, member_id, loan_period=14):
        """Handle the full borrow workflow between a Book and a Member.

        Returns:
            (bool, str): Success flag and a status message.
        """
        book = self.find_book(isbn)
        if not book:
            return False, "Book not found"

        member = self.find_member(member_id)
        if not member:
            return False, "Member not found"

        if not member.can_borrow():
            return False, f"{member.name} has reached the maximum borrow limit ({member.max_books} books)"

        success, message = book.check_out(member_id, loan_period)
        if not success:
            return False, message

        member.borrow_book(isbn)
        return True, message

    def return_book(self, isbn, member_id=None):
        """Handle the full return workflow between a Book and a Member.

        Args:
            isbn (str): ISBN of the book being returned.
            member_id (str, optional): If provided, validated against the book's
                borrower record before returning.

        Returns:
            (bool, str): Success flag and a status message.
        """
        book = self.find_book(isbn)
        if not book:
            return False, "Book not found"

        if book.available:
            return False, "Book is already marked as available"

        borrower_id = book.borrowed_by
        member = self.find_member(borrower_id) if borrower_id else None

        if member_id and borrower_id and member_id != borrower_id:
            return False, "This book was not borrowed by that member"

        success, message = book.return_book()
        if not success:
            return False, message

        if member:
            member.return_book(isbn)

        return True, message

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------
    def get_statistics(self):
        """Return a dictionary of overall library statistics."""
        total_books = len(self.books)
        available = len(self.available_books())
        borrowed = total_books - available
        overdue = len(self.overdue_books())
        return {
            'total_books': total_books,
            'available_books': available,
            'total_members': len(self.members),
            'books_borrowed': borrowed,
            'overdue_books': overdue
        }

    # ------------------------------------------------------------------
    # File persistence
    # ------------------------------------------------------------------
    def save_books(self):
        """Save all books to the JSON file."""
        os.makedirs(os.path.dirname(self.books_file), exist_ok=True)
        try:
            data = [book.to_dict() for book in self.books.values()]
            with open(self.books_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True, f"Saved {len(data)} books"
        except (IOError, OSError) as e:
            return False, f"Error saving books: {e}"

    def load_books(self):
        """Load books from the JSON file. Silently starts empty if file is missing."""
        if not os.path.exists(self.books_file):
            return True, "No existing books file found; starting fresh"
        try:
            with open(self.books_file, 'r') as f:
                data = json.load(f)
            self.books = {item['isbn']: Book.from_dict(item) for item in data}
            return True, f"Loaded {len(self.books)} books from file"
        except (IOError, OSError, json.JSONDecodeError) as e:
            return False, f"Error loading books: {e}"

    def save_members(self):
        """Save all members to the JSON file."""
        os.makedirs(os.path.dirname(self.members_file), exist_ok=True)
        try:
            data = [member.to_dict() for member in self.members.values()]
            with open(self.members_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True, f"Saved {len(data)} members"
        except (IOError, OSError) as e:
            return False, f"Error saving members: {e}"

    def load_members(self):
        """Load members from the JSON file. Silently starts empty if file is missing."""
        if not os.path.exists(self.members_file):
            return True, "No existing members file found; starting fresh"
        try:
            with open(self.members_file, 'r') as f:
                data = json.load(f)
            self.members = {item['member_id']: Member.from_dict(item) for item in data}
            return True, f"Loaded {len(self.members)} members from file"
        except (IOError, OSError, json.JSONDecodeError) as e:
            return False, f"Error loading members: {e}"

    def save_all(self):
        """Save both books and members."""
        b_ok, b_msg = self.save_books()
        m_ok, m_msg = self.save_members()
        return (b_ok and m_ok), f"{b_msg}; {m_msg}"

    def load_all(self):
        """Load both books and members."""
        b_ok, b_msg = self.load_books()
        m_ok, m_msg = self.load_members()
        return (b_ok and m_ok), f"{b_msg}; {m_msg}"

    def backup_data(self):
        """Create timestamped backup copies of the books and members files."""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backed_up = []

            if os.path.exists(self.books_file):
                dest = os.path.join(self.backup_dir, f'books_{timestamp}.json')
                shutil.copy2(self.books_file, dest)
                backed_up.append(dest)

            if os.path.exists(self.members_file):
                dest = os.path.join(self.backup_dir, f'members_{timestamp}.json')
                shutil.copy2(self.members_file, dest)
                backed_up.append(dest)

            if not backed_up:
                return False, "Nothing to back up yet"
            return True, f"Backup created: {', '.join(backed_up)}"
        except (IOError, OSError) as e:
            return False, f"Error creating backup: {e}"
