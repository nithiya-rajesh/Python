# Contact Management System

A comprehensive Command-Line Interface (CLI) application built with Python to manage personal contacts efficiently. This project demonstrates proficiency in data structures (dictionaries), file handling, and modular programming.

## 🚀 Features
- **CRUD Operations**: Create, Read, Update, and Delete contacts.
- **Data Persistence**: Automatically saves and loads data using `contacts_data.json`.
- **Search**: Partial name matching functionality.
- **Validation**: Ensures phone numbers and emails follow proper formats.
- **Organization**: Categorize contacts into groups (Friends, Work, Family, etc.).
- **Statistics**: View analytics about your contact list.
- **Export**: Ability to export contact data to CSV format.

## 🛠️ Technical Stack
- **Language**: Python 3.x
- **Libraries Used**: 
  - `json`: For data storage.
  - `re`: For input validation (Regex).
  - `datetime`: For tracking contact creation/updates.
  - `csv`: For data export functionality.
## 📝 Lessons Learned
- **Functions**: Developed modular code to handle specific tasks (adding, deleting, validating).
- **Dictionaries**: Used nested dictionaries for organized data retrieval.
- **File I/O**: Managed external file persistence to ensure data isn't lost after closing the program.
- **Defensive Programming**: Learned how to anticipate user errors by implementing robust validation loops, ensuring the program remains stable even when receiving unexpected input.
- **Error Handling**: Implemented safeguards to handle file operations and edge cases gracefully.

## 📂 Project Structure
```text
week3-contact-manager/
├── contacts_manager.py     # Main application logic
├── contacts_data.json      # JSON storage file (auto-generated)
├── test_contacts.py        # Unit tests
├── README.md               # Project documentation
├── .gitignore              # Ignore unnecessary files
└── requirements.txt        # Dependency list

```

## 💻 How to Run
1. Clone the repository or download the files.
2. Navigate to the directory:
```
cd week3-contact-manager
```
3. Run the application:
```
python contacts_manager.py
```
4. Run tests:
```
python test_contacts.py
```
5. Run unit tests:
```
python -m unittest test_contacts.py
```
## 📝 Lessons Learned
1. Functions: Developed modular code to handle specific tasks (adding, deleting, validating).
2. Dictionaries: Used nested dictionaries for organized data retrieval.
3. File I/O: Managed external file persistence to ensure data isn't lost after closing the program.
4. Error Handling: Implemented safeguards to handle user input errors gracefully.

## 📊 Sample Output
```
--- Contact Manager ---
1. Add Contact
2. Search Contact by Name
3. Search Contact by Phone
4. Update Contact
5. Delete Contact
6. Display All Contacts
7. Export to CSV
8. Show Statistics
9. Save & Exit
Enter choice: 1

--- ADD NEW CONTACT ---
Enter contact name: John
Enter phone number: 789456123
Enter email (optional, press Enter to skip): john@1878.com
Enter address (optional): 15th cross, raj street
Enter group (Friends/Work/Family/Other): Friends
✅ Contact 'John' added successfully!
```
## 👨‍💻 Author
Nithya Rajendran"# week3-contact management system"
