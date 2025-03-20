import datetime
import json
import os
import random
from log_in import authenticate_user, load_user_data, save_user_data

# Log in user and load personal data
username, nickname = authenticate_user()
user_data = load_user_data(username)

# Show nickname ONCE at the top
print(f"/// Welcome, {nickname}!")

# Function to get valid float input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("/// Bad number. Try again.")

# Ask for protein intake level (0.8 - 1.0)
def get_protein_multiplier():
    while True:
        choice = input("Choose protein intake level: Maximum (1.0), Minimum (0.8), or Medium (0.9): ").strip()
        if choice in ["1.0", "0.8", "0.9"]:
            print(f"/// You chose {choice}x protein intake.")
            return float(choice)
        else:
            print("/// No good. Pick 1.0, 0.9, or 0.8.")

# Function to determine goal
def get_goal_choice():
    gain_typos = {"1", "gain", "bulk", "muscle", "mass", "strong", "buff", "jacked", "gain weight and muscle"}
    lose_typos = {"2", "lose", "cut", "shred", "lean", "burn", "trim", "lose weight and gain muscle"}

    while True:
        choice = input("Pick goal: Gain weight & muscle (1) OR Lose weight & gain muscle (2)\n").strip().lower()

        if choice in gain_typos:
            print("/// You chose to gain weight and muscle.")
            return "gain"
        elif choice in lose_typos:
            print("/// You chose to lose weight and gain muscle.")
            return "lose"
        else:
            print("/// No good. Pick a valid option.")

# Ask for goal if not set
if user_data["goal"] is None:
    goal_type = get_goal_choice()

    if goal_type == "gain":
        weight = get_float_input("Enter your **current** body weight (lbs): ")
    else:
        weight = get_float_input("Enter your **goal** body weight (lbs): ")

    print(f"/// You entered {weight} lbs.")

    protein_multiplier = get_protein_multiplier()
    protein_goal = weight * protein_multiplier

    user_data["goal_type"] = goal_type
    user_data["goal"] = protein_goal
    user_data["protein_intake"] = {}
    save_user_data(username, user_data)
else:
    protein_goal = user_data["goal"]
    print(f"Your daily protein goal: {protein_goal}g")

# Track daily protein intake
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
today = weekdays[datetime.datetime.today().weekday()]

user_data.setdefault("protein_intake", {})

if today in user_data["protein_intake"]:
    print(f"/// Already logged for {today}.")
else:
    protein_eaten = get_float_input(f"Enter protein eaten on {today} (g): ")
    user_data["protein_intake"][today] = protein_eaten
    save_user_data(username, user_data)

    if protein_eaten < protein_goal:
        missing_protein = round(protein_goal - protein_eaten, 2)
        print(f"/// You need to eat {missing_protein}g more protein to hit your goal.")
    elif protein_eaten > protein_goal:
        print("/// Great job! You exceeded your goal.")
    else:
        print("/// Perfect! You hit your goal exactly.")

    print("/// Come back tomorrow to continue tracking!")

# **Ask if the user wants to change their goal**
change_goal = input("Change goal? (yes/no): ").strip().lower()

if change_goal == "yes":
    print("/// Restarting goal setup...")
    goal_type = get_goal_choice()

    if goal_type == "gain":
        weight = get_float_input("Enter your **current** body weight (lbs): ")
    else:
        weight = get_float_input("Enter your **goal** body weight (lbs): ")

    print(f"/// You entered {weight} lbs.")

    protein_multiplier = get_protein_multiplier()
    protein_goal = weight * protein_multiplier

    user_data["goal_type"] = goal_type
    user_data["goal"] = protein_goal
    user_data["protein_intake"] = {}
    save_user_data(username, user_data)

    print(f"/// Your new goal is now to **{goal_type} weight and muscle**.")
    os.system("python3 protein_tracker.py")

else:
    print("/// Goal remains the same. Come back tomorrow!")
