import json

def load_data():
    try:
        with open("protein_tracker.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("protein_tracker.json", "w") as file:
        json.dump(data, file)

def calculate_weekly_summary():
    data = load_data()

    if "protein_intake" not in data or not data["protein_intake"]:
        print("/// No data found for this week.")
        return

    total_protein = sum(data["protein_intake"].values())
    avg_protein = total_protein / len(data["protein_intake"])
    protein_goal = data["goal"]

    print("--- Week Ending Total ---")
    print(f"Total protein eaten: {total_protein}g")
    print(f"Daily average: {avg_protein:.2f}g")
    print(f"Goal per day: {protein_goal}g")

    if avg_protein > protein_goal:
        print("Amazing work all week!!!")
    elif avg_protein == protein_goal:
        print("Wow on point all week!!")
    else:
        print("You gonna have to work on your intake next week.")

    # Reset for next week
    data.pop("goal", None)
    data.pop("protein_intake", None)
    save_data(data)

if __name__ == "__main__":
    calculate_weekly_summary()
