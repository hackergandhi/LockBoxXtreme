#!/usr/bin/env python3

import sys
import os
import time
import colorama
from colorama import Fore, Style
import importlib.util
from getpass import getpass
import json
import shutil

sys.dont_write_bytecode = True

# Load module without extension
def load_module(module_name, module_path):
    # Check if the path without extension exists
    if not os.path.exists(module_path):
        # Attempt to add the .py extension and check again
        module_path_with_extension = module_path + '.py'
        if os.path.exists(module_path_with_extension):
            module_path = module_path_with_extension
        else:
            raise FileNotFoundError(f"Module '{module_name}' not found at '{module_path}'")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise FileNotFoundError(f"Module '{module_name}' not found at '{module_path}'")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load encryptor and storage modules
encryptor = load_module("encryptor", "./encryptor")
storage = load_module("storage", "./storage")

# Import functions from the loaded modules
generate_key = encryptor.generate_key
load_key = encryptor.load_key
encrypt_message = encryptor.encrypt_message
decrypt_message = encryptor.decrypt_message
validate_password = encryptor.validate_password
update_encryption_key = encryptor.update_encryption_key

save_passwords = storage.save_passwords
load_passwords = storage.load_passwords
delete_service = storage.delete_service

# Prevent the creation of __pycache__
def remove_pycache():
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')

remove_pycache()

colorama.init(autoreset=True)

def clear_screen():
    """
    Clears the terminal screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Fore.CYAN}┌─────────────────────────────────────────────────────┐
│                                                     │
│        {Fore.RED}Welcome to the LockBoxXtreme!{Fore.CYAN}         │
│                                                     │
│      {Fore.GREEN}Your password guardian and cringy buddy!{Fore.CYAN}   │
│                                                     │
└─────────────────────────────────────────────────────┘
"""
    print(banner)

def print_help():
    help_text = f"""
{Fore.CYAN}LockBoxXtreme - Password Management Tool

Usage: python main [options]

Options:
-h, --help                Show this help message and exit
1) Store Password         Store a new password securely.
2) Retrieve Password      Retrieve a stored password.
3) View All Services      View all services with stored passwords.
4) Delete a Service       Delete a stored password for a specific service.
5) Update Master Password Update your master password.
6) Exit                   Exit the application.

{Fore.YELLOW}Example:
python main            Run the interactive menu.
python main -h         Show help message.
"""
    print(help_text)

def update_master_password():
    """
    Allows the user to update the master password.
    """
    passwords = load_passwords()

    if not passwords:
        print(f"{Fore.RED}🚨 No passwords stored. Nothing to update!")
        return

    old_password = getpass(f"{Fore.CYAN}🔑 Enter your current master password: {Fore.YELLOW}")
    try:
        old_key = load_key(old_password, salt)
        # Attempt to decrypt one of the passwords to ensure the old key is correct
        decrypt_message(next(iter(passwords.values())).encode(), old_key)
    except Exception:
        print(f"{Fore.RED}❌ Incorrect master password. Update failed.")
        return

    new_password = getpass(f"{Fore.CYAN}🔑 Enter your new master password: {Fore.YELLOW}")
    if not validate_password(new_password):
        print(f"{Fore.RED}❌ New password did not meet the requirements. Update failed.")
        return

    confirm_password = getpass(f"{Fore.CYAN}🔑 Confirm your new master password: {Fore.YELLOW}")
    if new_password != confirm_password:
        print(f"{Fore.RED}❌ Passwords do not match. Update failed.")
        return

    new_key, new_salt = generate_key(new_password)

    updated_passwords = update_encryption_key(old_key, new_key, passwords)

    save_passwords(updated_passwords)

    with open("secret.salt", "wb") as salt_file:
        salt_file.write(new_salt)

    print(f"{Fore.GREEN}✅ Master password updated successfully!")

