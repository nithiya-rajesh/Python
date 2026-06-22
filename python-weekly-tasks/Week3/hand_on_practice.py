# 1. Common Calculations (Area, Volume, Conversions)
def area_rectangle(length, width):
    return length * width

def volume_cube(side):
    return side ** 3

def km_to_miles(km):
    return km * 0.621371


# 2. Currency Converter
def usd_to_inr(usd):
    return usd * 83.5

def inr_to_usd(inr):
    return inr / 83.5

def usd_to_eur(usd):
    return usd * 0.92


# 3. Student Database (Dictionaries)
students = {
    "Alice": {"age": 20, "subjects": ["Math", "CS"]},
    "Bob": {"age": 22, "subjects": ["History", "Economics"]}
}

def add_student(name, age, subjects):
    students[name] = {"age": age, "subjects": subjects}

def get_student(name):
    return students.get(name, "Student not found")


# 4. Text Analyzer
def text_analyzer(text):
    words = text.split()
    characters = len(text)
    vowels = sum(1 for ch in text.lower() if ch in "aeiou")
    return {"words": len(words), "characters": characters, "vowels": vowels}


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


# 6. String Methods Practice
def string_methods_demo(text):
    return {
        "upper": text.upper(),
        "lower": text.lower(),
        "strip": text.strip(),
        "split": text.split()
    }


# 7. Functions with Different Parameter Types
def greet(name, msg="Hello"):
    return f"{msg}, {name}!"

def add_numbers(*args):
    return sum(args)

def student_info(**kwargs):
    return kwargs


# --- Demo Calls ---
if __name__ == "__main__":
    print(area_rectangle(5, 3))          # 15
    print(volume_cube(4))                # 64
    print(km_to_miles(10))               # 6.21371

    print(usd_to_inr(10))                # 835 INR
    print(inr_to_usd(835))               # 10 USD
    print(usd_to_eur(10))                # 9.2 EUR

    add_student("Charlie", 21, ["Physics", "Chemistry"])
    print(get_student("Charlie"))

    print(text_analyzer("Hello World"))

    account = BankAccount("Rajesh", 1000)
    print(account.deposit(500))
    print(account.withdraw(300))

    print(string_methods_demo("   Python is Fun!   "))

    print(greet("Rajesh"))
    print(add_numbers(1, 2, 3, 4))
    print(student_info(name="Alice", age=20, grade="A"))
