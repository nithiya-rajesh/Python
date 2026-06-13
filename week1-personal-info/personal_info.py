# personal_info.py
# Author: Nithya
# Project: Personal Information Manager
# Description: A simple Python program that stores and displays personal information.

# Step 2: Store static information
# These are fixed values (you can change them if you like)
name = "Nithya"          # string
age = 25                 # integer
city = "Bangalore"       # string
hobby = "Coding"         # string

# Step 3: Get user input
# Ask for favorite food and color
favorite_food = input("Please enter your favorite food: ").strip()
favorite_color = input("Please enter your favorite color: ").strip()

# Basic validation: check if input is empty
if not favorite_food:
    favorite_food = "Not provided"
if not favorite_color:
    favorite_color = "Not provided"

# Step 6: Enhancements
print("\n👋 Welcome to the Personal Information Manager!\n")

# Calculate age in months
age_in_months = age * 12

# Step 4: Display information
print("========== Personal Information ==========")
print(f"Name: {name.title()}")   # .title() formats the string
print(f"Age: {age} years ({age_in_months} months)")
print(f"City: {city.title()}")
print(f"Hobby: {hobby.capitalize()}")
print("------------------------------------------")
print(f"Favorite Food: {favorite_food.title()}")
print(f"Favorite Color: {favorite_color.title()}")
print("==========================================")

# Step 6: Goodbye message
print("\nThank you for using the Personal Information Manager. Goodbye! 👋")
