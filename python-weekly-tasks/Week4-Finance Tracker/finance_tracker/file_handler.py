import json
import csv
import os
from datetime import datetime
from pathlib import Path


class FileHandler:
    
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.backup_dir = self.data_dir / 'backup'
        self.export_dir = self.data_dir / 'exports'
        self.data_file = self.data_dir / 'expenses.json'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def save_expenses(self, expenses, budgets=None):
        try:
            self.create_backup()
            expense_dicts = [expense.to_dict() for expense in expenses]
            data = {
                'expenses': expense_dicts,
                'budgets': budgets or {},
                'last_saved': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            return False
        except IOError:
            return False
    
    def load_expenses(self):
        try:
            if not self.data_file.exists():
                return [], {}
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            expenses = data.get('expenses', [])
            budgets = data.get('budgets', {})
            return expenses, budgets
        except FileNotFoundError:
            return [], {}
        except json.JSONDecodeError:
            self.create_backup(suffix='_corrupted')
            return [], {}
        except IOError:
            return [], {}
    
    def create_backup(self, suffix=''):
        if not self.data_file.exists():
            return False
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_name = f"expenses_{timestamp}{suffix}.json"
            backup_path = self.backup_dir / backup_name
            with open(self.data_file, 'rb') as source:
                file_content = source.read()
            with open(backup_path, 'wb') as backup:
                backup.write(file_content)
            return True
        except IOError:
            return False
    
    def export_to_csv(self, expenses):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            csv_name = f"expenses_{today}.csv"
            csv_path = self.export_dir / csv_name
            if not expenses:
                return False
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=['date', 'amount', 'category', 'description', 'created_at']
                )
                writer.writeheader()
                for expense in expenses:
                    writer.writerow(expense.to_dict())
            return True
        except IOError:
            return False
    
    def import_from_csv(self, file_path):
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            return rows
        except IOError:
            return []
    
    def file_exists(self, file_path):
        return Path(file_path).exists()
    
    def get_backup_list(self):
        if not self.backup_dir.exists():
            return []
        backups = list(self.backup_dir.glob('*.json'))
        backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return [backup.name for backup in backups]
