from cryptography.fernet import Fernet
import hashlib

# Functions related to key management
def create_key(path):
    key = Fernet.generate_key()
    with open(path, "wb") as key_file:
        key_file.write(key)

def load_key(path):
    with open(path, "rb") as key_file:
        return key_file.read()

# Functions related to encryption and decryption
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode("utf-8"))
    return encrypted_password

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_bytes = fernet.decrypt(encrypted_password)
    return decrypted_bytes.decode("utf-8")

# Function for hashing
def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
