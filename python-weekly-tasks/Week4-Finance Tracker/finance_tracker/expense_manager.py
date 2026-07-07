"""
EXPENSE MANAGER MODULE - Week 4 Finance Tracker
===============================================

This module defines the ExpenseManager class which manages a collection
of Expense objects. It handles adding, removing, searching, and filtering
expenses.

"""

from datetime import datetime 
from .expense import Expense



class ExpenseManager:
    
    def __init__(self):
    
        self.expenses = []
        self.budget = {}
    
    def add_expense(self, date, amount, category, description):
    
        try:
            expense = Expense(date, amount, category, description)
            self.expenses.append(expense)
            return True
        except ValueError as e:
            print(f"❌ Error adding expense: {e}")
            return False
    
    def remove_expense(self, index):
       
        try:
            if index < 0 or index >= len(self.expenses):
                raise IndexError(f"Invalid index: {index}")
            removed = self.expenses.pop(index)
            print(f"✅ Removed: {removed}")
            return True

        except IndexError as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_all_expenses(self):
        return self.expenses
    
    def search_by_category(self, category):
        return [expense for expense in self.expenses 
                if expense.category == category]
    
    def search_by_date_range(self, start_date, end_date):
        return [expense for expense in self.expenses
                if start_date <= expense.date <= end_date]
    
    def get_total_spent(self):
        return sum(expense.amount for expense in self.expenses)
    
    def get_category_total(self, category):
        category_expenses = self.search_by_category(category)
        return sum(expense.amount for expense in category_expenses) or 0
    
    def get_all_categories(self):
        
        categories = {expense.category for expense in self.expenses}
        return sorted(list(categories))
    
    def get_monthly_expenses(self, year, month):
        month_str = f"{year}-{month:02d}"  
 
        return [expense for expense in self.expenses
                if expense.date.startswith(month_str)]
    
    def set_budget(self, category, amount):
  
        try:
            validated_amount = Expense.validate_amount(amount)
            self.budget[category] = validated_amount
            return True
        except ValueError as e:
            print(f"❌ Error setting budget: {e}")
            return False
    
    def get_budget_status(self, category):
    
        if category not in self.budget:
        
            return {
                'category': category,
                'budget': 0,
                'spent': 0,
                'remaining': 0,
                'status': 'No budget set'
            }
        budget_limit = self.budget[category]
        
        spent = self.get_category_total(category)

        remaining = budget_limit - spent
 
        if spent > budget_limit:
            status = f"⚠️ OVER BUDGET by ₹{spent - budget_limit:.2f}"
        elif remaining < budget_limit * 0.2:  
            status = "⚠️ WARNING: Only 20% of budget left"
        else:
            status = "✅ Within budget"
        
        return {
            'category': category,
            'budget': budget_limit,
            'spent': spent,
            'remaining': remaining,
            'status': status
        }
    
    def clear_all(self):
        count = len(self.expenses)
        self.expenses = []
        return count



