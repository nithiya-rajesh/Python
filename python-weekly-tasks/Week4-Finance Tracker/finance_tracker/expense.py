"""
EXPENSE MODULE - Week 4 Finance Tracker
========================================

This module defines the Expense class, which represents a single financial transaction.
Each expense has a date, amount, category, and description.
"""

from datetime import datetime  
import json  


class Expense:
    
    VALID_CATEGORIES = [
        'Food',           # For meals, groceries, restaurants
        'Transport',      # For fuel, public transport, taxi
        'Entertainment',  # For movies, games, hobbies
        'Bills',          # For utilities, rent, insurance
        'Shopping',       # For clothes, accessories, household items
        'Healthcare',     # For doctor visits, medicine, gym
        'Education',      # For books, courses, tuition
        'Other'           # For miscellaneous expenses
    ]
    
    # Line 4: Define default category if none specified
    DEFAULT_CATEGORY = 'Other'
    
    def __init__(self, date, amount, category, description):
        self.date = self.validate_date(date)
        self.amount = self.validate_amount(amount)
        self.category = self.validate_category(category)
        self.description = str(description).strip()
        self.created_at = datetime.now().isoformat()
    
    @staticmethod
    def validate_date(date_str):
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")
    
    @staticmethod
    def validate_amount(amount):
        
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                raise ValueError("Amount must be greater than 0")
            return amount_float
        except ValueError as e:
            if "must be greater" in str(e):
                raise
            raise ValueError(f"Invalid amount: {amount}. Please enter a valid number")
    
    @staticmethod
    def validate_category(category):

        category = category.strip() if category else Expense.DEFAULT_CATEGORY

        if category not in Expense.VALID_CATEGORIES:
            valid_options = ', '.join(Expense.VALID_CATEGORIES)

            raise ValueError(
                f"Invalid category: {category}. "
                f"Valid categories: {valid_options}"
            )
        
        return category
    
    def to_dict(self):

        return {
            'date': self.date,              # Include the date
            'amount': self.amount,          # Include the amount
            'category': self.category,      # Include the category
            'description': self.description,  # Include the description
            'created_at': self.created_at   # Include creation timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
    
        return cls(
            date=data['date'],              # Get date from dictionary
            amount=data['amount'],          # Get amount from dictionary
            category=data['category'],      # Get category from dictionary
            description=data['description']  # Get description from dictionary
        )
    
    def __str__(self):
        return (
            f"Date: {self.date:>10} | "           # Date right-aligned in 10 chars
            f"Amount: ₹{self.amount:>8.2f} | "    # Amount as currency with 2 decimals
            f"Category: {self.category:<15} | "   # Category left-aligned in 15 chars
            f"Description: {self.description}"     # Description as-is
        )
    
    def __repr__(self):

        return (
            f"Expense(date='{self.date}', "
            f"amount={self.amount}, "
            f"category='{self.category}', "
            f"description='{self.description}')"
        )


