
import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_system.book import Book


class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book("Fluent Python", "Luciano Ramalho", "9781491946008", 2022)

    def test_initial_state(self):
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrowed_by)
        self.assertIsNone(self.book.due_date)

    def test_check_out_success(self):
        success, message = self.book.check_out("MEM001")
        self.assertTrue(success)
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrowed_by, "MEM001")
        self.assertIsNotNone(self.book.due_date)

    def test_check_out_already_borrowed(self):
        self.book.check_out("MEM001")
        success, message = self.book.check_out("MEM002")
        self.assertFalse(success)
        self.assertIn("already checked out", message)

    def test_return_book_success(self):
        self.book.check_out("MEM001")
        success, message = self.book.return_book()
        self.assertTrue(success)
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrowed_by)

    def test_return_book_when_not_borrowed(self):
        success, message = self.book.return_book()
        self.assertFalse(success)
        self.assertIn("already available", message)

    def test_is_overdue_false_when_recent(self):
        self.book.check_out("MEM001", loan_period=14)
        self.assertFalse(self.book.is_overdue())

    def test_is_overdue_true_when_past_due(self):
        self.book.check_out("MEM001", loan_period=1)
        self.book.due_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        self.assertTrue(self.book.is_overdue())
        self.assertEqual(self.book.days_overdue(), 5)

    def test_to_dict_and_from_dict_roundtrip(self):
        self.book.check_out("MEM001")
        data = self.book.to_dict()
        restored = Book.from_dict(data)
        self.assertEqual(restored.title, self.book.title)
        self.assertEqual(restored.isbn, self.book.isbn)
        self.assertEqual(restored.available, self.book.available)
        self.assertEqual(restored.borrowed_by, self.book.borrowed_by)

    def test_str_representation(self):
        self.assertIn("Available", str(self.book))
        self.book.check_out("MEM001")
        self.assertIn("Borrowed by MEM001", str(self.book))


if __name__ == '__main__':
    unittest.main()
