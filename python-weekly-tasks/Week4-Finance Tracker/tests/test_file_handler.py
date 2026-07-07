"""
Unit Tests for FileHandler Class - Week 4 Finance Tracker
========================================================

Tests validate FileHandler works correctly for all file operations.
Each test is documented to explain what it's testing.
"""

import unittest
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '../')
from finance_tracker.file_handler import FileHandler
from finance_tracker.expense import Expense


class TestFileHandlerSetup(unittest.TestCase):
    """Test FileHandler initialization and setup"""
    
    def setUp(self):
        """Create test handler with temp directory"""
        self.test_dir = 'test_data'
        self.handler = FileHandler(self.test_dir)
    
    def tearDown(self):
        """Clean up test files"""
        if Path(self.test_dir).exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_creates_data_directory(self):
        """Test that data directory is created"""
        self.assertTrue(Path(self.test_dir).exists())
    
    def test_creates_backup_directory(self):
        """Test that backup directory is created"""
        self.assertTrue((Path(self.test_dir) / 'backup').exists())
    
    def test_creates_export_directory(self):
        """Test that export directory is created"""
        self.assertTrue((Path(self.test_dir) / 'exports').exists())


class TestFileHandlerSaveLoad(unittest.TestCase):
    """Test save and load operations"""
    
    def setUp(self):
        """Create test handler and data"""
        self.test_dir = 'test_data'
        self.handler = FileHandler(self.test_dir)
        self.test_expenses = [
            Expense('2024-01-15', 500, 'Food', 'Lunch'),
            Expense('2024-01-16', 150, 'Transport', 'Bus'),
        ]
        self.test_budgets = {'Food': 5000, 'Transport': 2000}
    
    def tearDown(self):
        """Clean up test files"""
        if Path(self.test_dir).exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_save_expenses(self):
        """Test saving expenses to file"""
        result = self.handler.save_expenses(self.test_expenses, self.test_budgets)
        self.assertTrue(result)
        self.assertTrue(self.handler.data_file.exists())
    
    def test_load_expenses_empty(self):
        """Test loading when no file exists"""
        expenses, budgets = self.handler.load_expenses()
        self.assertEqual(expenses, [])
        self.assertEqual(budgets, {})
    
    def test_save_and_load_roundtrip(self):
        """Test saving and loading data"""
        # Save
        self.handler.save_expenses(self.test_expenses, self.test_budgets)
        
        # Load
        loaded_expenses, loaded_budgets = self.handler.load_expenses()
        
        # Verify
        self.assertEqual(len(loaded_expenses), 2)
        self.assertEqual(loaded_expenses[0]['category'], 'Food')
        self.assertEqual(loaded_budgets['Food'], 5000)
    
    def test_load_preserves_data_format(self):
        """Test that loaded data has correct format"""
        self.handler.save_expenses(self.test_expenses, self.test_budgets)
        expenses, budgets = self.handler.load_expenses()
        
        # Check expense format
        for exp in expenses:
            self.assertIn('date', exp)
            self.assertIn('amount', exp)
            self.assertIn('category', exp)
            self.assertIn('description', exp)


class TestFileHandlerBackup(unittest.TestCase):
    """Test backup functionality"""
    
    def setUp(self):
        """Create test handler and data"""
        self.test_dir = 'test_data'
        self.handler = FileHandler(self.test_dir)
        self.test_expenses = [Expense('2024-01-15', 500, 'Food', 'Lunch')]
        self.handler.save_expenses(self.test_expenses, {})
    
    def tearDown(self):
        """Clean up test files"""
        if Path(self.test_dir).exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_create_backup(self):
        """Test that backup is created"""
        result = self.handler.create_backup()
        self.assertTrue(result)
    
    def test_backup_has_timestamp(self):
        """Test that backup filename contains timestamp"""
        self.handler.create_backup()
        backups = list(self.handler.backup_dir.glob('*.json'))
        self.assertTrue(len(backups) > 0)
        # Backup name should contain timestamp pattern
        backup_name = backups[0].name
        self.assertIn('expenses_', backup_name)
    
    def test_backup_contains_data(self):
        """Test that backup contains the data"""
        self.handler.create_backup()
        backups = list(self.handler.backup_dir.glob('*.json'))
        self.assertTrue(len(backups) > 0)
        
        # Read backup file
        with open(backups[0], 'r') as f:
            backup_data = json.load(f)
        
        self.assertIn('expenses', backup_data)


class TestFileHandlerCSV(unittest.TestCase):
    """Test CSV export functionality"""
    
    def setUp(self):
        """Create test handler and data"""
        self.test_dir = 'test_data'
        self.handler = FileHandler(self.test_dir)
        self.test_expenses = [
            Expense('2024-01-15', 500, 'Food', 'Lunch'),
            Expense('2024-01-16', 150, 'Transport', 'Bus'),
        ]
    
    def tearDown(self):
        """Clean up test files"""
        if Path(self.test_dir).exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_export_to_csv(self):
        """Test exporting to CSV"""
        result = self.handler.export_to_csv(self.test_expenses)
        self.assertTrue(result)
    
    def test_csv_file_created(self):
        """Test that CSV file is created"""
        self.handler.export_to_csv(self.test_expenses)
        csv_files = list(self.handler.export_dir.glob('*.csv'))
        self.assertTrue(len(csv_files) > 0)
    
    def test_csv_contains_data(self):
        """Test that CSV contains the expense data"""
        self.handler.export_to_csv(self.test_expenses)
        csv_files = list(self.handler.export_dir.glob('*.csv'))
        
        with open(csv_files[0], 'r') as f:
            content = f.read()
        
        # Should contain header and data
        self.assertIn('date', content)
        self.assertIn('amount', content)
        self.assertIn('2024-01-15', content)


class TestFileHandlerErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def setUp(self):
        """Create test handler"""
        self.test_dir = 'test_data'
        self.handler = FileHandler(self.test_dir)
    
    def tearDown(self):
        """Clean up test files"""
        if Path(self.test_dir).exists():
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_load_empty_file(self):
        """Test loading empty file returns empty data"""
        expenses, budgets = self.handler.load_expenses()
        self.assertEqual(expenses, [])
        self.assertEqual(budgets, {})
    
    def test_export_empty_list(self):
        """Test exporting empty expense list"""
        result = self.handler.export_to_csv([])
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
