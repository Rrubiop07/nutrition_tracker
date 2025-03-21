import datetime
import json
import os

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("/// Bad number. Try again.")

def load_data():
    try:
        with open("protein_tracker.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("protein_tracker.json", "w") as file:
        json.dump(data, file)

#  Recommendation to start on Monday
print("/// Recommended to start on Monday for best tracking.")

data = load_data()

#  Ask for goal if not set
if "goal" not in data:
    print("Pick goal: Gain weight & muscle (1) OR Lose weight & muscle (2)")
    choice = input("Enter 1 or 2: ")
    while choice not in ["1", "2"]:
        print("/// No good. Pick 1 or 2.")
        choice = input("Enter 1 or 2: ")

    if choice == "1":
        weight = get_float_input("Enter current body weight (lbs): ")
        protein_goal = weight * 0.5
        data["goal_type"] = "gain"
    else:
        weight = get_float_input("Enter goal body weight (lbs): ")
        protein_goal = weight * 0.5
        data["goal_type"] = "lose"

    data["goal"] = protein_goal
    data["protein_intake"] = {}
    save_data(data)
else:
    protein_goal = data["goal"]
    print(f"Your daily protein goal: {protein_goal}g")

# Track daily intake
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
today = weekdays[datetime.datetime.today().weekday()]

data.setdefault("protein_intake", {})

if today in data["protein_intake"]:
    print(f"/// Already logged for {today}.")
else:
    protein_eaten = get_float_input(f"Enter protein eaten on {today} (g): ")
    data["protein_intake"][today] = protein_eaten
    save_data(data)

    if protein_eaten > protein_goal:
        print("Amazing work!!!")
    elif protein_eaten == protein_goal:
        print("Wow on point!!")
    else:
        print("You gonna have to work on your intake.")

# Weekly summary on Sunday
if today == "Sunday":
    print("/// Running weekly summary...")
    os.system("python week_summary.py")  # Runs the week summary script

# Ask if user wants to reset goal
change_goal = input("Change goal? (yes/no): ").lower()
if change_goal == "yes":
    print("Restarting goal setup...")
    data.pop("goal", None)
    data.pop("goal_type", None)
    data.pop("protein_intake", None)
    save_data(data)
    os.system("python protein_tracker.py")  # Restart program
else:
    print("/// Goal remains same. Come back tomorrow!")