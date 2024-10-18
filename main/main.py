from storage import store_password, retrieve_password, delete_service, backup_passwords, restore_passwords
from encryptor import validate_password, password_strength, generate_random_password

def main():
    print("Welcome to the Password Manager")
    while True:
        print("\nOptions:")
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Delete a service")
        print("4. Create a backup")
        print("5. Restore from a backup")
        print("6. Generate a strong password")
        print("7. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            service = input("Enter the service name: ")
            password = input("Enter the password: ")
            master_password = input("Enter your master password: ")
            if validate_password(master_password):
                store_password(service, password, master_password)
        elif choice == '2':
            service = input("Enter the service name: ")
            master_password = input("Enter your master password: ")
            retrieve_password(service, master_password)
        elif choice == '3':
            service = input("Enter the service name to delete: ")
            delete_service(service)
        elif choice == '4':
            master_password = input("Enter your master password for backup: ")
            backup_passwords(master_password)
        elif choice == '5':
            backup_filename = input("Enter the backup filename: ")
            master_password = input("Enter your master password for restoration: ")
            restore_passwords(backup_filename, master_password)
        elif choice == '6':
            length = int(input("Enter the desired password length (min 8): "))
            if length >= 8:
                print(f"Generated password: {generate_random_password(length)}")
            else:
                print("🚨 Password length should be at least 8 characters.")
        elif choice == '7':
            print("Exiting Password Manager. Goodbye!")
            break
        else:
            print("🚨 Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
