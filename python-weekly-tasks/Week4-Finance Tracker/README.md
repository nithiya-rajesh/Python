# Personal Finance Tracker - Week 4 Project

## 📋 Project Overview

A comprehensive personal finance tracking application built with Python that helps users manage expenses, categorize spending, save data to files, and generate financial reports.

**Course**: Python Hands-On Practice - Week 4  
**Topic**: File Handling & Final Project  
**Status**: ✅ Complete and Tested  

---

## 🎯 Learning Objectives

This project demonstrates mastery of Week 4 concepts:

### Core Concepts Covered

1. **File Operations**
   - Reading from and writing to files
   - Using `with` statement for proper resource management
   - Error handling for file operations

2. **Data Persistence**
   - JSON format for storing complex data structures
   - CSV format for spreadsheet compatibility
   - Automatic backups before overwriting

3. **Code Organization**
   - Modular code structure with separate files
   - Class-based organization
   - Separation of concerns (data, logic, I/O, reporting)

4. **Error Handling**
   - Try-except blocks for file operations
   - Graceful error messages
   - Recovery from corrupted files

5. **Advanced Python**
   - List comprehensions
   - Dictionary operations
   - Object serialization/deserialization
   - Generator expressions

---

## 📂 Project Structure

```
week4-finance-tracker/
│
├── finance_tracker/                 # Main package
│   ├── __init__.py                 # Package initialization
│   ├── expense.py                  # Expense class (65 lines)
│   ├── expense_manager.py           # ExpenseManager class (280 lines)
│   ├── file_handler.py              # FileHandler class (300 lines)
│   ├── reports.py                   # ReportGenerator class (280 lines)
│   └── main.py                      # Main application (350 lines)
│
├── data/                            # Data directory (auto-created)
│   ├── expenses.json               # Main data file
│   ├── backup/                     # Backup files
│   └── exports/                    # CSV exports
│
├── tests/                           # Test files
│   ├── test_expense.py             # Unit tests for Expense
│   ├── test_expense_manager.py      # Unit tests for manager
│   └── test_file_handler.py         # Unit tests for file I/O
│
├── run.py                           # Entry point
├── requirements.txt                 # Dependencies (none!)
├── README.md                        # This file
├── CODE_EXPLANATION.md              # Line-by-line explanations
├── LINE_BY_LINE_GUIDE.md           # Detailed code walkthrough
└── .gitignore                       # Git ignore patterns
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- No external dependencies (uses only standard library)

### Installation

1. **Clone/Download the project**
```bash
cd week4-finance-tracker
```

2. **Run the application**
```bash
python run.py
```

3. **Start using it!**
   - Choose option 1 to add an expense
   - Explore other menu options
   - Data automatically saves to `data/expenses.json`

---

## 💻 Code Explanation

### LINE-BY-LINE BREAKDOWN

Each file contains detailed comments explaining every line of code:

#### **expense.py** - Expense Class (65 lines)
```python
# Line 1: Import datetime module
from datetime import datetime
# Line 2: Import json module  
import json

class Expense:
    # Line 3: Define valid categories list
    VALID_CATEGORIES = ['Food', 'Transport', 'Entertainment', ...]
    
    def __init__(self, date, amount, category, description):
        # Line 5: Validate and store date
        self.date = self.validate_date(date)
        
        # Line 6: Validate and store amount
        self.amount = self.validate_amount(amount)
        
        # Line 7: Validate and store category
        self.category = self.validate_category(category)
        
        # Line 8: Store description
        self.description = str(description).strip()
```

**Key Methods**:
- `validate_date()` - Checks date format (YYYY-MM-DD)
- `validate_amount()` - Ensures positive number
- `validate_category()` - Validates against list
- `to_dict()` - Convert to dictionary for JSON storage
- `from_dict()` - Create from dictionary

---

#### **expense_manager.py** - Expense Manager (280 lines)
```python
class ExpenseManager:
    def __init__(self):
        # Line 3: Initialize empty expenses list
        self.expenses = []
        
        # Line 4: Initialize empty budget dictionary
        self.budget = {}
    
    def add_expense(self, date, amount, category, description):
        # Line 6: Create new Expense object
        expense = Expense(date, amount, category, description)
        
        # Line 7: Add to list
        self.expenses.append(expense)
        
        # Line 8: Return True for success
        return True
