"""
member.py
Defines the Member class used throughout the Library Management System.
"""

from datetime import datetime


class Member:
    """Represents a library member."""

    def __init__(self, name, member_id, max_books=5):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # list of ISBNs currently borrowed
        self.max_books = max_books
        self.date_joined = datetime.now().strftime('%Y-%m-%d')

    # ------------------------------------------------------------------
    # Core behaviors
    # ------------------------------------------------------------------
    def borrow_book(self, isbn):
        """Record that this member has borrowed a book.

        Args:
            isbn (str): ISBN of the book being borrowed.

        Returns:
            (bool, str): Success flag and a status message.
        """
        if isbn in self.borrowed_books:
            return False, f"{self.name} has already borrowed this book"

        if len(self.borrowed_books) >= self.max_books:
            return False, f"{self.name} has reached the maximum borrow limit ({self.max_books} books)"

        self.borrowed_books.append(isbn)
        return True, f"{self.name} successfully borrowed the book"

    def return_book(self, isbn):
        """Record that this member has returned a book.

        Args:
            isbn (str): ISBN of the book being returned.

        Returns:
            (bool, str): Success flag and a status message.
        """
        if isbn not in self.borrowed_books:
            return False, f"{self.name} does not have this book borrowed"

        self.borrowed_books.remove(isbn)
        return True, f"{self.name} successfully returned the book"

    def can_borrow(self):
        """Check if the member is under their borrow limit."""
        return len(self.borrowed_books) < self.max_books

    def books_borrowed_count(self):
        """Return the number of books currently borrowed."""
        return len(self.borrowed_books)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def to_dict(self):
        """Convert the member to a dictionary for JSON serialization."""
        return {
            'name': self.name,
            'member_id': self.member_id,
            'borrowed_books': self.borrowed_books,
            'max_books': self.max_books,
            'date_joined': self.date_joined
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Member instance from a dictionary (used when loading from JSON)."""
        member = cls(
            name=data['name'],
            member_id=data['member_id'],
            max_books=data.get('max_books', 5)
        )
        member.borrowed_books = data.get('borrowed_books', [])
        member.date_joined = data.get('date_joined', datetime.now().strftime('%Y-%m-%d'))
        return member

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------
    def __str__(self):
        return (f"{self.name} (ID: {self.member_id}) - "
                f"{self.books_borrowed_count()}/{self.max_books} books borrowed")

    def __repr__(self):
        return f"Member(name={self.name!r}, member_id={self.member_id!r})"
