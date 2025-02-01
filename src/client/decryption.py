from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_chunk(encrypted_chunk_data, encryption_key):
    """Decrypt an encrypted chunk using AES in CBC mode."""
    iv = encrypted_chunk_data[:16]  # Extract the IV (first 16 bytes)
    encrypted_data = encrypted_chunk_data[16:]  # The remaining data is the encrypted chunk

    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data