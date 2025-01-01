import os
import zipfile
from encryption import encrypt_chunk 

def split_file_into_chunks(file_path, chunk_size=20 * 1024 * 1024, peer_directory="C:/Peers/Files", encryption_key=None):
    """Split a file into chunks, encrypt each chunk, and save it in the specified directory."""
    os.makedirs(peer_directory, exist_ok=True)
    chunk_number = 0
    chunk_files = []
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            # Define chunk filename 
            chunk_filename = os.path.join(peer_directory, f"{os.path.basename(file_path)}_chunk_{chunk_number}")
            
            # Save the chunk to a file
            with open(chunk_filename, 'wb') as chunk_file: 
                chunk_file.write(chunk)
            
            # Encrypt the chunk
            encrypted_chunk_filename = f"{chunk_filename}.enc"
            encrypt_chunk(chunk_filename, encrypted_chunk_filename, encryption_key)

            # Create a separate ZIP file for each chunk
            zip_filename = f"{encrypted_chunk_filename}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(encrypted_chunk_filename, os.path.basename(encrypted_chunk_filename))
                print(f"Encrypted chunk created and zipped: {zip_filename}")
            
            # Delete the original encrypted chunk after zipping
            os.remove(encrypted_chunk_filename)
            chunk_files.append(zip_filename)
            chunk_number += 1

        print(f"All chunks have been zipped individually.")
    return chunk_number