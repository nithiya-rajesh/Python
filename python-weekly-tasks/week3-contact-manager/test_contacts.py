# Complete Test Suite for Contact Management System
import unittest
import json
import os
import re
from datetime import datetime
from contacts_manager import (
    validate_phone, validate_email, validate_name, create_contact,
    search_contacts, format_phone
)


class TestPhoneValidation(unittest.TestCase):
    """Test phone number validation"""
    
    def test_valid_phone_with_parentheses(self):
        """Test valid phone with parentheses format"""
        is_valid, cleaned = validate_phone("+1 (234) 567-8900")
        self.assertTrue(is_valid)
        self.assertEqual(cleaned, "12345678900")
    
    def test_valid_phone_with_dashes(self):
        """Test valid phone with dashes"""
        is_valid, cleaned = validate_phone("234-567-8900")
        self.assertTrue(is_valid)
        self.assertEqual(cleaned, "2345678900")
    
    def test_valid_phone_digits_only(self):
        """Test valid phone with digits only"""
        is_valid, cleaned = validate_phone("2345678900")
        self.assertTrue(is_valid)
        self.assertEqual(cleaned, "2345678900")
    
    def test_valid_international_phone(self):
        """Test valid international phone"""
        is_valid, cleaned = validate_phone("+91 9876543210")
        self.assertTrue(is_valid)
        self.assertEqual(cleaned, "919876543210")
    
    def test_invalid_phone_too_short(self):
        """Test invalid phone - too short"""
        is_valid, cleaned = validate_phone("123")
        self.assertFalse(is_valid)
        self.assertIsNone(cleaned)
    
    def test_invalid_phone_no_digits(self):
        """Test invalid phone - no digits"""
        is_valid, cleaned = validate_phone("abc def ghi")
        self.assertFalse(is_valid)
        self.assertIsNone(cleaned)
    
    def test_invalid_phone_too_long(self):
        """Test invalid phone - too many digits"""
        is_valid, cleaned = validate_phone("12345678901234567890")
        self.assertFalse(is_valid)
        self.assertIsNone(cleaned)


class TestEmailValidation(unittest.TestCase):
    """Test email validation"""
    
    def test_valid_email_standard(self):
        """Test valid standard email"""
        self.assertTrue(validate_email("john@example.com"))
    
    def test_valid_email_with_dots(self):
        """Test valid email with dots"""
        self.assertTrue(validate_email("john.doe@example.co.uk"))
    
    def test_valid_email_with_numbers(self):
        """Test valid email with numbers"""
        self.assertTrue(validate_email("user123@example.com"))
    
    def test_invalid_email_no_at(self):
        """Test invalid email - no @ symbol"""
        self.assertFalse(validate_email("invalid.email"))
    
    def test_invalid_email_no_domain(self):
        """Test invalid email - no domain"""
        self.assertFalse(validate_email("user@"))
    
    def test_invalid_email_no_username(self):
        """Test invalid email - no username"""
        self.assertFalse(validate_email("@example.com"))
    
    def test_invalid_email_no_tld(self):
        """Test invalid email - no TLD"""
        self.assertFalse(validate_email("user@example"))


class TestNameValidation(unittest.TestCase):
    """Test name validation"""
    
    def test_valid_name_full(self):
        """Test valid full name"""
        self.assertTrue(validate_name("John Doe"))
    
    def test_valid_name_single(self):
        """Test valid single name"""
        self.assertTrue(validate_name("Jane"))
    
    def test_invalid_name_empty(self):
        """Test invalid empty name"""
        self.assertFalse(validate_name(""))
    
    def test_invalid_name_spaces_only(self):
        """Test invalid name - spaces only"""
        self.assertFalse(validate_name("   "))
    
    def test_invalid_name_numbers_only(self):
        """Test invalid name - numbers only"""
        self.assertFalse(validate_name("12345"))


class TestContactCreation(unittest.TestCase):
    """Test contact creation"""
    
    def test_create_contact_full(self):
        """Test creating contact with all fields"""
        contact = create_contact(
            "John Doe",
            "1234567890",
            "john@example.com",
            "123 Main St",
            "Friends"
        )
        
        self.assertEqual(contact['phone'], "1234567890")
        self.assertEqual(contact['email'], "john@example.com")
        self.assertEqual(contact['address'], "123 Main St")
        self.assertEqual(contact['group'], "Friends")
        self.assertIn('created_at', contact)
        self.assertIn('updated_at', contact)
    
    def test_create_contact_minimal(self):
        """Test creating contact with minimal fields"""
        contact = create_contact("John Doe", "1234567890")
        
        self.assertEqual(contact['phone'], "1234567890")
        self.assertIsNone(contact['email'])
        self.assertIsNone(contact['address'])
        self.assertEqual(contact['group'], "Other")


if __name__ == '__main__':
    unittest.main()
