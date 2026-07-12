"""
book.py
Defines the Book class used throughout the Library Management System.
"""

from datetime import datetime, timedelta


class Book:
    """Represents a single book in the library."""

    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True
        self.borrowed_by = None
        self.due_date = None
        self.date_added = datetime.now().strftime('%Y-%m-%d')

    # ------------------------------------------------------------------
    # Core behaviors
    # ------------------------------------------------------------------
    def check_out(self, member_id, loan_period=14):
        """Check the book out to a member.

        Args:
            member_id (str): ID of the member borrowing the book.
            loan_period (int): Number of days until the book is due.

        Returns:
            (bool, str): Success flag and a status message.
        """
        if not self.available:
            return False, "Book is already checked out"

        self.available = False
        self.borrowed_by = member_id
        self.due_date = (datetime.now() + timedelta(days=loan_period)).strftime('%Y-%m-%d')
        return True, f"Book checked out successfully. Due date: {self.due_date}"

    def return_book(self):
        """Return the book to the library.

        Returns:
            (bool, str): Success flag and a status message.
        """
        if self.available:
            return False, "Book is already available"

        was_overdue = self.is_overdue()
        self.available = True
        self.borrowed_by = None
        self.due_date = None

        if was_overdue:
            return True, "Book returned (was overdue)"
        return True, "Book returned successfully"

    def is_overdue(self):
        """Check whether the book is currently overdue."""
        if self.due_date and not self.available:
            due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
            return datetime.now() > due_date
        return False

    def days_overdue(self):
        """Calculate the number of days the book is overdue (0 if not overdue)."""
        if self.is_overdue():
            due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
            return (datetime.now() - due_date).days
        return 0

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def to_dict(self):
        """Convert the book to a dictionary for JSON serialization."""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'available': self.available,
            'borrowed_by': self.borrowed_by,
            'due_date': self.due_date,
            'date_added': self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Book instance from a dictionary (used when loading from JSON)."""
        book = cls(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            year=data.get('year')
        )
        book.available = data['available']
        book.borrowed_by = data.get('borrowed_by')
        book.due_date = data.get('due_date')
        book.date_added = data.get('date_added', datetime.now().strftime('%Y-%m-%d'))
        return book

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------
    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.borrowed_by}"
        if not self.available and self.is_overdue():
            status += f" (OVERDUE by {self.days_overdue()} days)"
        return f"{self.title} by {self.author} ({self.isbn}) - {status}"

    def __repr__(self):
        return f"Book(title={self.title!r}, author={self.author!r}, isbn={self.isbn!r})"
