# Number Guessing Game

import random

number = random.randint(1, 20)
guess = 0

while guess != number:
    try:
        guess = int(input("Guess a number between 1 and 20: "))
        if guess < number:
            print("Too low! Try again.")
        elif guess > number:
            print("Too high! Try again.")
        else:
            print("Congratulations! You've guessed the number!")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

#Age Categorizer:

age = int(input("Enter your age: "))

if age < 13:
    print("You are a child.")
elif 13 <= age < 20:
    print("You are a teenager.")    
else:
    print("You are an adult.")


#Shopping List Manager

shopping_list = []
while True:
    action = input("Enter 'add' to add an item, 'remove' to remove an item, 'view' to see the list, or 'exit' to quit: ").strip().lower()
    if action == 'add':
        item = input("Enter the item to add: ").strip()
        shopping_list.append(item)
        print(f"{item} added to the shopping list.")        
    elif action == 'remove':
        item = input("Enter the item to remove: ").strip()
        if item in shopping_list:
            shopping_list.remove(item)
            print(f"{item} removed from the shopping list.")
        else:
            print(f"{item} not found in the shopping list.")
    elif action == 'view':
        print("Current shopping list:")
        for item in shopping_list:
            print(f"- {item}")
    elif action == 'exit':
        print("Exiting the shopping list manager.")
        break
    else:
        print("Invalid action. Please try again.")

# Multiplication Table Generator

num = int(input("Enter a number to generate its multiplication table: "))
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

#Simple Login System
username = "admin"
password = "password"

input_username = input("Enter your username: ")
input_password = input("Enter your password: ")

if input_username == username and input_password == password:
    print("Login successful!")
else:
    print("Invalid username or password.")

#List Operations Practice

nums = [1, 2, 3, 4, 5]

nums.append(6)  # Add an element
nums.remove(2)  # Remove an element
nums.insert(2, 10)  # Insert an element at a specific index
print("List after operations:",nums)  # Print the list

nums.sort()  # Sort the list
print("Sorted list:", nums)  # Print the sorted list    
nums.reverse()  # Reverse the list
print("Reversed list:", nums)  # Print the reversed list

#Error Handling for User Input

try:
    value = int(input("Enter a number: "))
    print(f"You entered: {value}")
except ValueError:
    print("Invalid input. Please enter a valid integer.")