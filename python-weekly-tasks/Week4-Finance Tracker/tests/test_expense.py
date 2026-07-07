"""
Unit Tests for Expense Class - Week 4 Finance Tracker
=====================================================

Tests validate the Expense class works correctly.
Each test is documented to explain what it's testing.
"""

import unittest
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '../')
from finance_tracker.expense import Expense


class TestExpenseValidation(unittest.TestCase):
    """Test Expense validation methods"""
    
    def test_valid_date_format(self):
        """Line 1: Test that valid date is accepted"""
        # Line 2: Should not raise exception
        result = Expense.validate_date('2024-01-15')
        self.assertEqual(result, '2024-01-15')
    
    def test_invalid_date_format(self):
        """Line 3: Test that invalid date raises error"""
        # Line 4: Should raise ValueError
        with self.assertRaises(ValueError):
            Expense.validate_date('15-01-2024')
    
    def test_valid_amount(self):
        """Line 5: Test that positive amount is valid"""
        # Line 6: Should return float
        result = Expense.validate_amount(500)
        self.assertEqual(result, 500.0)
    
    def test_negative_amount(self):
        """Line 7: Test that negative amount raises error"""
        # Line 8: Should raise ValueError
        with self.assertRaises(ValueError):
            Expense.validate_amount(-500)
    
    def test_zero_amount(self):
        """Line 9: Test that zero amount raises error"""
        # Line 10: Should raise ValueError
        with self.assertRaises(ValueError):
            Expense.validate_amount(0)
    
    def test_valid_category(self):
        """Line 11: Test that valid category is accepted"""
        # Line 12: Should return category name
        result = Expense.validate_category('Food')
        self.assertEqual(result, 'Food')
    
    def test_invalid_category(self):
        """Line 13: Test that invalid category raises error"""
        # Line 14: Should raise ValueError
        with self.assertRaises(ValueError):
            Expense.validate_category('InvalidCategory')


class TestExpenseCreation(unittest.TestCase):
    """Test Expense object creation"""
    
    def test_create_valid_expense(self):
        """Line 15: Test creating valid expense"""
        # Line 16: Create expense
        expense = Expense('2024-01-15', 500, 'Food', 'Lunch')
        
        # Line 17: Verify attributes
        self.assertEqual(expense.date, '2024-01-15')
        self.assertEqual(expense.amount, 500.0)
        self.assertEqual(expense.category, 'Food')
        self.assertEqual(expense.description, 'Lunch')
    
    def test_expense_has_timestamp(self):
        """Line 18: Test that timestamp is created"""
        # Line 19: Create expense
        expense = Expense('2024-01-15', 500, 'Food', 'Lunch')
        
        # Line 20: Verify created_at exists
        self.assertIsNotNone(expense.created_at)
        self.assertIsInstance(expense.created_at, str)
    
    def test_expense_default_category(self):
        """Line 21: Test default category handling"""
        # Line 22: Create with empty category
        expense = Expense('2024-01-15', 500, '', 'Lunch')
        
        # Line 23: Should use default 'Other'
        self.assertEqual(expense.category, 'Other')


class TestExpenseDictConversion(unittest.TestCase):
    """Test expense to/from dictionary conversion"""
    
    def test_to_dict(self):
        """Line 24: Test converting expense to dictionary"""
        # Line 25: Create expense
        expense = Expense('2024-01-15', 500, 'Food', 'Lunch')
        
        # Line 26: Convert to dict
        expense_dict = expense.to_dict()
        
        # Line 27: Verify all keys present
        self.assertIn('date', expense_dict)
        self.assertIn('amount', expense_dict)
        self.assertIn('category', expense_dict)
        self.assertIn('description', expense_dict)
        self.assertIn('created_at', expense_dict)
    
    def test_from_dict(self):
        """Line 28: Test creating expense from dictionary"""
        # Line 29: Create dictionary
        data = {
            'date': '2024-01-15',
            'amount': 500,
            'category': 'Food',
            'description': 'Lunch'
        }
        
        # Line 30: Create expense from dict
        expense = Expense.from_dict(data)
        
        # Line 31: Verify attributes
        self.assertEqual(expense.date, '2024-01-15')
        self.assertEqual(expense.amount, 500.0)
    
    def test_roundtrip_conversion(self):
        """Line 32: Test converting to dict and back"""
        # Line 33: Create original
        original = Expense('2024-01-15', 500, 'Food', 'Lunch')
        
        # Line 34: Convert to dict then back
        as_dict = original.to_dict()
        reconstructed = Expense.from_dict(as_dict)
        
        # Line 35: Verify same data
        self.assertEqual(original.date, reconstructed.date)
        self.assertEqual(original.amount, reconstructed.amount)
        self.assertEqual(original.category, reconstructed.category)


class TestExpenseStringRepresentation(unittest.TestCase):
    """Test expense string display"""
    
    def test_str_format(self):
        """Line 36: Test __str__ method"""
        # Line 37: Create expense
        expense = Expense('2024-01-15', 500.5, 'Food', 'Lunch')
        
        # Line 38: Convert to string
        str_repr = str(expense)
        
        # Line 39: Verify contains key info
        self.assertIn('2024-01-15', str_repr)
        self.assertIn('500', str_repr)
        self.assertIn('Food', str_repr)
        self.assertIn('Lunch', str_repr)
    
    def test_repr_format(self):
        """Line 40: Test __repr__ method"""
        # Line 41: Create expense
        expense = Expense('2024-01-15', 500, 'Food', 'Lunch')
        
        # Line 42: Get repr
        repr_str = repr(expense)
        
        # Line 43: Should contain class name
        self.assertIn('Expense', repr_str)


if __name__ == '__main__':
    unittest.main()
