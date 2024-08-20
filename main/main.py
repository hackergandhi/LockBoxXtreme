import sys
import os
import time
import colorama
from colorama import Fore, Style
from encryptor import generate_key, load_key, encrypt_message, decrypt_message, validate_password
from storage import save_passwords, load_passwords, delete_service
from getpass import getpass
import json

sys.dont_write_bytecode = True
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

def main():
    """
    Main function to interact with the user and manage passwords.
    """
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
        print(f"{Fore.YELLOW}5) Exit {Fore.MAGENTA}(Bye for now!)")
        
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
            print(f"{Fore.GREEN}👋 Exiting. Stay safe!")
            break

        else:
            clear_screen()
            print_banner()
            print(f"{Fore.RED}❌ Invalid option selected. Are you even trying?")
            time.sleep(1)

if __name__ == "__main__":
    main()
