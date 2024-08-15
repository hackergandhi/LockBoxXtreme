import sys
sys.dont_write_bytecode = True

import colorama
from colorama import Fore, Style
from encryptor import generate_key, load_key, encrypt_message, decrypt_message
from storage import save_passwords, load_passwords

colorama.init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}************************************************************
*                                                          *
*          {Fore.RED}Welcome to the LockBoxXtreme!{Fore.CYAN}          *
*                                                          *
*         {Fore.GREEN}Your password guardian and cringy buddy!{Fore.CYAN}       *
*                                                          *
************************************************************
"""
    print(banner)

def main():
    """
    Main function to interact with the user and manage passwords.
    """
    print_banner()
    
    print(f"{Fore.MAGENTA}💾 Choose an option:")
    print(f"{Fore.YELLOW}1) Store Password {Fore.MAGENTA}(Keep it safe, bro!)")
    print(f"{Fore.YELLOW}2) Retrieve Password {Fore.MAGENTA}(Don't worry, I got you!)")
    
    choice = input(f"{Fore.GREEN}👉 {Fore.CYAN}Enter your choice: {Style.RESET_ALL}")

    key = None
    try:
        key = load_key()
    except FileNotFoundError:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    if choice == "1":
        service = input(f"{Fore.CYAN}🔐 Enter the service name you wanna protect: {Fore.YELLOW}")
        password = input(f"{Fore.CYAN}🔑 Enter the password you wanna save: {Fore.YELLOW}")

        encrypted_password = encrypt_message(password, key)

        passwords = load_passwords()
        passwords[service] = encrypted_password.decode()  # Store as a string in JSON
        save_passwords(passwords)
        print(f"{Fore.GREEN}✅ Password for {service} has been locked away safely! 🔒")

    elif choice == "2":
        service = input(f"{Fore.CYAN}🔍 Enter the service name you wanna retrieve: {Fore.YELLOW}")

        passwords = load_passwords()
        encrypted_password = passwords.get(service)

        if encrypted_password:
            decrypted_password = decrypt_message(encrypted_password.encode(), key)
            print(f"{Fore.GREEN}🎉 Password for {service}: {Fore.YELLOW}{decrypted_password}")
        else:
            print(f"{Fore.RED}🚨 No password found for the given service! Try again, buddy.")

    else:
        print(f"{Fore.RED}❌ Invalid option selected. Are you even trying?")

if __name__ == "__main__":
    main()
