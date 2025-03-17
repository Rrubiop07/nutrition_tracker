import datetime
import json
import os
import difflib
import random

# Function to get a valid float input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("/// Bad number. Try again.")

# Function to load saved data
def load_data():
    try:
        with open("protein_tracker.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save data
def save_data(data):
    with open("protein_tracker.json", "w") as file:
        json.dump(data, file)

print("/// Recommended to start on Monday for best tracking.")

# Load saved data
data = load_data()

import difflib
import random

# Picks goal based on what user types
def get_goal_choice():
    # Words for gain and lose
    gain_base = [
        "gain", "bulk", "muscle", "bigger", "mass", "increase", "strong", "swole",
        "buff", "jacked", "heavy", "size", "grow", "build", "gains", "protein", "weight"
    ]
    
    lose_base = [
        "lose", "cut", "shred", "lean", "burn", "trim", "skinny", "drop",
        "light", "fit", "deficit", "reduce", "tone", "burn fat", "shrink"
    ]

    # Auto generates typos and common mistakes
    def generate_typos(words):
        typos = set()
        for word in words:
            typos.update([
                word, word + "s", word + "z", word + "zz", word[:-1], word + word[-1], 
                word.replace("c", "k"), word.replace("i", "y"), word.replace("y", "i"),
                word.replace("s", "z"), word.replace("m", "nn"), word.replace("g", "q"),
                word.replace("e", "a"), word.replace("o", "u"), word.replace("a", "o"),
                word.replace("t", "d"), word.replace("d", "t"), word.replace("l", "r"),
                word.replace("r", "l"), word.replace("n", "m"), word.replace("m", "n"),
                word.replace("w", "vv"), word.replace("v", "w"), word.replace("u", "o"),
                word.replace("f", "ph"), word.replace("ph", "f"), word.replace("k", "c"),
                word[::-1], word + random.choice(["x", "v", "m", "p"])  # Adds random endings
            ])
        return typos

    # Makes a big list of typos and other ways people say gain/lose
    gain_typos = generate_typos(gain_base)
    lose_typos = generate_typos(lose_base)

    # Add number choices (1 or 2) and phrases
    gain_typos.update(["1", "one", "first", "1st", "option one", "numero uno", "gain weight", "get fat", "get big"])
    lose_typos.update(["2", "two", "second", "2nd", "option two", "numero dos", "lose weight", "get skinny", "drop fat"])

    # Full sentences people might use for gaining
    gain_typos.update([
        "i want to gain", "i need to bulk", "make me bigger", "help me gain muscle",
        "let's get swole", "protein mode", "i wanna grow", "bigger frame",
        "lift heavy eat big", "bulking phase", "i wanna be jacked", "bulk szn",
        "i need mass", "more protein please", "i need more size", "make me strong",
        "i need more muscle", "swole gang", "gains gang", "time to gain", "let’s build muscle",
        "getting huge", "more size needed", "let’s pack on weight", "power mode"
    ])

    # Full sentences people might use for losing
    lose_typos.update([
        "i want to lose", "i need to cut", "help me lose weight", "trim me down",
        "lean mode", "i wanna be shredded", "cutting phase", "drop the weight",
        "burn mode", "get me toned", "make me fit", "i need to shred", "summer cut",
        "i wanna get lean", "i need to be lighter", "get me slim", "fat loss mode",
        "drop some pounds", "make me aesthetic", "cutting szn", "lean gains",
        "time to shred", "losing size", "cut mode activated", "abs mode", "i wanna be ripped"
    ])

    # Checks if any words in what they type match gain/lose
    def extract_goal_from_sentence(sentence):
        words = sentence.lower().split()
        
        for word in words:
            if word in gain_typos:
                return "gain"
            if word in lose_typos:
                return "lose"

        # If no exact match, tries to find the closest word
        closest_match = difflib.get_close_matches(sentence.lower(), gain_typos | lose_typos, n=1, cutoff=0.6)
        if closest_match:
            if closest_match[0] in gain_typos:
                return "gain"
            elif closest_match[0] in lose_typos:
                return "lose"

        return None  # If nothing matches, return None

    # Keeps asking until they type something good
    while True:
        choice = input("Pick goal: Gain weight & muscle (1) OR Lose weight & muscle (2)\n").strip().lower()

        result = extract_goal_from_sentence(choice)
        if result:
            return result
        else:
            print("/// No good. Pick a valid option.")


# Ask for goal if not set
if "goal" not in data:
    goal_type = get_goal_choice()  # Get goal choice using the function

    if goal_type == "gain":
        weight = get_float_input("Enter current body weight (lbs): ")
    else:
        weight = get_float_input("Enter goal body weight (lbs): ")

    protein_goal = weight * 0.5
    data["goal_type"] = goal_type
    data["goal"] = protein_goal
    data["protein_intake"] = {}
    save_data(data)

else:
    protein_goal = data["goal"]
    print(f"Your daily protein goal: {protein_goal}g")

# Track daily protein intake
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
    os.system("python3 week_summary.py")

# Ask if the user wants to reset their goal
change_goal = input("Change goal? (yes/no): ").lower()

if change_goal == "yes":
    print("Interesting choice")

    if data.get("goal_type") == "gain":
        print("Switching to a weight loss goal.")
        weight = get_float_input("Enter goal body weight (lbs): ")
        protein_goal = weight * 0.5
        data["goal_type"] = "lose"
        print("Your goal now is to **lose weight & muscle**.")
    else:
        print("Switching to a weight gain goal.")
        weight = get_float_input("Enter current body weight (lbs): ")
        protein_goal = weight * 0.5
        data["goal_type"] = "gain"
        print("Your goal now is to **gain weight & muscle**.")

    # Save new goal and reset weekly intake
    data["goal"] = protein_goal
    data["protein_intake"] = {}
    save_data(data)

    print(f"New daily protein goal set: {protein_goal}g")
    os.system("python3 protein_tracker.py")

else:
    print("/// Goal remains same. Come back tomorrow!")
