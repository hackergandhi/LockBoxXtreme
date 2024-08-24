#!/usr/bin/env python3

import sys
import os
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

sys.dont_write_bytecode = True

def generate_key(password: str) -> bytes:
    """
    Generates an encryption key based on a password using PBKDF2HMAC.
    """
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def load_key(password: str, salt: bytes) -> bytes:
    """
    Loads the encryption key using the provided password and salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

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
    Validates the password to ensure it meets enhanced security criteria.
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
    if re.search(r'(.)\1\1', password):
        print("Password should not contain sequences of three or more repeating characters.")
        return False
    return True

def update_encryption_key(old_key: bytes, new_key: bytes, passwords: dict) -> dict:
    """
    Re-encrypts all passwords with the new key.
    """
    updated_passwords = {}
    for service, encrypted_password in passwords.items():
        decrypted_password = decrypt_message(encrypted_password.encode(), old_key)
        updated_passwords[service] = encrypt_message(decrypted_password, new_key).decode()
    return updated_passwords
