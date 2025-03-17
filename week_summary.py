import json
import datetime

# Load data from JSON file
def load_data():
    try:
        with open("protein_tracker.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data back to JSON file
def save_data(data):
    with open("protein_tracker.json", "w") as file:
        json.dump(data, file)

# Run weekly and monthly summary
def calculate_summary():
    data = load_data()

    # If no weekly data, return
    if "protein_intake" not in data or not data["protein_intake"]:
        print("No data found for this week.")
        return

    # Get the current date info
    today = datetime.datetime.today()
    week_number = today.strftime("%U")  # Current week of the year
    month_name = today.strftime("%B")  # Current month

    # Calculate total and average for the week
    total_protein = sum(data["protein_intake"].values())
    avg_protein = total_protein / len(data["protein_intake"])
    protein_goal = data["goal"]

    print(f"--- Week {week_number} Summary ---")
    print(f"Total protein eaten: {total_protein}g")
    print(f"Daily average: {avg_protein:.2f}g")
    print(f"Goal per day: {protein_goal}g")

    if avg_protein > protein_goal:
        print("Above goal for the week.")
    elif avg_protein == protein_goal:
        print("Met goal for the week.")
    else:
        print("Below goal for the week.")

    # Store weekly data in monthly tracking
    if "monthly_data" not in data:
        data["monthly_data"] = {}

    if month_name not in data["monthly_data"]:
        data["monthly_data"][month_name] = []

    data["monthly_data"][month_name].append({
        "week": week_number,
        "total_protein": total_protein,
        "avg_protein": avg_protein
    })

    # Reset for next week
    data.pop("protein_intake", None)

    # If it's the last week of the month, show monthly summary
    if today.day >= 25:
        calculate_monthly_summary(data, month_name)

    save_data(data)

# Run monthly summary
def calculate_monthly_summary(data, month_name):
    if "monthly_data" not in data or month_name not in data["monthly_data"]:
        print("No monthly data available.")
        return

    print(f"\n=== {month_name} Monthly Summary ===")

    total_monthly_protein = 0
    num_weeks = len(data["monthly_data"][month_name])

    for week in data["monthly_data"][month_name]:
        total_monthly_protein += week["total_protein"]

    avg_monthly_protein = total_monthly_protein / num_weeks

    print(f"Total protein eaten in {month_name}: {total_monthly_protein}g")
    print(f"Weekly average: {avg_monthly_protein:.2f}g")

    if avg_monthly_protein > data["goal"]:
        print("Above goal for the month.")
    elif avg_monthly_protein == data["goal"]:
        print("Met goal for the month.")
    else:
        print("Below goal for the month.")

    # Reset for new month
    data.pop("monthly_data", None)
    save_data(data)

if __name__ == "__main__":
    calculate_summary()
