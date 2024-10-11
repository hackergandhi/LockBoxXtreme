#!/usr/bin/env python3

import json
import os
import base64
from datetime import datetime, timedelta
from encryptor import generate_key, encrypt_message, decrypt_message

def save_passwords(passwords: dict):
    """
    Saves passwords to a JSON file, backing up the previous version before saving.
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
        print(f"🚨 Error saving passwords: {e}")
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
        print("🚨 Error: passwords.json file not found! Starting fresh.")
        return {}
    except (json.JSONDecodeError, ValueError):
        print("🚨 Error: Corrupted or empty passwords file. Restoring from backup.")
        if os.path.exists('passwords_backup.json'):
            os.rename('passwords_backup.json', 'passwords.json')
            return load_passwords()
        return {}

def add_password(service: str, password: str, master_password: str):
    """
    Adds a new password for a service, encrypting it with the master password.
    """
    passwords = load_passwords()
    salt = os.urandom(16)
    key = generate_key(master_password, salt)
    encrypted_password = encrypt_message(password, key)
    encoded_password = base64.b64encode(encrypted_password).decode()
    encoded_salt = base64.b64encode(salt).decode()
    passwords[service] = {
        "password": encoded_password,
        "salt": encoded_salt,
        "created_at": str(datetime.now()),
        "expires_at": str(datetime.now() + timedelta(days=90))
    }
    save_passwords(passwords)
    print(f"✅ {service} password saved successfully!")

def retrieve_password(service: str, master_password: str):
    """
    Retrieves and decrypts the password for a given service using the master password.
    """
    passwords = load_passwords()
    if service in passwords:
        encoded_password = passwords[service]["password"]
        encoded_salt = passwords[service]["salt"]
        salt = base64.b64decode(encoded_salt)
        key = generate_key(master_password, salt)
        encrypted_password = base64.b64decode(encoded_password)
        try:
            password = decrypt_message(encrypted_password, key)
            expires_at = datetime.fromisoformat(passwords[service]["expires_at"])
            if expires_at < datetime.now():
                print(f"⚠️ The password for {service} has expired. Consider updating it.")
            print(f"🔓 {service} password: {password}")
        except Exception as e:
            print(f"🚨 Error decrypting password: {e}")
    else:
        print(f"🚨 No password found for {service}.")

def delete_service(service: str):
    """
    Deletes a specific service from the passwords file.
    """
    passwords = load_passwords()
    if service in passwords:
        del passwords[service]
        save_passwords(passwords)
        print(f"✅ {service} has been removed successfully.")
    else:
        print(f"🚨 No such service found.")