```

**Key Methods**:
- `add_expense()` - Add expense with validation
- `remove_expense()` - Remove by index
- `search_by_category()` - Filter by category
- `search_by_date_range()` - Filter by date range
- `get_total_spent()` - Sum all expenses
- `set_budget()` - Set category budget

---

#### **file_handler.py** - File Operations (300 lines)
```python
class FileHandler:
    def __init__(self, data_dir='data'):
        # Line 6: Create Path object for data directory
        self.data_dir = Path(data_dir)
        
        # Line 7: Create Path for backup directory
        self.backup_dir = self.data_dir / 'backup'
        
        # Line 9: Create directories if don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_expenses(self, expenses, budgets=None):
        # Line 15: Create backup first
        self.create_backup()
        
        # Line 16: Convert expenses to dictionaries
        # Line 17: Open file for writing
        with open(self.data_file, 'w', encoding='utf-8') as f:
            # Line 18: Write data as formatted JSON
            json.dump(data, f, indent=2)
```

**Key Methods**:
- `save_expenses()` - Save to JSON with backup
- `load_expenses()` - Load from JSON
- `create_backup()` - Create timestamped backup
- `export_to_csv()` - Export for spreadsheets
- `import_from_csv()` - Import from CSV

---

#### **reports.py** - Reporting (280 lines)
```python
class ReportGenerator:
    def __init__(self, expense_manager):
        # Line 3: Store reference to manager
        self.manager = expense_manager
    
    def monthly_summary(self, year, month):
        # Line 4: Get expenses for month
        monthly_expenses = self.manager.get_monthly_expenses(year, month)
        
        # Line 5: Calculate total
        total = sum(e.amount for e in monthly_expenses)
        
        # Return dictionary with summary
        return {...}
```

**Key Methods**:
- `monthly_summary()` - Generate monthly report
- `category_breakdown()` - Show by category
- `spending_trend()` - Trend over time
- `budget_comparison()` - Actual vs budget
- `text_chart()` - Create text-based chart

---

#### **main.py** - Application (350 lines)
```python
class FinanceTracker:
    def __init__(self):
        # Line 1: Create expense manager
        self.manager = ExpenseManager()
        
        # Line 2: Create file handler
        self.file_handler = FileHandler()
        
        # Line 3: Create report generator
        self.report_generator = ReportGenerator(self.manager)
        
        # Line 4: Load previously saved data
        self.load_data()
    
    def run(self):
        # Line 11: Main menu loop
        while True:
            self.display_menu()
            choice = input("\nEnter choice: ").strip()
            
            # Line 14: Handle menu choices
            if choice == '1':
                self.add_expense()
```

---

### KEY PROGRAMMING CONCEPTS

#### 1. **File Operations with Context Manager**
```python
# ✅ CORRECT - Uses 'with' statement
with open(filename, 'r') as f:
    data = json.load(f)
    # File automatically closes here

# ❌ WRONG - Manual open/close
f = open(filename, 'r')
data = json.load(f)
f.close()  # Easy to forget!
```

#### 2. **Error Handling**
```python
try:
    # Attempt operation
    expense = Expense(date, amount, category, description)
except ValueError as e:
    # Handle validation error
    print(f"Error: {e}")
    return False
```

#### 3. **List Comprehension**
```python
# Get all expenses in a category
category_expenses = [e for e in self.expenses 
                     if e.category == category]

# Convert expenses to dictionaries
expense_dicts = [e.to_dict() for e in expenses]
```

#### 4. **Dictionary Operations**
```python
# Store budget limits
self.budget = {'Food': 5000, 'Transport': 2000}

# Get value with default
budget = self.budget.get('Food', 0)  # 5000

# Check if key exists
if 'Food' in self.budget:
    print(self.budget['Food'])
```

#### 5. **JSON Serialization**
```python
# Convert object to JSON
data = {'expenses': [e.to_dict() for e in expenses]}
with open('file.json', 'w') as f:
    json.dump(data, f, indent=2)

# Load from JSON back to object
with open('file.json', 'r') as f:
    data = json.load(f)
    expense = Expense.from_dict(data)
