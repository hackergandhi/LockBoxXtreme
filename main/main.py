import sys
import os
import time
import colorama
from colorama import Fore, Style
from encryptor import generate_key, load_key, encrypt_message, decrypt_message, validate_password, generate_random_password
from storage import save_passwords, load_passwords, delete_service
from getpass import getpass
import json
import shutil

sys.dont_write_bytecode = True

def remove_pycache():
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')

remove_pycache()

colorama.init(autoreset=True)

def clear_screen():
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

Usage: python main.py [options]

Options:
-h, --help                Show this help message and exit
1) Store Password         Store a new password securely.
2) Retrieve Password      Retrieve a stored password.
3) View All Services      View all services with stored passwords.
4) Delete a Service       Delete a stored password for a specific service.
5) Search for Service     Search for a service name in stored passwords.
6) Exit                   Exit the application.

{Fore.YELLOW}Example:
python main.py            Run the interactive menu.
python main.py -h         Show help message.
"""
    print(help_text)

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print_help()
        return

    salt = None
    key = None

    try:
        with open("secret.salt", "rb") as salt_file:
            salt = salt_file.read()
    except FileNotFoundError:
        print(f"{Fore.RED}🚨 Salt file not found. A new one will be created.")
        salt = os.urandom(16)
        with open("secret.salt", "wb") as salt_file:
            salt_file.write(salt)

    password = getpass(f"{Fore.CYAN}🔑 Enter your master password: {Fore.YELLOW}")
    key = load_key(password, salt)

    while True:
        clear_screen()
        print_banner()
        
        print(f"{Fore.MAGENTA}💾 Choose an option:")
        print(f"{Fore.YELLOW}1) Store Password {Fore.MAGENTA}(Keep it safe, bro!)")
        print(f"{Fore.YELLOW}2) Retrieve Password {Fore.MAGENTA}(Don't worry, I got you!)")
        print(f"{Fore.YELLOW}3) View All Services {Fore.MAGENTA}(Check what you have stored!)")
        print(f"{Fore.YELLOW}4) Delete a Service {Fore.MAGENTA}(Remove a stored password!)")
        print(f"{Fore.YELLOW}5) Search for Service {Fore.MAGENTA}(Find a saved service!)")
        print(f"{Fore.YELLOW}6) Exit {Fore.MAGENTA}(Bye for now!)")
        
        choice = input(f"{Fore.GREEN}👉 {Fore.CYAN}Enter your choice: {Style.RESET_ALL}")

        if choice == "1":
            clear_screen()
            print_banner()
            service = input(f"{Fore.CYAN}🔐 Enter the service name you wanna protect: {Fore.YELLOW}")
            use_generated = input(f"{Fore.CYAN}🛠️ Do you want to generate a random password? (y/n): {Fore.YELLOW}").lower()
            
            if use_generated == 'y':
                length = int(input(f"{Fore.CYAN}🔢 Enter desired password length: {Fore.YELLOW}"))
                password = generate_random_password(length)
                print(f"{Fore.GREEN}🛠️ Generated Password: {Fore.YELLOW}{password}")
            else:
                password = getpass(f"{Fore.CYAN}🔑 Enter the password you wanna save: {Fore.YELLOW}")

            if not validate_password(password):
                print(f"{Fore.RED}❌ Password did not meet the requirements. Please try again.")
                time.sleep(1)
                continue

            encrypted_password = encrypt_message(password, key)

            passwords = load_passwords()
            passwords[service] = encrypted_password.decode()
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
            print()
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
            search_term = input(f"{Fore.CYAN}🔍 Enter the service name or keyword to search: {Fore.YELLOW}")
            passwords = load_passwords()
            found_services = [service for service in passwords if search_term.lower() in service.lower()]

            if found_services:
                print(f"{Fore.GREEN}🔍 Services found:")
                for service in found_services:
                    print(f"{Fore.YELLOW} - {service}")
            else:
                print(f"{Fore.RED}🚨 No services matched the search term.")
            print()
            time.sleep(1)

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
