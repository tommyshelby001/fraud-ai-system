import json
import os

# Database file path
DB_FILE = "utils/auth_db.json"


# Load users from JSON file
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}


# Save users to JSON file
def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)


# Register new user
def register_user(username, password):
    users = load_users()

    # Check if user already exists
    if username in users:
        return False

    # Save new user
    users[username] = password
    save_users(users)

    return True


# Login user
def login_user(username, password):
    users = load_users()

    # Validate credentials
    if username in users and users[username] == password:
        return True

    return False