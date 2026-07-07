"""
Finance Tracker Package
=======================

A complete personal finance tracking application built with Python.

Modules:
    - expense: Expense class for individual transactions
    - expense_manager: Manager for expense collection
    - file_handler: File I/O operations
    - reports: Report generation
    - main: Main application
"""

__version__ = "1.0.0"
__author__ = "Finance Tracker Team"

from .expense import Expense
from .expense_manager import ExpenseManager
from .file_handler import FileHandler
from .reports import ReportGenerator

__all__ = [
    'Expense',
    'ExpenseManager',
    'FileHandler',
    'ReportGenerator',
]
