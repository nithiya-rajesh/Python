# 🎓 Student Grade Calculator
**Week 2 Project – Control Flow & Data Structures**


## 📖 Project Description
A comprehensive grade calculator that processes multiple students' marks, calculates grades with personalized comments, and provides class statistics.  
This project demonstrates mastery of **conditionals, lists, loops, functions, and error handling** in Python.


## 🚀 Features
- Processes multiple students with validated input
- Calculates grades based on a custom grading system
- Provides personalized comments for each student
- Computes class statistics (average, highest, lowest)
- Displays results in a formatted table
- Input validation for all user inputs
- Error handling for edge cases
- Search functionality for specific students *(optional extension)*
- Save results to a file *(optional extension)*

---

## 🧠 What I Learned
- **Conditional Logic**: Using `if/elif/else` for decision making  
- **Lists**: Storing and manipulating collections of data  
- **Loops**: Using `for` and `while` loops for repetition  
- **Error Handling**: Using `try/except` to handle invalid inputs  
- **Functions**: Organizing code into reusable blocks  

---

## 🛠️ How to Run
```bash
# Navigate to project folder
cd week2-grade-calculator
```
```bash
# Run the program
python grade_calculator.py
```
```bash
# Sample test with provided data
python grade_calculator.py < test_students.txt
```

## 📊 Grading System
A: 90–100 → Excellent!

B: 80–89 → Very Good!

C: 70–79 → Good

D: 60–69 → Needs Improvement

F: 0–59 → Failed – Please seek help

## 🖥️ Sample Output

```text
==================================================
      STUDENT GRADE CALCULATOR
==================================================

Enter number of students: 2

=== STUDENT 1 ===
Student name: John Smith
Enter marks (0-100):
Math: 85
Science: 92
English: 88

=== STUDENT 2 ===
Student name: Sarah Johnson
Enter marks (0-100):
Math: 78
Science: 81
English: 85

==================================================
            RESULTS SUMMARY
==================================================
Name                 |  Avg | Grade | Comment
------------------------------------------------------------
John Smith           |  88.3 |   B   | Very Good! You're doing well.
Sarah Johnson        |  81.3 |   B   | Very Good! You're doing well.

==================================================
          CLASS STATISTICS
==================================================
Total Students: 2
Class Average: 84.8
Highest Average: 88.3 (John Smith)
Lowest Average: 81.3 (Sarah Johnson)

==================================================
Thank you for using the Grade Calculator!
==================================================
```

## 📂 Repository Structure
```bash
week2-grade-calculator/
│── grade_calculator.py      # Main program
│── test_students.txt        # Sample input data
│── results_sample.txt       # Example output
│── README.md                # Documentation
└── .gitignore               # Ignore unnecessary files
```

## ✅ Quality Standards Checklist
[x] Handles invalid input gracefully

[x] Formats results in a clear table

[x] Calculates multiple statistics

[x] Provides personalized feedback

[x] Includes documentation and sample output

## 👨‍💻 Author
Nithya Rajendran"# week2-grade-calculator" 
