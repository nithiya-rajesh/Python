from datetime import datetime
from collections import defaultdict


class ReportGenerator:
    """Generates various financial reports and visualizations."""

    def __init__(self, expense_manager):
        self.manager = expense_manager
    
    def monthly_summary(self, year, month):
        monthly_expenses = self.manager.get_monthly_expenses(year, month)
        total = sum(e.amount for e in monthly_expenses) or 0
        by_category = defaultdict(list)
        for expense in monthly_expenses:
            by_category[expense.category].append(expense)
        category_summary = {}
        for category, expenses in by_category.items():
            total_amount = sum(e.amount for e in expenses)
            count = len(expenses)
            category_summary[category] = {
                'total': total_amount,
                'count': count,
                'average': total_amount / count if count > 0 else 0
            }
        return {
            'month': f"{year}-{month:02d}",
            'total_spent': total,
            'expense_count': len(monthly_expenses),
            'by_category': category_summary,
            'num_categories': len(category_summary)
        }
    
    def category_breakdown(self):
        categories = self.manager.get_all_categories()
        total_spent = self.manager.get_total_spent()
        breakdown = []
        for category in categories:
            amount = self.manager.get_category_total(category)
            percentage = (amount / total_spent * 100) if total_spent > 0 else 0
            count = len(self.manager.search_by_category(category))
            breakdown.append({
                'category': category,
                'amount': amount,
                'percentage': percentage,
                'count': count
            })
        breakdown.sort(key=lambda x: x['amount'], reverse=True)
        return {
            'total': total_spent,
            'categories': breakdown,
            'num_categories': len(breakdown)
        }
    
    def spending_trend(self, start_date, end_date):
        expenses = self.manager.search_by_date_range(start_date, end_date)
        monthly_totals = defaultdict(float)
        for expense in expenses:
            month = expense.date[:7]
            monthly_totals[month] += expense.amount
        sorted_months = sorted(monthly_totals.items())
        return {
            'start_date': start_date,
            'end_date': end_date,
            'monthly_totals': dict(sorted_months),
            'total_period': sum(e.amount for e in expenses),
            'average_monthly': sum(monthly_totals.values()) / len(monthly_totals) if monthly_totals else 0
        }
    
    def budget_comparison(self):
        categories_with_budget = self.manager.budget.keys()
        comparisons = []
        for category in categories_with_budget:
            status = self.manager.get_budget_status(category)
            comparisons.append(status)
        total_budget = sum(self.manager.budget.values())
        total_spent = sum(self.manager.get_category_total(cat) for cat in categories_with_budget)
        return {
            'total_budget': total_budget,
            'total_spent': total_spent,
            'total_remaining': total_budget - total_spent,
            'categories': comparisons,
            'is_over_budget': total_spent > total_budget
        }
    
    def text_chart(self, title, data_dict, max_width=50):
        if not data_dict:
            return "No data to display"
        max_value = max(data_dict.values())
        if max_value == 0:
            return "All values are 0"
        chart = f"\n{title}\n"
        chart += "=" * (len(title) + 10) + "\n"
        for label, value in data_dict.items():
            bar_length = int((value / max_value) * max_width)
            bar = '█' * bar_length
            chart += f"{label:<15} │{bar:<{max_width}}│ ₹{value:>8.2f}\n"
        return chart
    
    def print_monthly_summary(self, year, month):
        report = self.monthly_summary(year, month)
        print("\n" + "=" * 60)
        print(f"MONTHLY SUMMARY - {report['month']}")
        print("=" * 60)
        print(f"\nTotal Spent: ₹{report['total_spent']:.2f}")
        print(f"Number of Transactions: {report['expense_count']}")
        print(f"Number of Categories: {report['num_categories']}")
        if report['by_category']:
            print("\n" + "-" * 40)
            print("BREAKDOWN BY CATEGORY:")
            print("-" * 40)
            for category, data in report['by_category'].items():
                print(f"\n{category}:")
                print(f"  Total: ₹{data['total']:.2f}")
                print(f"  Count: {data['count']} transactions")
                print(f"  Average: ₹{data['average']:.2f}")
    
    def print_category_breakdown(self):
        breakdown = self.category_breakdown()
        print("\n" + "=" * 60)
        print("CATEGORY BREAKDOWN")
        print("=" * 60)
        print(f"\nTotal Spending: ₹{breakdown['total']:.2f}")
        chart_data = {cat['category']: cat['amount'] for cat in breakdown['categories']}
        print(self.text_chart("Spending by Category", chart_data))
        print("\nDETAILED BREAKDOWN:")
        print("-" * 60)
        for category in breakdown['categories']:
            print(
                f"{category['category']:<15} "
                f"₹{category['amount']:>10.2f}  "
                f"({category['percentage']:>5.1f}%)  "
                f"({category['count']} transactions)"
            )
