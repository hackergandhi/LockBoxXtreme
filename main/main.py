#!/usr/bin/env python3

import os
import sys
import time
import json
import shutil
from getpass import getpass
from colorama import Fore, Style, init
from encryptor import generate_key, encrypt_message, decrypt_message, validate_password, password_strength
from storage import add_password, retrieve_password, delete_service, load_passwords, save_passwords

# Initialize Colorama for colored terminal output
init(autoreset=True)

# Prevent creation of __pycache__
def remove_pycache():
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')

remove_pycache()

def clear_screen():
    """
    Clears the terminal screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Fore.CYAN}┌────────────────────────────────────────────────┐
{Fore.CYAN}│{Fore.YELLOW}           ENHANCED PASSWORD MANAGER           {Fore.CYAN}│
{Fore.CYAN}└────────────────────────────────────────────────┘
    """
    print(banner)

def update_master_password():
    """
    Handles the master password update process, re-encrypting stored passwords.
    """
    print(f"{Fore.CYAN}🔄 Master Password Update:")
    current_master = getpass("Enter current master password: ").strip()
    passwords = load_passwords()
    if not passwords:
        print(f"{Fore.RED}🚨 No passwords stored. Nothing to update.")
        return
    
    new_master = getpass("Enter new master password: ").strip()
    confirm_master = getpass("Confirm new master password: ").strip()

    if new_master != confirm_master:
        print(f"{Fore.RED}🚨 Passwords do not match. Try again.")
        return

    if not validate_password(new_master):
        print(f"{Fore.RED}🚨 New master password did not meet the security criteria.")
        return

    for service, data in passwords.items():
        encoded_password = data["password"]
        encoded_salt = data["salt"]
        salt = base64.b64decode(encoded_salt)
        key = generate_key(current_master, salt)

        try:
            encrypted_password = base64.b64decode(encoded_password)
            decrypted_password = decrypt_message(encrypted_password, key)
            # Re-encrypt with the new master password
            new_salt = os.urandom(16)
            new_key = generate_key(new_master, new_salt)
            new_encrypted_password = encrypt_message(decrypted_password, new_key)
            passwords[service]["password"] = base64.b64encode(new_encrypted_password).decode()
            passwords[service]["salt"] = base64.b64encode(new_salt).decode()
        except Exception as e:
            print(f"{Fore.RED}🚨 Error re-encrypting password for {service}: {e}")
            return

    save_passwords(passwords)
    print(f"{Fore.GREEN}✅ Master password updated and passwords re-encrypted successfully!")

def main():
    """
    Main function to handle user interaction with the password manager.
    """
    print_banner()
    while True:
        print("\nOptions:")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. View saved services")
        print("4. Delete a service")
        print("5. Update master password")
        print("6. Exit")

        choice = input(f"{Fore.CYAN}Enter your choice: {Fore.YELLOW}").strip()

        if choice == "1":
            clear_screen()
            print_banner()
            service = input(f"{Fore.CYAN}💾 Enter the service name to save: {Fore.YELLOW}").strip()
            password = getpass(f"{Fore.CYAN}🔑 Enter the password for {service}: {Fore.YELLOW}").strip()
            master_password = getpass(f"{Fore.CYAN}🔒 Enter your master password: {Fore.YELLOW}").strip()

            if validate_password(master_password):
                strength = password_strength(master_password)
                print(f"{Fore.GREEN}🔍 Password strength: {strength}")
                add_password(service, password, master_password)
            else:
                print(f"{Fore.RED}🚨 Master password did not meet security requirements.")
            time.sleep(2)

        elif choice == "2":
            clear_screen()
            print_banner()
            service = input(f"{Fore.CYAN}🔍 Enter the service name you want to retrieve: {Fore.YELLOW}").strip()
            master_password = getpass(f"{Fore.CYAN}🔒 Enter your master password: {Fore.YELLOW}").strip()
            retrieve_password(service, master_password)
            time.sleep(2)

        elif choice == "3":
            clear_screen()
            print_banner()
            passwords = load_passwords()
            if passwords:
                print(f"{Fore.CYAN}🔍 Saved services:")
                for service in passwords:
                    print(f"{Fore.YELLOW} - {service}")
            else:
                print(f"{Fore.RED}🚨 No services saved yet.")
            time.sleep(2)

        elif choice == "4":
            clear_screen()
            print_banner()
            service = input(f"{Fore.CYAN}🗑️ Enter the service name you want to delete: {Fore.YELLOW}").strip()
            delete_service(service)
            time.sleep(2)

        elif choice == "5":
            clear_screen()
            print_banner()
            update_master_password()
            time.sleep(2)

        elif choice == "6":
            clear_screen()
            print(f"{Fore.GREEN}👋 Exiting. Stay safe!")
            break

        else:
            print(f"{Fore.RED}❌ Invalid option selected. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()
    remove_pycache()
