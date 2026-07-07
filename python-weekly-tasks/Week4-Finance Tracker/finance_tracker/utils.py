from datetime import datetime
import json


def format_currency(amount, currency_symbol='₹'):
    return f"{currency_symbol}{amount:,.2f}"


def format_date(date_str, output_format='%d-%b-%Y'):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str


def get_month_name(month_num):
    months = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    if 1 <= month_num <= 12:
        return months[month_num - 1]
    return 'Invalid'


def get_current_year_month():
    now = datetime.now()
    return now.year, now.month


def validate_date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return start <= end
    except ValueError:
        return False


def round_to_cents(amount):
    return round(amount, 2)


def calculate_percentage(part, total):
    if total == 0:
        return 0.0
    return (part / total) * 100


def truncate_string(text, max_length=20):
    if len(text) > max_length:
        return text[:max_length-3] + '...'
    return text


def print_separator(char='=', width=60):
    print(char * width)


def get_expense_summary(expenses):
    if not expenses:
        return {'count': 0, 'total': 0, 'average': 0}
    total = sum(e.amount for e in expenses)
    average = total / len(expenses)
    return {
        'count': len(expenses),
        'total': total,
        'average': average
    }


def save_json(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        return False


def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return {}
