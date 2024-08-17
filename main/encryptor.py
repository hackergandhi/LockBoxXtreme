import sys
sys.dont_write_bytecode = True

from cryptography.fernet import Fernet
import re

def generate_key():
    """
    Generates a new encryption key.
    """
    return Fernet.generate_key()

def load_key():
    """
    Loads the encryption key from a file.
    """
    return open("secret.key", "rb").read()

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the provided key.
    """
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """
    Decrypts an encrypted message using the provided key.
    """
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def validate_password(password: str) -> bool:
    """
    Validates the password to ensure it meets certain criteria.
    """
    if len(password) < 8:
        print("Password should be at least 8 characters long.")
        return False
    if not re.search("[a-z]", password):
        print("Password should contain at least one lowercase letter.")
        return False
    if not re.search("[A-Z]", password):
        print("Password should contain at least one uppercase letter.")
        return False
    if not re.search("[0-9]", password):
        print("Password should contain at least one number.")
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password should contain at least one special character.")
        return False
    return True
