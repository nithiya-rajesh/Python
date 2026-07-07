from .expense import Expense
from .expense_manager import ExpenseManager
from .file_handler import FileHandler
from .reports import ReportGenerator

class FinanceTracker:
    """Main Finance Tracker Application"""
    
    def __init__(self):
        self.manager = ExpenseManager()
        self.file_handler = FileHandler()
        self.report_generator = ReportGenerator(self.manager)
        self.load_data()
    
    def load_data(self):
        expenses_data, budgets_data = self.file_handler.load_expenses()
        for exp_data in expenses_data:
            expense = Expense.from_dict(exp_data)
            self.manager.expenses.append(expense)
        self.manager.budget = budgets_data
    
    def save_data(self):
        self.file_handler.save_expenses(
            self.manager.get_all_expenses(),
            self.manager.budget
        )
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (0-9): ").strip()
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.search_expenses()
            elif choice == '4':
                self.generate_monthly_report()
            elif choice == '5':
                self.view_category_breakdown()
            elif choice == '6':
                self.set_budget()
            elif choice == '7':
                self.view_budget_status()
            elif choice == '8':
                self.export_data()
            elif choice == '9':
                self.view_statistics()
            elif choice == '0':
                self.save_data()
                print("\n" + "=" * 60)
                print("Thank you for using Personal Finance Tracker!")
                print("=" * 60 + "\n")
                break
            else:
                print("❌ Invalid choice! Please enter 0-9.")
    
    def display_menu(self):
        print("\n" + "=" * 60)
        print("PERSONAL FINANCE TRACKER - MAIN MENU")
        print("=" * 60)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Search Expenses")
        print("4. Generate Monthly Report")
        print("5. View Category Breakdown")
        print("6. Set/Update Budget")
        print("7. View Budget Status")
        print("8. Export Data to CSV")
        print("9. View Statistics")
        print("0. Exit")
        print("=" * 60)
    
    def add_expense(self):
        print("\n--- ADD NEW EXPENSE ---")
        date = input("Enter date (YYYY-MM-DD) [default: today]: ").strip()
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            amount = float(input("Enter amount (₹): ").strip())
        except ValueError:
            print("❌ Invalid amount!")
            return
        print("\nAvailable categories:")
        for i, cat in enumerate(Expense.VALID_CATEGORIES, 1):
            print(f"  {i}. {cat}")
        cat_choice = input("Select category (number or name): ").strip()
        try:
            if cat_choice.isdigit():
                category = Expense.VALID_CATEGORIES[int(cat_choice) - 1]
            else:
                category = cat_choice
        except (IndexError, ValueError):
            print("❌ Invalid category!")
            return
        description = input("Enter description: ").strip()
        if self.manager.add_expense(date, amount, category, description):
            self.save_data()
    
    def view_expenses(self):
        print("\n--- ALL EXPENSES ---")
        expenses = self.manager.get_all_expenses()
        if not expenses:
            print("No expenses found.")
            return
        print(f"\n{'Date':<12} {'Amount':<12} {'Category':<15} {'Description':<20}")
        print("-" * 60)
        for i, expense in enumerate(expenses, 1):
            print(f"{expense.date:<12} ₹{expense.amount:<11.2f} {expense.category:<15} {expense.description:<20}")
        total = self.manager.get_total_spent()
        print("-" * 60)
        print(f"TOTAL: ₹{total:.2f} ({len(expenses)} expenses)")
    
    def search_expenses(self):
        print("\n--- SEARCH EXPENSES ---")
        print("1. Search by category")
        print("2. Search by date range")
        search_type = input("Enter choice (1-2): ").strip()
        if search_type == '1':
            category = input("Enter category: ").strip()
            results = self.manager.search_by_category(category)
        elif search_type == '2':
            start = input("Enter start date (YYYY-MM-DD): ").strip()
            end = input("Enter end date (YYYY-MM-DD): ").strip()
            results = self.manager.search_by_date_range(start, end)
        else:
            print("❌ Invalid choice!")
            return
        if results:
            print(f"\nFound {len(results)} expense(s):")
            for expense in results:
                print(f"  {expense}")
        else:
            print("No expenses found matching criteria.")
    
    def generate_monthly_report(self):
        print("\n--- MONTHLY REPORT ---")
        try:
            year = int(input("Enter year (YYYY): ").strip())
            month = int(input("Enter month (1-12): ").strip())
        except ValueError:
            print("❌ Invalid input!")
            return
        self.report_generator.print_monthly_summary(year, month)
    
    def view_category_breakdown(self):
        print("\n--- CATEGORY BREAKDOWN ---")
        self.report_generator.print_category_breakdown()
    
    def set_budget(self):
        print("\n--- SET BUDGET ---")
        print("Available categories:")
        for i, cat in enumerate(Expense.VALID_CATEGORIES, 1):
            print(f"  {i}. {cat}")
        cat_choice = input("Select category: ").strip()
        try:
            if cat_choice.isdigit():
                category = Expense.VALID_CATEGORIES[int(cat_choice) - 1]
            else:
                category = cat_choice
        except IndexError:
            print("❌ Invalid category!")
            return
        try:
            amount = float(input("Enter budget amount (₹): ").strip())
        except ValueError:
            print("❌ Invalid amount!")
            return
        if self.manager.set_budget(category, amount):
            self.save_data()
    
    def view_budget_status(self):
        print("\n--- BUDGET STATUS ---")
        comparison = self.report_generator.budget_comparison()
        if not comparison['categories']:
            print("No budgets set yet.")
            return
        print(f"\n{'Category':<15} {'Budget':<12} {'Spent':<12} {'Remaining':<12} {'Status'}")
        print("-" * 70)
        for cat in comparison['categories']:
            print(
                f"{cat['category']:<15} "
                f"₹{cat['budget']:<11.2f} "
                f"₹{cat['spent']:<11.2f} "
                f"₹{cat['remaining']:<11.2f} "
                f"{cat['status']}"
            )
        print("-" * 70)
        print(
            f"{'TOTAL':<15} "
            f"₹{comparison['total_budget']:<11.2f} "
            f"₹{comparison['total_spent']:<11.2f} "
            f"₹{comparison['total_remaining']:<11.2f}"
        )
    
    def export_data(self):
        print("\n--- EXPORT DATA ---")
        expenses = self.manager.get_all_expenses()
        self.file_handler.export_to_csv(expenses)
    
    def view_statistics(self):
        print("\n--- STATISTICS ---")
        expenses = self.manager.get_all_expenses()
        if not expenses:
            print("No expenses to analyze.")
            return
        total = self.manager.get_total_spent()
        avg = total / len(expenses) if expenses else 0
        highest = max(expenses, key=lambda e: e.amount)
        lowest = min(expenses, key=lambda e: e.amount)
        print(f"\nTotal expenses: {len(expenses)}")
        print(f"Total spent: ₹{total:.2f}")
        print(f"Average per expense: ₹{avg:.2f}")
        print(f"Highest: ₹{highest.amount:.2f} ({highest.category})")
        print(f"Lowest: ₹{lowest.amount:.2f} ({lowest.category})")


def main():
    app = FinanceTracker()
    app.run()


if __name__ == "__main__":
    main()
