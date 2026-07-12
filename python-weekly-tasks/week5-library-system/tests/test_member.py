"""
test_member.py
Unit tests for the Member class.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_system.member import Member


class TestMember(unittest.TestCase):

    def setUp(self):
        self.member = Member("Jane Smith", "MEM002", max_books=2)

    def test_initial_state(self):
        self.assertEqual(self.member.borrowed_books, [])
        self.assertEqual(self.member.max_books, 2)

    def test_borrow_book_success(self):
        success, message = self.member.borrow_book("ISBN001")
        self.assertTrue(success)
        self.assertIn("ISBN001", self.member.borrowed_books)

    def test_borrow_book_duplicate(self):
        self.member.borrow_book("ISBN001")
        success, message = self.member.borrow_book("ISBN001")
        self.assertFalse(success)
        self.assertIn("already borrowed", message)

    def test_borrow_book_exceeds_limit(self):
        self.member.borrow_book("ISBN001")
        self.member.borrow_book("ISBN002")
        success, message = self.member.borrow_book("ISBN003")
        self.assertFalse(success)
        self.assertIn("maximum borrow limit", message)

    def test_return_book_success(self):
        self.member.borrow_book("ISBN001")
        success, message = self.member.return_book("ISBN001")
        self.assertTrue(success)
        self.assertNotIn("ISBN001", self.member.borrowed_books)

    def test_return_book_not_borrowed(self):
        success, message = self.member.return_book("ISBN999")
        self.assertFalse(success)
        self.assertIn("does not have this book", message)

    def test_can_borrow(self):
        self.assertTrue(self.member.can_borrow())
        self.member.borrow_book("ISBN001")
        self.member.borrow_book("ISBN002")
        self.assertFalse(self.member.can_borrow())

    def test_to_dict_and_from_dict_roundtrip(self):
        self.member.borrow_book("ISBN001")
        data = self.member.to_dict()
        restored = Member.from_dict(data)
        self.assertEqual(restored.name, self.member.name)
        self.assertEqual(restored.member_id, self.member.member_id)
        self.assertEqual(restored.borrowed_books, self.member.borrowed_books)


if __name__ == '__main__':
    unittest.main()
