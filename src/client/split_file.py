import os
import zipfile
from encryption import encrypt_chunk
from encryptionKey import save_encryption_key_to_config
import secrets

def split_file_into_chunks_with_encryption(file_path, chunk_size=20 * 1024 * 1024, peer_directory="C:/Peers/chunk", encryption_key=None, config_file_path='config.json'):
    """Split a file into chunks, encrypt each chunk, and save it in the specified directory."""
    encryption_key = secrets.token_bytes(32)
    os.makedirs(peer_directory, exist_ok=True)
    chunk_number = 0
    chunk_files = []
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            chunk_filename = os.path.join(peer_directory, f"{os.path.basename(file_path)}_chunk_{chunk_number}")
            encrypted_chunk_data = encrypt_chunk(chunk, encryption_key)
            # Save the encrypted chunk to a file
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(encrypted_chunk_data)
            # Compress the chunk into a zip file
            zip_filename = chunk_filename + '.zip'
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(chunk_filename, os.path.basename(chunk_filename))
            os.remove(chunk_filename)  # Delete the uncompressed chunk file
            chunk_files.append(zip_filename)
            chunk_number += 1
    print(f"All chunks have been encrypted, compressed, and saved.")
    
    # Save the encryption key to the config file after the encryption process
    save_encryption_key_to_config(encryption_key, config_file_path)
    return chunk_files