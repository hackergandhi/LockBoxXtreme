import sys
import re
import string
import random
from cryptography.fernet import Fernet

sys.dont_write_bytecode = True

def generate_key():
    return Fernet.generate_key()

def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def validate_password(password: str) -> bool:
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

def generate_random_password(length: int = 12, use_special_chars: bool = True) -> str:
    """
    Generates a random password with the given length.
    """
    chars = string.ascii_letters + string.digits
    if use_special_chars:
        chars += string.punctuation

    password = ''.join(random.choice(chars) for _ in range(length))
    if validate_password(password):
        return password
    else:
        return generate_random_password(length, use_special_chars)
