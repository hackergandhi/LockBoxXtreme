#!/usr/bin/env python3

import os
import re
import json
import base64
import random
import string
import sys
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Constants and configurations
PASSWORD_FILE = "passwords.json"
MASTER_PASSWORD_FILE = "master_password.json"

# Utility functions for colors and clearing screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

# Function to generate a key from the master password
def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# Encryption and Decryption functions
def encrypt_message(message: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

# Password management functions
def validate_password(password: str) -> bool:
    if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password) or not re.search("[@#$%^&+=]", password):
        print("🚨 Password must be 8+ chars with a mix of upper, lower, digits, and special chars.")
        return False
    return True

def load_passwords() -> dict:
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_passwords(passwords: dict):
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(passwords, file, indent=4)

def set_master_password():
    """
    Set the master password for the first time.
    """
    if os.path.exists(MASTER_PASSWORD_FILE):
        with open(MASTER_PASSWORD_FILE, 'r') as file:
            return json.load(file)["master_password"]
    while True:
        print_colored("🔐 Set up your master password:", "33")
        master_password = input("Enter a strong master password: ").strip()
        if validate_password(master_password):
            with open(MASTER_PASSWORD_FILE, 'w') as file:
                json.dump({"master_password": master_password}, file)
            print_colored("✅ Master password set successfully!", "32")
            return master_password

def authenticate_master_password():
    """
    Authenticate the user using the master password.
    """
    master_password = set_master_password()
    for _ in range(3):
        entered_password = input("Enter your master password to proceed: ").strip()
        if entered_password == master_password:
            return True
        print_colored("🚨 Incorrect master password. Try again.", "31")
    print_colored("❌ Too many incorrect attempts. Exiting...", "31")
    sys.exit()

# Function to show the welcome screen
def show_welcome_screen():
    clear_screen()
    print_colored("┌───────────────────────────────────────┐", "34")
    print_colored("│          Welcome to LockBoxXtreme      │", "34")
    print_colored("│         Your Secure Password Vault     │", "34")
    print_colored("└───────────────────────────────────────┘", "34")
    print_colored("🔒 Keep your passwords safe and secure! 🔒", "36")
    print_colored("Powered by LockBoxXtreme 💪", "36")
    print("\n")

# Main program logic
def main():
    clear_screen()
    show_welcome_screen()
    authenticate_master_password()
    
    while True:
        print_colored("\n==========================", "34")
        print_colored("        Main Menu         ", "34")
        print_colored("==========================", "34")
        print("1. 🔐 Store a new password")
        print("2. 🔍 Retrieve a password")
        print("3. 🗑️  Delete a service")
        print("4. 💾 Create a backup")
        print("5. 🔄 Restore from a backup")
        print("6. 🔧 Generate a strong password")
        print("7. 🚪 Exit")
        print_colored("==========================", "34")
        choice = input("Select an option (1-7): ").strip()

        if choice == '1':
            service = input("Enter the service name: ").strip()
            password = input("Enter the password: ").strip()
            master_password = input("Re-enter your master password: ").strip()
            store_password(service, password, master_password)
        elif choice == '2':
            service = input("Enter the service name: ").strip()
            master_password = input("Enter your master password: ").strip()
            retrieve_password(service, master_password)
        elif choice == '3':
            service = input("Enter the service name to delete: ").strip()
            delete_service(service)
        elif choice == '4':
            master_password = input("Enter your master password for backup: ").strip()
            backup_passwords(master_password)
        elif choice == '5':
            backup_filename = input("Enter the backup filename (e.g., backup.enc): ").strip()
            master_password = input("Enter your master password for restoration: ").strip()
            restore_passwords(backup_filename, master_password)
        elif choice == '6':
            length = input("Enter the desired password length (min 8): ").strip()
            if length.isdigit() and int(length) >= 8:
                print_colored(f"🔑 Generated password: {generate_random_password(int(length))}", "32")
            else:
                print_colored("🚨 Password length should be a number and at least 8 characters.", "31")
        elif choice == '7':
            print_colored("Thank you for using LockBoxXtreme. Goodbye! 🚪", "32")
            break
        else:
            print_colored("🚨 Invalid choice. Please enter a number between 1 and 7.", "31")

if __name__ == "__main__":
    main()
