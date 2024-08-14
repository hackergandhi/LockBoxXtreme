import json

def save_passwords(passwords: dict):
    """
    Saves the encrypted passwords to a JSON file.
    """
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f, indent=4)

def load_passwords() -> dict:
    """
    Loads the encrypted passwords from the JSON file.
    """
    try:
        with open('passwords.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
