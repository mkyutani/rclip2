import os
from urllib.parse import urljoin
from cryptography.fernet import Fernet

def get_api(dir: str) -> str:
    """
    Get the full API URL by joining the server URL with the given directory.
    
    Args:
        dir: API endpoint path
    Returns:
        Full API URL
    """
    server = os.environ.get('RCLIP_API', 'http://localhost:8099')
    return urljoin(server, dir)

def get_crypt_key() -> str | None:
    """
    Get encryption key from RCLIP_KEY environment variable.
    
    Returns:
        The key if RCLIP_KEY is set, None otherwise
    """
    return os.environ.get('RCLIP_KEY', None)

def generate_crypt_key() -> str:
    """Generate a new Fernet key"""
    return Fernet.generate_key().decode('utf-8')

def encrypt(text: str, key: str) -> str:
    """Encrypt text using the given key"""
    f = Fernet(key.encode('utf-8'))
    encrypted = f.encrypt(text.encode('utf-8'))
    return encrypted.decode('utf-8')

def decrypt(encrypted: str, key: str) -> str:
    """Decrypt text using the given key"""
    f = Fernet(key.encode('utf-8'))
    decrypted = f.decrypt(encrypted.encode('utf-8'))
    return decrypted.decode('utf-8')