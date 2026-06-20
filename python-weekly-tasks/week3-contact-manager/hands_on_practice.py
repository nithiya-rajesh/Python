#1. Common Calculations (Area, Volume, Conversions)
def area_rectangle(length, width):
    return length * width
def volume_cube(side):
    return side ** 3    
def km_to_miles(km):
    return km * 0.621371    

print("Area of rectangle (5, 10):", area_rectangle(5, 10))
print("Volume of cube (3):", volume_cube(3))    
print("10 km in miles:", km_to_miles(10))

# 2. Currency Converter

def usd_to_inr(usd):
    return usd * 74.85

def inr_to_usd(inr):
    return inr / 74.85  

def usd_to_eur(usd):
    return usd * 0.85

print("100 USD in INR:", usd_to_inr(100))
print("100 INR in USD:", inr_to_usd(100))
print("100 USD in EUR:", usd_to_eur(100))

#3. Student Database (Dictionaries)

students = {
    "Alice": {"age": 20, "subjects": ["Math", "CS"]},
    "Bob": {"age": 22, "subjects": ["History", "Economics"]}
}

def add_student(name, age, subjects):
    students[name] = {"age": age, "subjects": subjects}

def get_student(name):
    return students.get(name, "Student not found")

# Example usage
add_student("Charlie", 21, ["Physics", "Chemistry"])
print(get_student("Charlie"))

# 4. Text Analyzer

def text_analyzer(text):
    words = text.split()
    characters = len(text)
    vowels = sum (1 for char in text.lower() if char in 'aeiou')
    return {"words": len(words), "characters": characters, "vowels": vowels}        
print(text_analyzer("Hello World! This is a test."))

# 5. Bank Account System

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return f"Deposited {amount}. New balance: {self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        return f"Withdrew {amount}. New balance: {self.balance}"

# Example usage
account = BankAccount("Rajesh", 1000)
print(account.deposit(500))
print(account.withdraw(300))


#6. String Methods Practice

text = "   Python is Fun!   "

print(text.upper())   # "   PYTHON IS FUN!   "
print(text.lower())   # "   python is fun!   "
print(text.strip())   # "Python is Fun!"
print(text.split())   # ['Python', 'is', 'Fun!']

# 7. Functions with Different Parameter Types

def greet(name, msg="Hello"):
    return f"{msg}, {name}!"

def add_numbers(*args):
    return sum(args)

def student_info(**kwargs):
    return kwargs

# Example usage
print(greet("Rajesh"))
print(add_numbers(1, 2, 3, 4))
print(student_info(name="Alice", age=20, grade="A"))
