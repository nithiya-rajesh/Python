# Contact Management System - Complete Implementation
# Week 3 Project - Functions & Dictionaries
# All 7 Steps Integrated

import json
import re
from datetime import datetime, timedelta
import csv
import os

# ============================================================
# STEP 1: PROJECT STRUCTURE - Global Setup
# ============================================================

# Global dictionary to store contacts
contacts = {}
DATA_FILE = 'contacts_data.json'

# ============================================================
# STEP 2: CORE DATA STRUCTURE - Validation Functions
# ============================================================

def validate_phone(phone):
    """
    Validate phone number format
    Accepts 10-15 digits in any format
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        tuple: (is_valid: bool, cleaned_phone: str or None)
    """
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None


def validate_email(email):
    """
    Validate email format using regex
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_name(name):
    """
    Validate contact name
    Must be non-empty and contain at least one letter
    
    Args:
        name (str): Name to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    return bool(name.strip()) and any(char.isalpha() for char in name)


def create_contact(name, phone, email="", address="", group="Other"):
    """
    Create a contact dictionary with all required information
    
    Args:
        name (str): Contact name
        phone (str): Phone number (cleaned)
        email (str): Email address (optional)
        address (str): Physical address (optional)
        group (str): Contact group/category
    
    Returns:
        dict: Contact information dictionary
    """
    return {
        'phone': phone,
        'email': email if email else None,
        'address': address if address else None,
        'group': group,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }


def format_phone(phone):
    """
    Format phone number for display
    
    Args:
        phone (str): Cleaned phone number
    
    Returns:
        str: Formatted phone number
    """
    if len(phone) == 10:
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    elif len(phone) == 11:
        return f"+{phone[0]} ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
    else:
        return phone


# ============================================================
# STEP 3: CRUD FUNCTIONS
# ============================================================

def add_contact():
    """Create a new contact with validation"""
    global contacts
    
    print("\n--- ADD NEW CONTACT ---")
    
    # Get and validate contact name
    while True:
        name = input("Enter contact name: ").strip()
        
        if not validate_name(name):
            print("❌ Name cannot be empty and must contain letters!")
            continue
        
        if name in contacts:
            print(f"⚠️  Contact '{name}' already exists!")
            choice = input("Do you want to update instead? (y/n): ").lower()
            if choice == 'y':
                update_contact_by_name(name)
            return
        
        break
    
    # Get and validate phone number
    while True:
        phone = input("Enter phone number: ").strip()
        is_valid, cleaned_phone = validate_phone(phone)
        
        if is_valid:
            break
        
        print("❌ Invalid phone number! Please enter 10-15 digits.")
    
    # Get and validate email (optional)
    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        
        if not email:
            email = ""
            break
        
        if validate_email(email):
            break
        
        print("❌ Invalid email format! Example: john@example.com")
    
    # Get address (optional)
    address = input("Enter address (optional): ").strip()
    
    # Get group
    print("Contact groups: Friends, Work, Family, Other")
    group = input("Enter group (default: Other): ").strip() or "Other"
    
    # Create and store contact
    contacts[name] = create_contact(
        name=name,
        phone=cleaned_phone,
        email=email,
        address=address,
        group=group
    )
    
    save_to_file()
    print(f"✅ Contact '{name}' added successfully!")


def search_contact():
    """Search for contacts by partial name match"""
    print("\n--- SEARCH CONTACTS ---")
    search_term = input("Enter name to search: ").strip()
    
    if not search_term:
        print("❌ Search term cannot be empty!")
        return
    
    results = search_contacts(search_term)
    display_search_results(results)


def search_contacts(search_term):
    """
    Helper function: Search contacts by name (partial match)
    Case-insensitive search
    
    Args:
        search_term (str): Search string
    
    Returns:
        dict: Dictionary of matching contacts
    """
    search_term_lower = search_term.lower()
    results = {}
    
    for name, info in contacts.items():
        if search_term_lower in name.lower():
            results[name] = info
    
    return results


