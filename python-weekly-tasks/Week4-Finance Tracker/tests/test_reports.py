"""
Unit Tests for ReportGenerator Class - Week 4 Finance Tracker
===========================================================

Tests validate ReportGenerator works correctly for all reports.
"""

import unittest
import sys
from datetime import datetime

sys.path.insert(0, '../')
from finance_tracker.expense_manager import ExpenseManager
from finance_tracker.reports import ReportGenerator
from finance_tracker.expense import Expense


class TestReportGeneratorSetup(unittest.TestCase):
    """Test ReportGenerator initialization"""
    
    def setUp(self):
        """Create manager and generator"""
        self.manager = ExpenseManager()
        self.generator = ReportGenerator(self.manager)
    
    def test_initialization(self):
        """Test that generator initializes"""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.manager, self.manager)


class TestMonthlySummary(unittest.TestCase):
    """Test monthly summary report"""
    
    def setUp(self):
        """Create data for testing"""
        self.manager = ExpenseManager()
        self.generator = ReportGenerator(self.manager)
        
        # Add expenses
        self.manager.add_expense('2024-01-15', 500, 'Food', 'Lunch')
        self.manager.add_expense('2024-01-16', 150, 'Transport', 'Bus')
        self.manager.add_expense('2024-01-17', 300, 'Food', 'Dinner')
    
    def test_monthly_summary_structure(self):
        """Test that monthly summary has correct structure"""
        report = self.generator.monthly_summary(2024, 1)
        
        self.assertIn('month', report)
        self.assertIn('total_spent', report)
        self.assertIn('by_category', report)
    
    def test_monthly_summary_calculation(self):
        """Test that totals are calculated correctly"""
        report = self.generator.monthly_summary(2024, 1)
        
        self.assertEqual(report['total_spent'], 950)  # 500+150+300
        self.assertEqual(report['expense_count'], 3)
    
    def test_monthly_summary_by_category(self):
        """Test category breakdown"""
        report = self.generator.monthly_summary(2024, 1)
        
        self.assertIn('Food', report['by_category'])
        self.assertEqual(report['by_category']['Food']['total'], 800)
        self.assertEqual(report['by_category']['Food']['count'], 2)


class TestCategoryBreakdown(unittest.TestCase):
    """Test category breakdown report"""
    
    def setUp(self):
        """Create data for testing"""
        self.manager = ExpenseManager()
        self.generator = ReportGenerator(self.manager)
        
        # Add expenses in different categories
        self.manager.add_expense('2024-01-15', 500, 'Food', 'Lunch')
        self.manager.add_expense('2024-01-16', 200, 'Transport', 'Bus')
        self.manager.add_expense('2024-01-17', 100, 'Entertainment', 'Movie')
    
    def test_breakdown_structure(self):
        """Test breakdown has correct structure"""
        breakdown = self.generator.category_breakdown()
        
        self.assertIn('total', breakdown)
        self.assertIn('categories', breakdown)
        self.assertIn('num_categories', breakdown)
    
    def test_breakdown_categories(self):
        """Test that all categories appear"""
        breakdown = self.generator.category_breakdown()
        
        categories = [c['category'] for c in breakdown['categories']]
        self.assertIn('Food', categories)
        self.assertIn('Transport', categories)
        self.assertIn('Entertainment', categories)
    
    def test_breakdown_percentages(self):
        """Test that percentages are calculated"""
        breakdown = self.generator.category_breakdown()
        
        # Food is 500/800 = 62.5%
        food = [c for c in breakdown['categories'] if c['category'] == 'Food'][0]
        self.assertAlmostEqual(food['percentage'], 62.5, places=1)


class TestBudgetComparison(unittest.TestCase):
    """Test budget comparison report"""
    
    def setUp(self):
        """Create data for testing"""
        self.manager = ExpenseManager()
        self.generator = ReportGenerator(self.manager)
        
        # Set budgets
        self.manager.set_budget('Food', 1000)
        self.manager.set_budget('Transport', 300)
        
        # Add expenses
        self.manager.add_expense('2024-01-15', 600, 'Food', 'Lunch')
        self.manager.add_expense('2024-01-16', 250, 'Transport', 'Bus')
    
    def test_comparison_structure(self):
        """Test comparison has correct structure"""
        comparison = self.generator.budget_comparison()
        
        self.assertIn('total_budget', comparison)
        self.assertIn('total_spent', comparison)
        self.assertIn('total_remaining', comparison)
        self.assertIn('categories', comparison)
    
    def test_comparison_totals(self):
        """Test budget comparison totals"""
        comparison = self.generator.budget_comparison()
        
        self.assertEqual(comparison['total_budget'], 1300)  # 1000+300
        self.assertEqual(comparison['total_spent'], 850)    # 600+250
        self.assertEqual(comparison['total_remaining'], 450)  # 1300-850
    
    def test_under_budget_status(self):
        """Test that under-budget is detected"""
        comparison = self.generator.budget_comparison()
        
        self.assertFalse(comparison['is_over_budget'])


class TestTextChart(unittest.TestCase):
    """Test text chart generation"""
    
    def setUp(self):
        """Create generator"""
        self.manager = ExpenseManager()
        self.generator = ReportGenerator(self.manager)
    
    def test_chart_generation(self):
        """Test that chart is generated"""
        data = {'Food': 500, 'Transport': 200}
        chart = self.generator.text_chart('Test Chart', data)
        
        self.assertIsNotNone(chart)
        self.assertIsInstance(chart, str)
        self.assertIn('Test Chart', chart)
    
    def test_chart_contains_data(self):
        """Test that chart contains data labels"""
        data = {'Food': 500, 'Transport': 200}
        chart = self.generator.text_chart('Test Chart', data)
        
        self.assertIn('Food', chart)
        self.assertIn('Transport', chart)
    
    def test_empty_data_handling(self):
        """Test handling of empty data"""
        chart = self.generator.text_chart('Empty Chart', {})
        
        self.assertIn('No data', chart)


class TestSpendingTrend(unittest.TestCase):
    """Test spending trend analysis"""
    
    def setUp(self):
        """Create data for testing"""
        self.manager = ExpenseManager()
        self.generator = ReportGenerator(self.manager)
        
        # Add expenses in different months
        self.manager.add_expense('2024-01-15', 500, 'Food', 'January')
        self.manager.add_expense('2024-02-15', 600, 'Food', 'February')
        self.manager.add_expense('2024-03-15', 700, 'Food', 'March')
    
    def test_trend_structure(self):
        """Test trend has correct structure"""
        trend = self.generator.spending_trend('2024-01-01', '2024-03-31')
        
        self.assertIn('monthly_totals', trend)
        self.assertIn('total_period', trend)
        self.assertIn('average_monthly', trend)
    
    def test_trend_calculation(self):
        """Test trend calculations"""
        trend = self.generator.spending_trend('2024-01-01', '2024-03-31')
        
        self.assertEqual(trend['total_period'], 1800)  # 500+600+700
        self.assertAlmostEqual(trend['average_monthly'], 600, places=0)


if __name__ == '__main__':
    unittest.main()
