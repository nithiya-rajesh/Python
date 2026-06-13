"""
Project: Student Grade Calculator
Author: Nithiya Rajendran
Description: A formatted grading system with input validation and statistics.
"""

def get_grade_info(avg):
    if avg >= 90: return 'A', "Excellent work! Keep it up."
    if avg >= 80: return 'B', "Very Good! You're doing well."
    if avg >= 70: return 'C', "Good effort. Room for growth."
    if avg >= 60: return 'D', "Pass, but needs improvement."
    return 'F', "Failed. Please seek assistance."

def get_valid_marks(subject):
    while True:
        try:
            marks = float(input(f"{subject}: "))
            if 0 <= marks <= 100:
                return marks
            print("Invalid input. Please enter marks between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def main():
    print("=" * 50)
    print("      STUDENT GRADE CALCULATOR")
    print("=" * 50)

    while True:
        try:
            num_students = int(input("\nEnter number of students: "))
            if num_students > 0: break
            print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    students = []

    for i in range(num_students):
        print(f"\n=== STUDENT {i+1} ===")
        name = input("Student name: ")
        print("Enter marks (0-100):")
        m1 = get_valid_marks("Math")
        m2 = get_valid_marks("Science")
        m3 = get_valid_marks("English")
        
        avg = (m1 + m2 + m3) / 3
        grade, comment = get_grade_info(avg)
        students.append({'name': name, 'avg': avg, 'grade': grade, 'comment': comment})

    print("\n" + "=" * 50)
    print("            RESULTS SUMMARY")
    print("=" * 50)
    print(f"{'Name':<20} | {'Avg':<4} | {'Grade':<5} | {'Comment'}")
    print("-" * 60)
    
    for s in students:
        print(f"{s['name']:<20} | {s['avg']:<4.1f} | {s['grade']:<5} | {s['comment']}")

    # Statistics Calculation
    avgs = [s['avg'] for s in students]
    highest = max(students, key=lambda x: x['avg'])
    lowest = min(students, key=lambda x: x['avg'])

    print("\n" + "=" * 50)
    print("          CLASS STATISTICS")
    print("=" * 50)
    print(f"Total Students: {len(students)}")
    print(f"Class Average: {sum(avgs)/len(avgs):.1f}")
    print(f"Highest Average: {highest['avg']:.1f} ({highest['name']})")
    print(f"Lowest Average: {lowest['avg']:.1f} ({lowest['name']})")
    print("\n" + "=" * 50)
    print("Thank you for using the Grade Calculator!")

if __name__ == "__main__":
    main()