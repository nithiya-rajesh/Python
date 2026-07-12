
"""
test_library.py
Unit tests for the Library class, including borrowing, searching,
statistics, and JSON persistence.
"""

import sys
import os
import shutil
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_system.library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.library = Library(
            books_file=os.path.join(self.temp_dir, 'books.json'),
            members_file=os.path.join(self.temp_dir, 'members.json'),
            backup_dir=os.path.join(self.temp_dir, 'backup')
        )
        self.library.add_book("Fluent Python", "Luciano Ramalho", "9781491946008", 2022)
        self.library.add_book("Python Crash Course", "Eric Matthes", "9781593279288", 2019)
        self.library.register_member("Jane Smith", "MEM002", max_books=2)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # -- Book management --------------------------------------------
    def test_add_book(self):
        success, message = self.library.add_book("New Book", "Author", "111")
        self.assertTrue(success)
        self.assertIn("111", self.library.books)

    def test_add_duplicate_book(self):
        success, message = self.library.add_book(
            "Dup", "Author", "9781491946008"
        )
        self.assertFalse(success)

    def test_remove_book(self):
        success, message = self.library.remove_book("9781491946008")
        self.assertTrue(success)
        self.assertNotIn("9781491946008", self.library.books)

    def test_remove_book_while_borrowed(self):
        self.library.borrow_book("9781491946008", "MEM002")
        success, message = self.library.remove_book("9781491946008")
        self.assertFalse(success)

    # -- Search --------------------------------------------------------
    def test_search_by_title(self):
        results = self.library.search_books("python", field='title')
        self.assertEqual(len(results), 2)

    def test_search_by_author(self):
        results = self.library.search_books("Ramalho", field='author')
        self.assertEqual(len(results), 1)

    def test_search_by_isbn(self):
        results = self.library.search_books("9781491946008", field='isbn')
        self.assertEqual(len(results), 1)

    # -- Borrow / return workflow --------------------------------------
    def test_borrow_book_success(self):
        success, message = self.library.borrow_book("9781491946008", "MEM002")
        self.assertTrue(success)
        self.assertFalse(self.library.books["9781491946008"].available)
        self.assertIn("9781491946008", self.library.members["MEM002"].borrowed_books)

    def test_borrow_book_member_limit(self):
        self.library.borrow_book("9781491946008", "MEM002")
        self.library.borrow_book("9781593279288", "MEM002")
        self.library.add_book("Third Book", "Author", "333")
        success, message = self.library.borrow_book("333", "MEM002")
        self.assertFalse(success)

    def test_borrow_nonexistent_book(self):
        success, message = self.library.borrow_book("000", "MEM002")
        self.assertFalse(success)
        self.assertIn("not found", message)

    def test_return_book_success(self):
        self.library.borrow_book("9781491946008", "MEM002")
        success, message = self.library.return_book("9781491946008")
        self.assertTrue(success)
        self.assertTrue(self.library.books["9781491946008"].available)
        self.assertNotIn("9781491946008", self.library.members["MEM002"].borrowed_books)

    # -- Statistics ------------------------------------------------------
    def test_statistics(self):
        self.library.borrow_book("9781491946008", "MEM002")
        stats = self.library.get_statistics()
        self.assertEqual(stats['total_books'], 2)
        self.assertEqual(stats['available_books'], 1)
        self.assertEqual(stats['books_borrowed'], 1)
        self.assertEqual(stats['total_members'], 1)

    # -- Persistence -----------------------------------------------------
    def test_save_and_load_books(self):
        self.library.save_books()
        new_library = Library(books_file=self.library.books_file,
                               members_file=self.library.members_file)
        ok, message = new_library.load_books()
        self.assertTrue(ok)
        self.assertEqual(len(new_library.books), 2)

    def test_save_and_load_members(self):
        self.library.save_members()
        new_library = Library(books_file=self.library.books_file,
                               members_file=self.library.members_file)
        ok, message = new_library.load_members()
        self.assertTrue(ok)
        self.assertEqual(len(new_library.members), 1)

    def test_load_missing_file_starts_empty(self):
        empty_library = Library(
            books_file=os.path.join(self.temp_dir, 'nonexistent_books.json'),
            members_file=os.path.join(self.temp_dir, 'nonexistent_members.json')
        )
        ok, message = empty_library.load_all()
        self.assertTrue(ok)
        self.assertEqual(len(empty_library.books), 0)

    def test_backup_creates_files(self):
        self.library.save_all()
        success, message = self.library.backup_data()
        self.assertTrue(success)
        self.assertTrue(os.path.isdir(self.library.backup_dir))
        self.assertTrue(len(os.listdir(self.library.backup_dir)) > 0)


if __name__ == '__main__':
    unittest.main()
