#!/usr/bin/env python3

import sys
import os
import json
from colorama import Fore

sys.dont_write_bytecode = True

def save_passwords(passwords: dict):
    """
    Saves the encrypted passwords to a JSON file.
    Backs up the previous version before saving.
    """
    backup_filename = 'passwords_backup.json'
    if os.path.exists('passwords.json'):
        os.rename('passwords.json', backup_filename)

    try:
        with open('passwords.json', 'w') as f:
            json.dump(passwords, f, indent=4)
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
    except Exception as e:
        print(f"{Fore.RED}🚨 Error saving passwords: {e}")
        if os.path.exists(backup_filename):
            os.rename(backup_filename, 'passwords.json')

def load_passwords() -> dict:
    """
    Loads the encrypted passwords from the JSON file.
    """
    try:
        with open('passwords.json', 'r') as f:
            passwords = json.load(f)
            if not isinstance(passwords, dict):
                raise ValueError("Corrupted passwords file format.")
            return passwords
    except FileNotFoundError:
        print(f"{Fore.RED}🚨 Error: passwords.json file not found! Starting fresh.")
        return {}
    except (json.JSONDecodeError, ValueError):
        # Handle case where the JSON file is corrupted or empty
        print(f"{Fore.RED}🚨 Error: Corrupted or empty passwords file. Restoring from backup.")
        try:
            if os.path.exists('passwords_backup.json'):
                os.rename('passwords_backup.json', 'passwords.json')
                return load_passwords()  # Retry loading
            else:
                return {}
        except Exception as e:
            print(f"{Fore.RED}🚨 Unable to restore backup: {e}")
            return {}

def delete_service(service: str):
    """
    Deletes a specific service from the passwords file.
    """
    passwords = load_passwords()
    if service in passwords:
        del passwords[service]
        save_passwords(passwords)
        print(f"{Fore.GREEN}✅ {service} has been removed successfully.")
    else:
        print(f"{Fore.RED}🚨 No such service found.")