```

---

## 📊 Features

### ✅ Core Features Implemented

1. **Add Expenses**
   - Date validation (YYYY-MM-DD)
   - Amount validation (positive numbers)
   - Category selection
   - Description

2. **View Expenses**
   - List all expenses
   - Show date, amount, category, description
   - Display total

3. **Search**
   - Search by category
   - Search by date range
   - Display matching expenses

4. **Budgets**
   - Set budget per category
   - Track spending vs budget
   - Warning if over budget

5. **Reports**
   - Monthly summary
   - Category breakdown with chart
   - Spending statistics
   - Budget comparison

6. **Data Persistence**
   - Save to JSON file
   - Load on startup
   - Automatic backups
   - Export to CSV

---

## 🧪 Testing

### Run Unit Tests
```bash
python -m pytest tests/
```

### Manual Testing

1. **Add Expense**
   - Run app, choose option 1
   - Enter date, amount, category, description
   - Verify saved to `data/expenses.json`

2. **View All**
   - Choose option 2
   - Verify all expenses display

3. **Search**
   - Choose option 3
   - Search by category or date

4. **Reports**
   - Choose option 4 for monthly
   - Choose option 5 for categories

5. **Export**
   - Choose option 8
   - Check `data/exports/` folder

---

## 📝 Data Format

### JSON Format
```json
{
  "expenses": [
    {
      "date": "2024-01-15",
      "amount": 500.0,
      "category": "Food",
      "description": "Lunch at restaurant",
      "created_at": "2024-01-15T10:30:45.123456"
    }
  ],
  "budgets": {
    "Food": 5000,
    "Transport": 2000
  },
  "last_saved": "2024-01-15T10:30:45.123456"
}
```

### CSV Format
```csv
date,amount,category,description,created_at
2024-01-15,500.0,Food,Lunch at restaurant,2024-01-15T10:30:45.123456
2024-01-16,150.0,Transport,Bus fare,2024-01-16T08:00:00.000000
```

---

## 🔍 Validation Rules

### Date Format
- Format: `YYYY-MM-DD` (e.g., `2024-01-15`)
- Validation: `datetime.strptime()` ensures valid date

### Amount
- Must be positive number
- Can be integer or decimal (e.g., `500` or `500.50`)
- Stored as float with 2 decimal places

### Categories
Valid categories:
- Food
- Transport
- Entertainment
- Bills
- Shopping
- Healthcare
- Education
- Other

### Description
- Any text (stripped of leading/trailing whitespace)
- Optional (can be empty)

---

## 🎓 Key Learnings

### Week 1-3 Concepts Reviewed
- ✅ Variables and data types
- ✅ Control flow (if/else, loops)
- ✅ Functions and parameters
- ✅ Dictionaries and lists
- ✅ String methods

### Week 4 New Concepts
- ✅ File I/O with context managers
- ✅ JSON serialization
- ✅ CSV file handling
- ✅ Error handling for file operations
- ✅ Project organization

---

## 🐛 Error Handling

### File-Related Errors
```python
# Handle missing files
except FileNotFoundError:
    print("File not found. Starting fresh.")
    return [], {}

# Handle permission errors
except PermissionError:
    print("Cannot write to file. Check permissions.")

# Handle corrupted JSON
except json.JSONDecodeError:
    print("File corrupted. Creating backup...")
    return [], {}
```

### Data Validation Errors
```python
# Invalid date format
try:
    datetime.strptime(date_str, '%Y-%m-%d')
except ValueError:
    raise ValueError("Invalid date. Use YYYY-MM-DD")

# Invalid amount
if amount <= 0:
    raise ValueError("Amount must be positive")

# Invalid category
if category not in VALID_CATEGORIES:
    raise ValueError(f"Invalid category: {category}")
```

---

## 📚 Additional Documentation

See separate files for more details:
- **CODE_EXPLANATION.md** - Detailed code walkthrough
- **LINE_BY_LINE_GUIDE.md** - Every line explained
- **ARCHITECTURE.md** - Design patterns and structure

---

## 🔧 Configuration

### Change Default Directory
```python
# In main.py
file_handler = FileHandler(data_dir='my_data')
```

### Add New Category
```python
# In expense.py - Add to VALID_CATEGORIES
VALID_CATEGORIES = [
    'Food',
    'Transport',
    'MyNewCategory',  # Add here
    ...
]
```

---

## 🚨 Troubleshooting

### Issue: "No expenses found"
- **Cause**: First run or deleted data file
- **Solution**: Add an expense (option 1)

### Issue: Import error on startup
- **Cause**: Wrong directory or Python path
- **Solution**: Run from project root: `python run.py`

### Issue: Cannot write to file
- **Cause**: Permission denied
- **Solution**: Check folder permissions, move project folder

### Issue: Data not saving
- **Cause**: Crash before save_data() called
- **Solution**: Choose exit (option 0) to save

---

## 📈 Future Enhancements

Possible improvements:
1. Database integration (SQLite)
2. Recurring expenses
3. Pie charts with matplotlib
4. Web interface with Flask
5. Mobile app compatibility
6. Data encryption
7. Multi-user support
8. Cloud backup

---

## 📄 License

This project is for educational purposes.

---




Enjoy tracking your finances! 💰
