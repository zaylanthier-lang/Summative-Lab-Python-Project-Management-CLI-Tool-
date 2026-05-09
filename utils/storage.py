import json
import os
from models.user import User

# Path to the local JSON database file
DATA_FILE = "data/db.json"


def load_users():
    """Load all users from the JSON database file."""
    try:
        # If the file does not exist yet, return an empty list
        if not os.path.exists(DATA_FILE):
            return []

        # Open and read the JSON file
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        # Convert saved dictionaries back into User objects
        return [User.from_dict(user) for user in data.get("users", [])]

    except json.JSONDecodeError:
        # Handles broken or malformed JSON
        print("Error: data file is damaged or invalid.")
        return []

    except FileNotFoundError:
        # Handles missing file just in case
        return []


def save_users(users):
    """Save all users to the JSON database file."""
    # Make sure the data folder exists before saving
    os.makedirs("data", exist_ok=True)

    # Convert User objects into dictionaries
    data = {
        "users": [user.to_dict() for user in users]
    }

    # Save the data in a readable JSON format
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def find_user(users, name):
    """Find and return a user by name."""
    for user in users:
        if user.name.lower() == name.lower():
            return user

    return None


def find_project(users, title):
    """Find and return a project by title across all users."""
    for user in users:
        project = user.find_project(title)

        if project:
            return project

    return None