def initial_master_password_setup():
    """
    Sets up the master password initially with validation.
    """
    while True:
        new_password = getpass(f"{Fore.CYAN}🔑 Create your master password: {Fore.YELLOW}")
        if not validate_password(new_password):
            print(f"{Fore.RED}❌ Password did not meet the requirements. Please try again.")
            continue

        confirm_password = getpass(f"{Fore.CYAN}🔑 Confirm your master password: {Fore.YELLOW}")
        if new_password != confirm_password:
            print(f"{Fore.RED}❌ Passwords do not match. Please try again.")
        else:
            break

    new_key, new_salt = generate_key(new_password)
    with open("secret.salt", "wb") as salt_file:
        salt_file.write(new_salt)

    print(f"{Fore.GREEN}✅ Master password setup complete!")

def main():
    """
    Main function to display the menu and handle user choices.
    """
    clear_screen()
    print_banner()

    if not os.path.exists("secret.salt"):
        initial_master_password_setup()

    with open("secret.salt", "rb") as salt_file:
        global salt
        salt = salt_file.read()

    master_password = getpass(f"{Fore.CYAN}🔑 Enter your master password to unlock: {Fore.YELLOW}")
    key = load_key(master_password, salt)

    while True:
        clear_screen()
        print_banner()
        print(f"{Fore.YELLOW}💾 Choose an option:")
        print(f"{Fore.YELLOW}1) Store Password {Fore.MAGENTA}(Keep it safe, bro!)")
        print(f"{Fore.YELLOW}2) Retrieve Password {Fore.MAGENTA}(Don't worry, I got you!)")
        print(f"{Fore.YELLOW}3) View All Services {Fore.MAGENTA}(Check what you have stored!)")
        print(f"{Fore.YELLOW}4) Delete a Service {Fore.MAGENTA}(Remove a stored password!)")
        print(f"{Fore.YELLOW}5) Update Master Password {Fore.MAGENTA}(Secure your vault!)")
        print(f"{Fore.YELLOW}6) Exit {Fore.MAGENTA}(Bye for now!)")

        choice = input(f"{Fore.GREEN}👉 {Fore.CYAN}Enter your choice: {Style.RESET_ALL}")

        if choice == "1":
            clear_screen()
            print_banner()
            service = input(f"{Fore.CYAN}🔐 Enter the service name you wanna protect: {Fore.YELLOW}")
            password = getpass(f"{Fore.CYAN}🔑 Enter the password you wanna save: {Fore.YELLOW}")

            if not validate_password(password):
                print(f"{Fore.RED}❌ Password did not meet the requirements. Please try again.")
                time.sleep(1)
                continue

            encrypted_password = encrypt_message(password, key)

            passwords = load_passwords()
            passwords[service] = encrypted_password.decode()  # Store as a string in JSON
            save_passwords(passwords)
            print(f"{Fore.GREEN}✅ Password for {service} has been locked away safely! 🔒")
            time.sleep(2)

        elif choice == "2":
            clear_screen()
            print_banner()
            service = input(f"{Fore.CYAN}🔍 Enter the service name you wanna retrieve: {Fore.YELLOW}")

            passwords = load_passwords()
            encrypted_password = passwords.get(service)

            if encrypted_password:
                decrypted_password = decrypt_message(encrypted_password.encode(), key)
                print(f"{Fore.GREEN}🎉 Password for {service}: {Fore.YELLOW}{decrypted_password}")
            else:
                print(f"{Fore.RED}🚨 No password found for the given service! Try again, buddy.")
            time.sleep(1)

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
            print()  # Adding space for better readability
            time.sleep(1)

        elif choice == "4":
            clear_screen()
            print_banner()
            service = input(f"{Fore.CYAN}🗑️ Enter the service name you wanna delete: {Fore.YELLOW}")
            delete_service(service)
            time.sleep(1)

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
            clear_screen()
            print_banner()
            print(f"{Fore.RED}❌ Invalid option selected. Are you even trying?")
            time.sleep(1)

if __name__ == "__main__":
    main()

    # Ensure __pycache__ is removed at the end of the script
    remove_pycache()