def display_search_results(results):
    """Display search results in formatted way"""
    if not results:
        print("❌ No contacts found.")
        return
    
    print(f"\n✅ Found {len(results)} contact(s):")
    print("-" * 60)
    
    for i, (name, info) in enumerate(results.items(), 1):
        print(f"{i}. {name}")
        print(f"   📞 Phone: {info['phone']}")
        if info['email']:
            print(f"   📧 Email: {info['email']}")
        if info['address']:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}")
        print()


def update_contact():
    """Update an existing contact"""
    print("\n--- UPDATE CONTACT ---")
    
    search_term = input("Enter name to search for update: ").strip()
    results = search_contacts(search_term)
    
    if not results:
        print("❌ No contacts found.")
        return
    
    if len(results) == 1:
        name = list(results.keys())[0]
    else:
        print("\nMultiple matches found:")
        for i, name in enumerate(results.keys(), 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input("Select contact number: "))
            names = list(results.keys())
            if 1 <= choice <= len(names):
                name = names[choice - 1]
            else:
                print("❌ Invalid choice!")
                return
        except ValueError:
            print("❌ Invalid input!")
            return
    
    update_contact_by_name(name)


def update_contact_by_name(name):
    """
    Helper function: Update a specific contact by name
    
    Args:
        name (str): Contact name to update
    """
    if name not in contacts:
        print(f"❌ Contact '{name}' not found!")
        return
    
    contact = contacts[name]
    
    print(f"\n--- UPDATING: {name} ---")
    print("Press Enter to skip any field (keep existing value)")
    print()
    
    # Update phone
    while True:
        phone_input = input(f"Phone ({contact['phone']}): ").strip()
        if not phone_input:
            break
        is_valid, cleaned = validate_phone(phone_input)
        if is_valid:
            contact['phone'] = cleaned
            break
        print("❌ Invalid phone number!")
    
    # Update email
    while True:
        email_input = input(f"Email ({contact['email'] or 'Not set'}): ").strip()
        if not email_input:
            break
        if validate_email(email_input):
            contact['email'] = email_input
            break
        print("❌ Invalid email format!")
    
    # Update address
    address_input = input(f"Address ({contact['address'] or 'Not set'}): ").strip()
    if address_input:
        contact['address'] = address_input
    
    # Update group
    group_input = input(f"Group ({contact['group']}): ").strip()
    if group_input:
        contact['group'] = group_input
    
    # Update timestamp
    contact['updated_at'] = datetime.now().isoformat()
    
    save_to_file()
    print(f"✅ Contact '{name}' updated successfully!")


def delete_contact():
    """Delete a contact with confirmation"""
    print("\n--- DELETE CONTACT ---")
    
    search_term = input("Enter name to search for deletion: ").strip()
    results = search_contacts(search_term)
    
    if not results:
        print("❌ No contacts found.")
        return
    
    if len(results) == 1:
        name = list(results.keys())[0]
    else:
        print("\nMultiple matches found:")
        for i, name in enumerate(results.keys(), 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input("Select contact number: "))
            names = list(results.keys())
            if 1 <= choice <= len(names):
                name = names[choice - 1]
            else:
                print("❌ Invalid choice!")
                return
        except ValueError:
            print("❌ Invalid input!")
            return
    
    # Show contact details before deletion
    contact = contacts[name]
    print(f"\n📋 Contact to delete:")
    print(f"   Name: {name}")
    print(f"   Phone: {contact['phone']}")
    print(f"   Email: {contact['email']}")
    print()
    
    # Confirm deletion
    confirm = input(f"⚠️  Are you sure you want to delete '{name}'? (y/n): ").lower()
    
    if confirm == 'y':
        del contacts[name]
        save_to_file()
        print(f"✅ Contact '{name}' deleted successfully!")
    else:
        print("❌ Deletion cancelled.")


def display_all():
    """Display all contacts in formatted way"""
    if not contacts:
        print("\n❌ No contacts found. Add some contacts to get started!")
        return
    
    print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
    print("=" * 60)
    
    for i, (name, info) in enumerate(contacts.items(), 1):
        print(f"{i}. {name}")
        print(f"   📞 Phone: {info['phone']}")
        if info['email']:
            print(f"   📧 Email: {info['email']}")
        if info['address']:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}")
        print("-" * 60)


