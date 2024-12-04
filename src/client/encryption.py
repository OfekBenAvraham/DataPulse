from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_chunk(chunk_path, encrypted_chunk_path, key):
    "Chunk encryption with AES (CBC mode)"
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    with open(chunk_path, 'rb') as f:
        chunk_data = f.read()
    ciphertext = encryptor.update(chunk_data) + encryptor.finalize()
    with open(encrypted_chunk_path, 'wb') as f:
        f.write(iv + ciphertext)
    print(f"Encrypted chunk saved in-{encrypted_chunk_path}")

def encrypt_all_chunks(file_path, chunk_size=20 * 1024 * 1024, key=None):
    chunk_number = 0
    while True:
        chunk_filename = f"{file_path}\Charlie_and_the_chocolate_factory.avi_chunk_{chunk_number}"
        if not os.path.exists(chunk_filename): 
            break
        encrypted_chunk_filename = f"{chunk_filename}.enc"
        encrypt_chunk(chunk_filename, encrypted_chunk_filename, key)
        chunk_number += 1

file_path = r"C:\Users\rotem\Desktop\bittorent\movie"
key = os.urandom(32)
encrypt_all_chunks(file_path, key=key)