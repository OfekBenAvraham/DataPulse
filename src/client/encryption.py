from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets

def encrypt_chunk(chunk_data, encryption_key):
    """Encrypt a chunk using AES in CBC mode."""
    iv = secrets.token_bytes(16)  # Create a random IV
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(chunk_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data  # Prepend IV to encrypted data for later use in decryption