# ============================================================
# STEP 4: FILE OPERATIONS
# ============================================================

def save_to_file():
    """
    Save contacts to JSON file
    Creates or overwrites contacts_data.json
    """
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(contacts, f, indent=4)
        return True
    except Exception as e:
        print(f"❌ Error saving to file: {str(e)}")
        return False


def load_from_file():
    """
    Load contacts from JSON file
    Runs on startup to restore previous data
    """
    global contacts
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                contacts = json.load(f)
                print(f"✅ Loaded {len(contacts)} contacts from file.")
        else:
            print("✅ No existing contacts file found. Starting fresh.")
            contacts = {}
    except Exception as e:
        print(f"❌ Error loading from file: {str(e)}")
        contacts = {}


def backup_contacts():
    """
    Create a backup of contacts data
    Saves as contacts_backup_[timestamp].json
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"contacts_backup_{timestamp}.json"
        
        with open(backup_file, 'w') as f:
            json.dump(contacts, f, indent=4)
        
        print(f"✅ Backup created: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating backup: {str(e)}")
        return False


# ============================================================
# STEP 5: USER INTERFACE
# ============================================================

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 30)
    print("          MAIN MENU")
    print("=" * 30)
    print("1. Add New Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. View All Contacts")
    print("6. Export to CSV")
    print("7. View Statistics")
    print("8. View by Group")
    print("9. Backup Data")
    print("10. Exit")
    print("=" * 30)


def main():
    """Main program entry point"""
    print("=" * 50)
    print("      CONTACT MANAGEMENT SYSTEM")
    print("=" * 50)
    
    # Load existing contacts from file
    load_from_file()
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == '1':
            add_contact()
        elif choice == '2':
            search_contact()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            display_all()
        elif choice == '6':
            export_to_csv()
        elif choice == '7':
            display_statistics()
        elif choice == '8':
            display_by_group()
        elif choice == '9':
            backup_contacts()
        elif choice == '10':
            save_to_file()
            print("✅ Contacts saved to contacts_data.json")
            print("\n" + "=" * 50)
            print("Thank you for using Contact Management System!")
            print("=" * 50)
            break
        else:
            print("❌ Invalid choice! Please try again.")


# ============================================================
# STEP 6: ADVANCED FEATURES
# ============================================================

def export_to_csv():
    """
    Export all contacts to CSV file
    Creates contacts_export.csv
    """
    if not contacts:
        print("❌ No contacts to export!")
        return
    
    try:
        filename = "contacts_export.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Phone', 'Email', 'Address', 'Group', 'Created', 'Updated']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
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
        print(f"❌ Error exporting to CSV: {str(e)}")


def display_statistics():
    """
    Display contact statistics
    Shows total count, breakdown by group, and recent updates
    """
    if not contacts:
        print("\n❌ No contacts to display statistics for!")
        return
    
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {len(contacts)}")
    print()
    
    # Count by group
    groups = {}
    for name, info in contacts.items():
        group = info['group']
        groups[group] = groups.get(group, 0) + 1
    
    print("Contacts by Group:")
    for group, count in sorted(groups.items()):
        print(f"  {group}: {count} contact(s)")
    print()
    
    # Recently updated (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_count = 0
    recent_contacts = []
    
    for name, info in contacts.items():
        updated = datetime.fromisoformat(info['updated_at'])
        if updated > seven_days_ago:
            recent_count += 1
            recent_contacts.append(name)
    
    print(f"Recently Updated (last 7 days): {recent_count}")
    if recent_contacts:
        for contact in recent_contacts:
            print(f"  - {contact}")
    print()


def display_by_group():
    """
    Display all contacts organized by group
    """
    if not contacts:
        print("\n❌ No contacts to display!")
        return
    
    # Group contacts
    groups = {}
    for name, info in contacts.items():
        group = info['group']
        if group not in groups:
            groups[group] = []
        groups[group].append((name, info))
    
    print("\n--- CONTACTS BY GROUP ---")
    print("=" * 60)
    
    for group in sorted(groups.keys()):
        print(f"\n👥 {group} ({len(groups[group])} contact(s))")
        print("-" * 60)
        
        for name, info in groups[group]:
            print(f"  • {name}")
            print(f"    📞 {info['phone']}")
            if info['email']:
                print(f"    📧 {info['email']}")
            if info['address']:
                print(f"    📍 {info['address']}")


def import_from_csv(filename):
    """
    Import contacts from CSV file
    CSV should have columns: Name, Phone, Email, Address, Group
    
    Args:
        filename (str): CSV file path
    """
    global contacts
    
    try:
        imported_count = 0
        errors = []
        
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                name = row.get('Name', '').strip()
                phone = row.get('Phone', '').strip()
                email = row.get('Email', '').strip()
                address = row.get('Address', '').strip()
                group = row.get('Group', 'Other').strip()
                
                # Validate
                if not validate_name(name):
                    errors.append(f"Invalid name: {name}")
                    continue
                
                is_valid, cleaned = validate_phone(phone)
                if not is_valid:
                    errors.append(f"Invalid phone for {name}: {phone}")
                    continue
                
                if email and not validate_email(email):
                    errors.append(f"Invalid email for {name}: {email}")
                    continue
                
                # Add contact
                contacts[name] = create_contact(name, cleaned, email, address, group)
                imported_count += 1
        
        save_to_file()
        print(f"✅ Imported {imported_count} contacts from {filename}")
        
        if errors:
            print(f"\n⚠️  {len(errors)} errors during import:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
    
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
    except Exception as e:
        print(f"❌ Error importing contacts: {str(e)}")


# ============================================================
# STEP 7: TESTING & VALIDATION
# ============================================================

def validate_contacts_data():
    """
    Validate all stored contacts data
    Checks for data integrity
    """
    print("\n--- DATA VALIDATION ---")
    errors = []
    warnings = []
    
    for name, info in contacts.items():
        # Check required fields
        if not info.get('phone'):
            errors.append(f"{name}: Missing phone number")
        
        if not info.get('created_at'):
            warnings.append(f"{name}: Missing created_at timestamp")
        
        if not info.get('updated_at'):
            warnings.append(f"{name}: Missing updated_at timestamp")
        
        # Validate phone format
        if info.get('phone') and len(info['phone']) < 10:
            errors.append(f"{name}: Invalid phone format")
        
        # Validate email if present
        if info.get('email') and not validate_email(info['email']):
            errors.append(f"{name}: Invalid email format")
    
    print(f"Total contacts checked: {len(contacts)}")
    
    if errors:
        print(f"\n❌ Errors found: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ No errors found!")
    
    if warnings:
        print(f"\n⚠️  Warnings: {len(warnings)}")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("✅ No warnings!")
    
    return len(errors) == 0


def test_system():
    """
    Run basic system tests
    Validates that all functions work correctly
    """
    print("\n--- SYSTEM TEST ---")
    print("Testing core functions...")
    
    # Test validation functions
    print("\n1. Testing validation functions...")
    
    # Phone validation
    is_valid, cleaned = validate_phone("+1 (234) 567-8900")
    assert is_valid and cleaned == "12345678900", "Phone validation failed"
    print("   ✅ Phone validation works")
    
    # Email validation
    assert validate_email("test@example.com"), "Email validation failed"
    assert not validate_email("invalid.email"), "Email validation failed"
    print("   ✅ Email validation works")
    
    # Name validation
    assert validate_name("John Doe"), "Name validation failed"
    assert not validate_name(""), "Name validation failed"
    print("   ✅ Name validation works")
    
    # Test contact creation
    print("\n2. Testing contact creation...")
    contact = create_contact("Test User", "1234567890", "test@example.com")
    assert contact['phone'] == "1234567890", "Contact creation failed"
    assert 'created_at' in contact, "Contact creation failed"
    print("   ✅ Contact creation works")
    
    # Test search
    print("\n3. Testing search function...")
    global contacts
    test_contacts_backup = contacts.copy()
    contacts = {"John Doe": create_contact("John Doe", "1234567890")}
    
    results = search_contacts("john")
    assert len(results) == 1, "Search failed"
    print("   ✅ Search function works")
    
    # Restore contacts
    contacts = test_contacts_backup
    
    print("\n✅ All tests passed!")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    main()
