from cryptography.fernet import Fernet
from app.configs import config
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
key_file_path = os.path.join(script_dir, "image.txt")

with open(key_file_path, "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)


def get_decrypted_value(section, key_name):
    """
    Fetches and decrypts a specific value from the encrypted configuration.

    :param section: The section name (e.g., "mongo_creds").
    :param key_name: The key name in the section (e.g., "host").
    :return: The decrypted value as a string.
    """
    encrypted_section = config.ENCRYPTED_CONFIG.get(section)
    if not encrypted_section:
        raise KeyError(f"Section '{section}' not found in configuration.")

    encrypted_value = encrypted_section.get(key_name)
    if not encrypted_value:
        raise KeyError(f"Key '{key_name}' not found in section '{section}'.")

    # Decrypt and return the value
    if isinstance(encrypted_value, str):  # Encrypted strings are stored as str
        return cipher_suite.decrypt(encrypted_value.encode()).decode()
    return encrypted_value  # Return non-encrypted values as-is
