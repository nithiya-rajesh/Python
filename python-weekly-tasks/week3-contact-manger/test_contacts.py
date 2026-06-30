# Test Suite for Contact Management System
# Week 3 Project - Functions & Dictionaries

import unittest
import json
import os
from contacts_manager import (
    validate_phone,
    validate_email,
    validate_name,
    search_contacts,
    search_by_phone,
    load_from_file,
    save_to_file
)

class TestValidationFunctions(unittest.TestCase):
    """Test validation functions"""
    
    def test_validate_phone_valid(self):
        """Test valid phone numbers"""
        # US format
        is_valid, digits = validate_phone("+1 (234) 567-8900")
        self.assertTrue(is_valid)
        self.assertEqual(digits, "12345678900")
        
        # International format
        is_valid, digits = validate_phone("+44-20-1234-5678")
        self.assertTrue(is_valid)
        
        # Simple format
        is_valid, digits = validate_phone("1234567890")
        self.assertTrue(is_valid)
    
    def test_validate_phone_invalid(self):
        """Test invalid phone numbers"""
        # Too short
        is_valid, digits = validate_phone("123")
        self.assertFalse(is_valid)
        
        # Too long
        is_valid, digits = validate_phone("12345678901234567890")
        self.assertFalse(is_valid)
        
        # No digits
        is_valid, digits = validate_phone("abc def ghi")
        self.assertFalse(is_valid)
    
    def test_validate_email_valid(self):
        """Test valid email addresses"""
        self.assertTrue(validate_email("john@example.com"))
        self.assertTrue(validate_email("user.name+tag@domain.co.uk"))
        self.assertTrue(validate_email("test_123@test-domain.org"))
    
    def test_validate_email_invalid(self):
        """Test invalid email addresses"""
        self.assertFalse(validate_email("plainaddress"))
        self.assertFalse(validate_email("@example.com"))
        self.assertFalse(validate_email("user@"))
        self.assertFalse(validate_email("user name@example.com"))
    
    def test_validate_name_valid(self):
        """Test valid names"""
        self.assertTrue(validate_name("John Doe"))
        self.assertTrue(validate_name("Jane"))
        self.assertTrue(validate_name("  Bob Smith  "))  # Spaces are trimmed
    
    def test_validate_name_invalid(self):
        """Test invalid names"""
        self.assertFalse(validate_name(""))
        self.assertFalse(validate_name("   "))  # Only spaces

class TestSearchFunctions(unittest.TestCase):
    """Test search functions"""
    
    def setUp(self):
        """Set up test data"""
        self.contacts = {
            "John Doe": {
                "phone": "12345678900",
                "email": "john@example.com",
                "address": "123 Main St",
                "group": "Friends",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            },
            "Jane Smith": {
                "phone": "19876543210",
                "email": "jane@example.com",
                "address": "456 Oak Ave",
                "group": "Work",
                "created_at": "2024-01-02T10:00:00",
                "updated_at": "2024-01-02T10:00:00"
            },
            "Johnny Appleseed": {
                "phone": "15551234567",
                "email": "johnny@apple.com",
                "address": "789 Orchard Rd",
                "group": "Family",
                "created_at": "2024-01-03T10:00:00",
                "updated_at": "2024-01-03T10:00:00"
            }
        }
    
    def test_search_exact_match(self):
        """Test exact name match"""
        results = search_contacts(self.contacts, "John Doe")
        self.assertEqual(len(results), 1)
        self.assertIn("John Doe", results)
    
    def test_search_partial_match(self):
        """Test partial name match"""
        results = search_contacts(self.contacts, "john")
        self.assertEqual(len(results), 2)
        self.assertIn("John Doe", results)
        self.assertIn("Johnny Appleseed", results)
    
    def test_search_case_insensitive(self):
        """Test case-insensitive search"""
        results = search_contacts(self.contacts, "JANE")
        self.assertEqual(len(results), 1)
        self.assertIn("Jane Smith", results)
    
    def test_search_no_match(self):
        """Test search with no results"""
        results = search_contacts(self.contacts, "NonExistent")
        self.assertEqual(len(results), 0)
    
    def test_search_by_phone_full(self):
        """Test search by full phone number"""
        results = search_by_phone(self.contacts, "12345678900")
        self.assertEqual(len(results), 1)
        self.assertIn("John Doe", results)
    
    def test_search_by_phone_partial(self):
        """Test search by partial phone number"""
        results = search_by_phone(self.contacts, "123456789")
        self.assertEqual(len(results), 1)
        self.assertIn("John Doe", results)
    
    def test_search_by_phone_format_variations(self):
        """Test search with different phone formats"""
        results = search_by_phone(self.contacts, "+1 (234) 567-8900")
        self.assertEqual(len(results), 1)
        self.assertIn("John Doe", results)

