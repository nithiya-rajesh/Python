# Contact Management System
# Week 3 Project - Functions & Dictionaries

import json
import re
import os
from datetime import datetime
import csv

# ==================== VALIDATION FUNCTIONS ====================

def validate_phone(phone):
    """Validate phone number format (10-15 digits)"""
    digits = re.sub(r'\D', '', phone)
    
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_name(name):
    """Validate contact name"""
    return len(name.strip()) > 0

# ==================== FILE OPERATIONS ====================

def load_from_file(filename='contacts_data.json'):
    """Load contacts from JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            print("✅ No existing contacts file found. Starting fresh.\n")
            return {}
    except json.JSONDecodeError:
        print("⚠️  Error reading contacts file. Starting fresh.\n")
        return {}
    except Exception as e:
        print(f"⚠️  Error loading contacts: {e}\n")
        return {}

def save_to_file(contacts, filename='contacts_data.json'):
    """Save contacts to JSON file"""
    try:
        with open(filename, 'w') as file:
            json.dump(contacts, file, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving contacts: {e}")
        return False

def create_backup(filename='contacts_data.json'):
    """Create a backup of the contacts file"""
    if os.path.exists(filename):
        backup_name = f"contacts_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'r') as original:
                with open(backup_name, 'w') as backup:
                    backup.write(original.read())
            print(f"✅ Backup created: {backup_name}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    return False

# ==================== CRUD FUNCTIONS ====================

def add_contact(contacts):
    """Add a new contact to the dictionary"""
    print("\n" + "="*50)
    print("ADD NEW CONTACT")
    print("="*50)
    
    # Get contact name
    while True:
        name = input("\nEnter contact name: ").strip()
        if validate_name(name):
            if name in contacts:
                print(f"❌ Contact '{name}' already exists!")
                choice = input("Do you want to update instead? (y/n): ").lower()
                if choice == 'y':
                    update_contact(contacts, name)
                    return contacts
            else:
                break
        else:
            print("❌ Name cannot be empty!")
    
    # Get phone number with validation
    while True:
        phone = input("Enter phone number (e.g., +1-234-567-8900): ").strip()
        is_valid, cleaned_phone = validate_phone(phone)
        if is_valid:
            break
        print("❌ Invalid phone number! Please enter 10-15 digits.")
    
    # Get email with validation
    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if not email or validate_email(email):
            break
        print("❌ Invalid email format!")
    
    # Get additional info
    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"
    
    # Store in dictionary
    contacts[name] = {
        'phone': cleaned_phone,
        'email': email if email else None,
        'address': address if address else None,
        'group': group,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    print(f"\n✅ Contact '{name}' added successfully!")
    
    # Save to file
    if save_to_file(contacts):
        print("✅ Contacts saved to contacts_data.json")
    
    return contacts

def search_contacts(contacts, search_term=None):
    """Search contacts by name (partial match)"""
    if search_term is None:
        search_term = input("\nEnter name to search: ").strip()
    
    if not search_term:
        print("❌ Search term cannot be empty!")
        return {}
    
    search_term = search_term.lower()
    results = {}
    
    for name, info in contacts.items():
        if search_term in name.lower():
            results[name] = info
    
    return results

def display_search_results(results):
    """Display search results in formatted way"""
    if not results:
        print("\n❌ No contacts found.")
        return
    
    print(f"\n{'='*60}")
    print(f"Found {len(results)} contact(s):")
    print('='*60)
    
    for i, (name, info) in enumerate(results.items(), 1):
        print(f"\n{i}. {name}")
        print(f"   📞 Phone: {info['phone']}")
        if info['email']:
            print(f"   📧 Email: {info['email']}")
        if info['address']:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}")
    print('='*60)

def search_contact_menu(contacts):
    """Menu-driven search function"""
    print("\n" + "="*50)
    print("SEARCH CONTACT")
    print("="*50)
    
    results = search_contacts(contacts)
    display_search_results(results)

def search_by_phone(contacts, phone_term=None):
    """Search contacts by phone number"""
    if phone_term is None:
        phone_term = input("\nEnter phone number to search: ").strip()
    
    phone_digits = re.sub(r'\D', '', phone_term)
    results = {}
    
    for name, info in contacts.items():
        if phone_digits in info['phone']:
            results[name] = info
    
    return results

def update_contact(contacts, name=None):
    """Update an existing contact"""
    print("\n" + "="*50)
    print("UPDATE CONTACT")
    print("="*50)
    
    # Get contact name if not provided
    if name is None:
        name = input("\nEnter contact name to update: ").strip()
    
    if name not in contacts:
        print(f"❌ Contact '{name}' not found!")
        return contacts
    
    contact = contacts[name]
    print(f"\nUpdating contact: {name}")
    print(f"  Current phone: {contact['phone']}")
    print(f"  Current email: {contact['email']}")
    print(f"  Current address: {contact['address']}")
    print(f"  Current group: {contact['group']}")
    
    # Update phone
    while True:
        new_phone = input("\nEnter new phone number (or press Enter to keep current): ").strip()
        if not new_phone:
            break
        is_valid, cleaned_phone = validate_phone(new_phone)
        if is_valid:
            contact['phone'] = cleaned_phone
            break
        print("❌ Invalid phone number!")
    
    # Update email
    while True:
        new_email = input("Enter new email (or press Enter to keep current): ").strip()
        if not new_email:
            break
        if validate_email(new_email):
            contact['email'] = new_email
            break
        print("❌ Invalid email format!")
    
    # Update address
    new_address = input("Enter new address (or press Enter to keep current): ").strip()
    if new_address:
        contact['address'] = new_address
    
    # Update group
    new_group = input("Enter new group (or press Enter to keep current): ").strip()
    if new_group:
        contact['group'] = new_group
    
    contact['updated_at'] = datetime.now().isoformat()
    
    print(f"\n✅ Contact '{name}' updated successfully!")
    
    # Save to file
    if save_to_file(contacts):
        print("✅ Contacts saved to contacts_data.json")
    
    return contacts

def delete_contact(contacts, name=None):
    """Delete a contact with confirmation"""
    print("\n" + "="*50)
    print("DELETE CONTACT")
    print("="*50)
    
    # Get contact name if not provided
    if name is None:
        name = input("\nEnter contact name to delete: ").strip()
    
    if name not in contacts:
        print(f"❌ Contact '{name}' not found!")
        return contacts
    
    # Show contact details
    contact = contacts[name]
    print(f"\nContact to delete:")
    print(f"  Name: {name}")
    print(f"  Phone: {contact['phone']}")
    print(f"  Email: {contact['email']}")
    print(f"  Group: {contact['group']}")
    
    # Confirmation
    confirmation = input(f"\nAre you sure you want to delete '{name}'? (yes/no): ").lower()
    if confirmation == 'yes':
        del contacts[name]
        print(f"\n✅ Contact '{name}' deleted successfully!")
        
        # Save to file
        if save_to_file(contacts):
            print("✅ Contacts saved to contacts_data.json")
    else:
        print("❌ Deletion cancelled.")
    
    return contacts

def display_all_contacts(contacts):
    """Display all contacts in formatted way"""
    print("\n" + "="*60)
    
    if not contacts:
        print("No contacts found. Add one to get started!")
        print("="*60)
        return
    
    print(f"ALL CONTACTS ({len(contacts)} total)")
    print("="*60)
    
    for i, (name, info) in enumerate(contacts.items(), 1):
        print(f"\n{i}. {name}")
        print(f"   📞 {info['phone']}")
        if info['email']:
            print(f"   📧 {info['email']}")
        if info['address']:
            print(f"   📍 {info['address']}")
        print(f"   👥 {info['group']}")
    
    print("\n" + "="*60)

def export_to_csv(contacts, filename='contacts_export.csv'):
    """Export contacts to CSV file"""
    if not contacts:
        print("❌ No contacts to export!")
        return
    
    try:
        with open(filename, 'w', newline='') as file:
            fieldnames = ['Name', 'Phone', 'Email', 'Address', 'Group', 'Created', 'Updated']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for name, info in contacts.items():
                writer.writerow({
                    'Name': name,
                    'Phone': info['phone'],
                    'Email': info['email'] or '',
                    'Address': info['address'] or '',
                    'Group': info['group'],
                    'Created': info['created_at'],
                    'Updated': info['updated_at']
                })
        
        print(f"✅ Contacts exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")

# ==================== STATISTICS & ANALYTICS ====================

def view_statistics(contacts):
    """Display contact statistics"""
    print("\n" + "="*50)
    print("CONTACT STATISTICS")
    print("="*50)
    
    if not contacts:
        print("\nNo contacts to analyze.")
        print("="*50)
        return
    
    # Total contacts
    print(f"\nTotal Contacts: {len(contacts)}")
    
    # Contacts by group
    groups = {}
    for name, info in contacts.items():
        group = info['group']
        groups[group] = groups.get(group, 0) + 1
    
    print("\nContacts by Group:")
    for group, count in sorted(groups.items()):
        print(f"  {group}: {count} contact(s)")
    
    # Recently updated
    now = datetime.fromisoformat(datetime.now().isoformat())
    recent_count = 0
    for name, info in contacts.items():
        updated = datetime.fromisoformat(info['updated_at'])
        days_diff = (now - updated).days
        if days_diff <= 7:
            recent_count += 1
    
    print(f"\nRecently Updated (last 7 days): {recent_count}")
    
    # Contacts with email
    email_count = sum(1 for info in contacts.values() if info['email'])
    print(f"Contacts with Email: {email_count}")
    
    print("="*50)

# ==================== MENU SYSTEM ====================

def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("CONTACT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add New Contact")
    print("2. Search Contact")
    print("3. Search by Phone")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. View All Contacts")
    print("7. Export to CSV")
    print("8. View Statistics")
    print("9. Create Backup")
    print("0. Exit")
    print("="*50)

def get_menu_choice():
    """Get user menu choice"""
    while True:
        try:
            choice = input("Enter your choice (0-9): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return choice
            else:
                print("❌ Invalid choice! Please enter 0-9.")
        except KeyboardInterrupt:
            print("\n\n❌ Program interrupted by user.")
            return '0'
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main program loop"""
    contacts = load_from_file()
    
    while True:
        display_menu()
        choice = get_menu_choice()
        
        if choice == '1':
            add_contact(contacts)
        
        elif choice == '2':
            search_contact_menu(contacts)
        
        elif choice == '3':
            print("\n" + "="*50)
            print("SEARCH BY PHONE")
            print("="*50)
            results = search_by_phone(contacts)
            display_search_results(results)
        
        elif choice == '4':
            update_contact(contacts)
        
        elif choice == '5':
            delete_contact(contacts)
        
        elif choice == '6':
            display_all_contacts(contacts)
        
        elif choice == '7':
            export_to_csv(contacts)
        
        elif choice == '8':
            view_statistics(contacts)
        
        elif choice == '9':
            create_backup()
        
        elif choice == '0':
            print("\n" + "="*50)
            print("Thank you for using Contact Management System!")
            print("="*50 + "\n")
            break

if __name__ == "__main__":
    main()
