from encryptor import generate_key, load_key, encrypt_message, decrypt_message
from storage import save_passwords, load_passwords

def main():
    """
    Main function to interact with the user and manage passwords.
    """
    print("Welcome to LockBoxXtreme!")
    choice = input("Choose an option: (1) Store Password (2) Retrieve Password: ")

    key = None
    try:
        key = load_key()
    except FileNotFoundError:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    if choice == "1":
        service = input("Enter the service name: ")
        password = input("Enter the password: ")

        encrypted_password = encrypt_message(password, key)

        passwords = load_passwords()
        passwords[service] = encrypted_password.decode()  # Store as a string in JSON
        save_passwords(passwords)
        print(f"Password for {service} stored successfully!")

    elif choice == "2":
        service = input("Enter the service name: ")

        passwords = load_passwords()
        encrypted_password = passwords.get(service)

        if encrypted_password:
            decrypted_password = decrypt_message(encrypted_password.encode(), key)
            print(f"Password for {service}: {decrypted_password}")
        else:
            print("No password found for the given service.")

    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