class TestFileOperations(unittest.TestCase):
    """Test file save/load operations"""
    
    def setUp(self):
        """Set up test data"""
        self.test_file = 'test_contacts.json'
        self.test_contacts = {
            "Test User": {
                "phone": "1234567890",
                "email": "test@example.com",
                "address": "123 Test St",
                "group": "Test",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_to_file(self):
        """Test saving contacts to file"""
        result = save_to_file(self.test_contacts, self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_load_from_file(self):
        """Test loading contacts from file"""
        # First save
        save_to_file(self.test_contacts, self.test_file)
        
        # Then load
        loaded = load_from_file(self.test_file)
        self.assertEqual(loaded, self.test_contacts)
    
    def test_load_nonexistent_file(self):
        """Test loading from non-existent file"""
        loaded = load_from_file('nonexistent.json')
        self.assertEqual(loaded, {})
    
    def test_save_and_load_roundtrip(self):
        """Test save and load roundtrip"""
        # Save
        save_to_file(self.test_contacts, self.test_file)
        
        # Load
        loaded = load_from_file(self.test_file)
        
        # Verify
        self.assertEqual(loaded, self.test_contacts)
        self.assertEqual(loaded["Test User"]["phone"], "1234567890")

class TestDataStructure(unittest.TestCase):
    """Test the contact data structure"""
    
    def test_contact_has_all_fields(self):
        """Test that contacts have all required fields"""
        contact = {
            "phone": "1234567890",
            "email": "test@example.com",
            "address": "123 Test St",
            "group": "Test",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        }
        
        required_fields = ['phone', 'email', 'address', 'group', 'created_at', 'updated_at']
        for field in required_fields:
            self.assertIn(field, contact)
    
    def test_contact_can_have_optional_fields(self):
        """Test that email and address can be None"""
        contact = {
            "phone": "1234567890",
            "email": None,
            "address": None,
            "group": "Test",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        }
        
        self.assertIsNone(contact['email'])
        self.assertIsNone(contact['address'])

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test data"""
        self.contacts = {
            "John": {
                "phone": "12345678900",
                "email": None,
                "address": None,
                "group": "Friends",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }
    
    def test_duplicate_contact_name(self):
        """Test handling of duplicate contact names"""
        # Duplicate name already exists in contacts
        self.assertIn("John", self.contacts)
    
    def test_empty_contacts_dict(self):
        """Test with empty contacts dictionary"""
        empty_contacts = {}
        results = search_contacts(empty_contacts, "test")
        self.assertEqual(results, {})
    
    def test_phone_with_special_characters(self):
        """Test phone numbers with special characters"""
        is_valid, cleaned = validate_phone("+1-234-567-8900")
        self.assertTrue(is_valid)
        self.assertEqual(cleaned, "12345678900")
    
    def test_email_case_sensitivity(self):
        """Test email validation with different cases"""
        self.assertTrue(validate_email("Test@Example.Com"))
        self.assertTrue(validate_email("test@example.com"))

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestValidationFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestDataStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
