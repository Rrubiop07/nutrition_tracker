import json
import hashlib
import os

USER_DIR = "users"

# Ensure the folder exists
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

# Load user data
def load_user_data(username):
    user_file = os.path.join(USER_DIR, f"{username}.json")
    try:
        with open(user_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

# Save user data (without username & password)
def save_user_data(username, data):
    user_file = os.path.join(USER_DIR, f"{username}.json")
    clean_data = {k: v for k, v in data.items() if k not in ["username", "password"]}
    
    with open(user_file, "w") as file:
        json.dump(clean_data, file, indent=4)

# Hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authenticate user (login or signup)
def authenticate_user():
    while True:
        choice = input("Log in or Sign up? (login/signup): ").strip().lower()

        if choice == "signup":
            while True:
                username = input("Choose a username: ").strip()
                user_file = os.path.join(USER_DIR, f"{username}.json")

                if os.path.exists(user_file):
                    print("/// Username already exists. Try a different one.")
                    continue

                while True:
                    password = input("Choose a password: ").strip()
                    confirm_password = input("Re-enter password: ").strip()

                    if password != confirm_password:
                        print("/// Passwords do not match. Try again.")
                        continue

                    hashed_password = hash_password(password)
                    break  # Passwords match

                nickname = input("Enter your nickname: ").strip()

                user_data = {
                    "nickname": nickname,
                    "goal": None,
                    "protein_intake": {}
                }
                save_user_data(username, user_data)

                with open(os.path.join(USER_DIR, f"{username}_pass.txt"), "w") as pass_file:
                    pass_file.write(hashed_password)

                print(f"/// Account created! Welcome, {nickname}!")
                return username, nickname

        elif choice == "login":
            while True:
                username = input("Enter your username: ").strip()
                user_data = load_user_data(username)
                pass_file_path = os.path.join(USER_DIR, f"{username}_pass.txt")

                if user_data is None or not os.path.exists(pass_file_path):
                    print("/// Username not found. Try again.")
                    continue

                password = input("Enter your password: ").strip()
                hashed_password = hash_password(password)

                with open(pass_file_path, "r") as pass_file:
                    stored_password = pass_file.read().strip()

                if hashed_password == stored_password:
                    nickname = user_data.get("nickname", "User")  
                    return username, nickname  
                else:
                    print("/// Incorrect password. Try again.")

        else:
            print("/// Invalid choice. Type 'login' or 'signup'.")
