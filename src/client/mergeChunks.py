import os
import zipfile
from decryption import decrypt_chunk
from encryptionKey import load_encryption_key_from_config

def merge_chunks(output_file_path, file_name, total_chunks, peer_directory):
    """Merge encrypted chunks, decrypt them, and save them to a single file."""
    try:
        encryption_key = load_encryption_key_from_config()
        with open(output_file_path, 'wb') as output_file:
            for i in range(total_chunks):
                chunk_filename = os.path.join(peer_directory, f"{file_name}_chunk_{i}.zip")
                print(f"Looking for: {chunk_filename}")
                
                if os.path.exists(chunk_filename):
                    with zipfile.ZipFile(chunk_filename, 'r') as zipf:
                        zipf.extractall(peer_directory)
                        extracted_chunk_filename = os.path.join(peer_directory, f"{file_name}_chunk_{i}")
                        with open(extracted_chunk_filename, 'rb') as chunk_file:
                            encrypted_chunk_data = chunk_file.read()
                            decrypted_chunk = decrypt_chunk(encrypted_chunk_data, encryption_key)
                            output_file.write(decrypted_chunk)
                            print(f"Chunk {i} decrypted and merged successfully from {chunk_filename}")
                        os.remove(extracted_chunk_filename)
                else:
                    print(f"Error: Chunk not found {chunk_filename}")
                    
        print(f"Merged file created: {output_file_path}")
        return True
    except Exception as e:
        print(f"Error during merging: {e}")
        return False
