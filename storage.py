import sys
sys.dont_write_bytecode = True

import json
from colorama import Fore

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
        print(f"{Fore.RED}🚨 Error: passwords.json file not found! Starting fresh.")
        return {}
    except json.JSONDecodeError:
        # Handle case where the JSON file is corrupted or empty
        print(f"{Fore.RED}🚨 Error: Corrupted or empty passwords file.")
        return {}
