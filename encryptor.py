import sys
sys.dont_write_bytecode = True

from cryptography.fernet import Fernet

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

