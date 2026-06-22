'''
Week 3 Project - Functions & Dictionaries

Project: Contact Management System
Author: Nithiya Rajendran
Description: A dictionary-based contact manager with full CRUD operations, 
             input validation, formatted display, search (name/phone), 
             statistics, and file persistence (JSON/CSV).
'''
import json
import re
from datetime import datetime
import csv

# -------------------------------
# Validation Helpers
# -------------------------------
def validate_phone(phone):
    """Validate phone number format"""
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# -------------------------------
# CRUD Functions
# -------------------------------
def add_contact(contacts):
    print("\n--- ADD NEW CONTACT ---")
    while True:
        name = input("Enter contact name: ").strip()
        if name:
            if name in contacts:
                print(f"Contact '{name}' already exists!")
                choice = input("Do you want to update instead? (y/n): ").lower()
                if choice == 'y':
                    update_contact(contacts, name)
                    return contacts
            break
        print("Name cannot be empty!")

    while True:
        phone = input("Enter phone number: ").strip()
        is_valid, cleaned_phone = validate_phone(phone)
        if is_valid:
            break
        print("Invalid phone number! Please enter 10-15 digits.")

    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if not email or validate_email(email):
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    contacts[name] = {
        'phone': cleaned_phone,
        'email': email if email else None,
        'address': address if address else None,
        'group': group,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    print(f"✅ Contact '{name}' added successfully!")
    return contacts

def update_contact(contacts, name):
    if name not in contacts:
        print("❌ Contact not found.")
        return
    print(f"\n--- UPDATE CONTACT: {name} ---")
    phone = input("New phone (leave blank to skip): ").strip()
    if phone:
        is_valid, cleaned_phone = validate_phone(phone)
        if is_valid:
            contacts[name]['phone'] = cleaned_phone
        else:
            print("Invalid phone number, skipped.")

    email = input("New email (leave blank to skip): ").strip()
    if email and validate_email(email):
        contacts[name]['email'] = email

    address = input("New address (leave blank to skip): ").strip()
    if address:
        contacts[name]['address'] = address

    group = input("New group (leave blank to skip): ").strip()
    if group:
        contacts[name]['group'] = group

    contacts[name]['updated_at'] = datetime.now().isoformat()
    print(f"✅ Contact '{name}' updated successfully!")

def delete_contact(contacts, name):
    if name in contacts:
        confirm = input(f"Delete {name}? (y/n): ").lower()
        if confirm == 'y':
            del contacts[name]
            print(f"✅ Contact '{name}' deleted.")
    else:
        print("❌ Contact not found.")

def search_contacts(contacts, search_term):
    search_term = search_term.lower()
    results = {n: i for n, i in contacts.items() if search_term in n.lower()}
    return results

def search_by_phone(contacts, phone):
    results = {n: i for n, i in contacts.items() if i.get('phone') == phone}
    return results

def display_results(results):
    if not results:
        print("No contacts found.")
        return
    print(f"\nFound {len(results)} contact(s):")
    print("-" * 50)
    for i, (name, info) in enumerate(results.items(), 1):
        print(f"{i}. {name}")
        print(f"   📞 Phone: {info.get('phone','N/A')}")
        if info.get('email'):
            print(f"   📧 Email: {info['email']}")
        if info.get('address'):
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info.get('group','Other')}")
        print(f"   🕒 Updated: {info.get('updated_at','N/A')}")
        print("-" * 50)

def display_all(contacts):
    if contacts:
        display_results(contacts)
    else:
        print("📭 No contacts available.")

# -------------------------------
# File Operations
# -------------------------------
def save_to_file(contacts, filename="contacts.json"):
    with open(filename, "w") as f:
        json.dump(contacts, f, indent=4)
    print("💾 Contacts saved.")

def load_from_file(filename="contacts.json"):
    try:
        with open(filename, "r") as f:
            contacts = json.load(f)
        # Normalize missing fields
        for info in contacts.values():
            if "group" not in info:
                info["group"] = "Other"
            if "created_at" not in info:
                info["created_at"] = datetime.now().isoformat()
            if "updated_at" not in info:
                info["updated_at"] = datetime.now().isoformat()
        return contacts
    except FileNotFoundError:
        return {}

def export_to_csv(contacts, filename="contacts.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group", "Created At", "Updated At"])
        for name, info in contacts.items():
            writer.writerow([
                name,
                info.get('phone',''),
                info.get('email',''),
                info.get('address',''),
                info.get('group','Other'),
                info.get('created_at',''),
                info.get('updated_at','')
            ])
    print("📑 Contacts exported to CSV.")

# -------------------------------
# Statistics
# -------------------------------
def show_stats(contacts):
    print(f"📊 Total contacts: {len(contacts)}")
    groups = {}
    for info in contacts.values():
        g = info.get('group', 'Other')
        groups[g] = groups.get(g, 0) + 1
    for group, count in groups.items():
        print(f"   {group}: {count}")

# -------------------------------
# Menu System
# -------------------------------
def menu():
    contacts = load_from_file()
    while True:
        print("\n--- Contact Manager ---")
        print("1. Add Contact")
        print("2. Search Contact by Name")
        print("3. Search Contact by Phone")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Display All Contacts")
        print("7. Export to CSV")
        print("8. Show Statistics")
        print("9. Save & Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            query = input("Search name: ")
            results = search_contacts(contacts, query)
            display_results(results)
        elif choice == "3":
            phone = input("Search phone: ")
            results = search_by_phone(contacts, phone)
            display_results(results)
        elif choice == "4":
            name = input("Name to update: ")
            update_contact(contacts, name)
        elif choice == "5":
            name = input("Name to delete: ")
            delete_contact(contacts, name)
        elif choice == "6":
            display_all(contacts)
        elif choice == "7":
            export_to_csv(contacts)
        elif choice == "8":
            show_stats(contacts)
        elif choice == "9":
            save_to_file(contacts)
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    menu()
