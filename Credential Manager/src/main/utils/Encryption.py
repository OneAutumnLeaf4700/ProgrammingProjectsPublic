from utils.LibraryManager import Fernet, hashlib

# Functions related to key management
def createKey(path):
    key = Fernet.generate_key()
    with open(path, "wb") as key_file:
        key_file.write(key)

def loadKey(path):
    with open(path, "rb") as key_file:
        return key_file.read()

# Functions related to encryption and decryption
def encryptPassword(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode("utf-8"))
    return encrypted_password

def decryptPassword(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_bytes = fernet.decrypt(encrypted_password)
    return decrypted_bytes.decode("utf-8")

# Function for hashing
def hashText(text):
    if isinstance(text, bytes):
        return hashlib.sha256(text).hexdigest()  # Already bytes, no need to encode
    return hashlib.sha256(text.encode("utf-8")).hexdigest()  # Encode if it's a string
