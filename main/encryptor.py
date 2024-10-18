#!/usr/bin/env python3

import os
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import random
import string

def generate_key(password: str, salt: bytes) -> bytes:
    """
    Generates an encryption key based on a password using PBKDF2HMAC.
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
        print("🚨 Password should be at least 8 characters long.")
        return False
    if not re.search("[a-z]", password):
        print("🚨 Password should contain at least one lowercase letter.")
        return False
    if not re.search("[A-Z]", password):
        print("🚨 Password should contain at least one uppercase letter.")
        return False
    if not re.search("[0-9]", password):
        print("🚨 Password should contain at least one digit.")
        return False
    if not re.search("[@#$%^&+=]", password):
        print("🚨 Password should contain at least one special character.")
        return False
    return True

def password_strength(password: str) -> str:
    """
    Provides feedback on the strength of the password.
    """
    length = len(password)
    if length >= 16 and re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[@#$%^&+=]", password):
        return "Strong"
    elif length >= 12:
        return "Moderate"
    else:
        return "Weak"

def generate_random_password(length=12) -> str:
    """
    Generates a strong random password with the specified length.
    """
    characters = string.ascii_letters + string.digits + '@#$%^&+='
    return ''.join(random.choice(characters) for _ in range(length))

def generate_2fa_code() -> str:
    """
    Generates a temporary 6-digit 2FA code.
    """
    return str(random.randint(100000, 999999))
