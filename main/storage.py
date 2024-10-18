import json
import base64
import os
from datetime import datetime, timedelta
from encryptor import encrypt_message, decrypt_message, generate_key, generate_2fa_code

PASSWORD_FILE = "passwords.json"

def load_passwords() -> dict:
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_passwords(passwords: dict):
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(passwords, file, indent=4)

def store_password(service: str, password: str, master_password: str):
    """
    Stores a new password for a service, encrypting it with the master password.
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
            # New feature: 2FA Code generation
            print(f"🔒 2FA Code: {generate_2fa_code()}")
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

def backup_passwords(master_password: str):
    """
    Creates a secure encrypted backup of the passwords file.
    """
    passwords = load_passwords()
    salt = os.urandom(16)
    key = generate_key(master_password, salt)
    backup_data = encrypt_message(json.dumps(passwords), key)
    backup_filename = "backup.enc"
    with open(backup_filename, 'wb') as file:
        file.write(base64.b64encode(salt + backup_data))
    print(f"✅ Backup created as {backup_filename}. Keep it safe.")

def restore_passwords(backup_filename: str, master_password: str):
    """
    Restores passwords from an encrypted backup.
    """
    with open(backup_filename, 'rb') as file:
        data = base64.b64decode(file.read())
        salt = data[:16]
        encrypted_data = data[16:]
        key = generate_key(master_password, salt)
        decrypted_data = decrypt_message(encrypted_data, key)
        passwords = json.loads(decrypted_data)
        save_passwords(passwords)
        print(f"✅ Passwords restored from {backup_filename}.")
