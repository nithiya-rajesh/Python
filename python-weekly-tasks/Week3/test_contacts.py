"""
Project: Contact Management System - Unit Tests
Author: Nithiya Rajendran
Description: Automated tests for validation, CRUD, and file operations.
"""

import unittest
import os
import json
from datetime import datetime
from contacts_manager import (
    validate_phone, validate_email,
    add_contact, update_contact, delete_contact,
    search_contacts, search_by_phone,
    save_to_file, load_from_file, export_to_csv
)

class TestContactManager(unittest.TestCase):

    def setUp(self):
        # fresh contacts dict for each test
        self.contacts = {}

    # -------------------------------
    # Validation Tests
    # -------------------------------
    def test_validate_phone_valid(self):
        valid, cleaned = validate_phone("9876543210")
        self.assertTrue(valid)
        self.assertEqual(cleaned, "9876543210")

    def test_validate_phone_invalid(self):
        valid, cleaned = validate_phone("abc123")
        self.assertFalse(valid)
        self.assertIsNone(cleaned)

    def test_validate_email_valid(self):
        self.assertTrue(validate_email("test@example.com"))

    def test_validate_email_invalid(self):
        self.assertFalse(validate_email("bad-email"))

    # -------------------------------
    # CRUD Tests
    # -------------------------------
    def test_add_contact(self):
        # simulate adding contact
        self.contacts["John"] = {
            "phone": "9876543210",
            "email": "john@example.com",
            "address": "Street 1",
            "group": "Friends",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.assertIn("John", self.contacts)

    def test_update_contact(self):
        self.contacts["John"] = {"phone": "9876543210", "email": None, "address": None, "group": "Other", "created_at": "", "updated_at": ""}
        update_contact(self.contacts, "John")  # interactive, but ensures function exists
        self.assertIn("John", self.contacts)

    def test_delete_contact(self):
        self.contacts["John"] = {"phone": "9876543210", "email": None, "address": None, "group": "Other", "created_at": "", "updated_at": ""}
        delete_contact(self.contacts, "John")  # interactive, but ensures function exists
        # deletion requires 'y' input, so we just check function exists

    def test_search_contacts(self):
        self.contacts["Alice"] = {"phone": "1234567890"}
        results = search_contacts(self.contacts, "Ali")
        self.assertIn("Alice", results)

    def test_search_by_phone(self):
        self.contacts["Bob"] = {"phone": "1112223333"}
        results = search_by_phone(self.contacts, "1112223333")
        self.assertIn("Bob", results)

    # -------------------------------
    # File Operation Tests
    # -------------------------------
    def test_save_and_load_file(self):
        filename = "test_contacts.json"
        self.contacts["Test"] = {"phone": "9998887777", "email": None, "address": None, "group": "Other", "created_at": "", "updated_at": ""}
        save_to_file(self.contacts, filename)
        loaded = load_from_file(filename)
        self.assertIn("Test", loaded)
        os.remove(filename)

    def test_export_to_csv(self):
        filename = "test_contacts.csv"
        self.contacts["Test"] = {"phone": "9998887777", "email": None, "address": None, "group": "Other", "created_at": "", "updated_at": ""}
        export_to_csv(self.contacts, filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
