import os
import json
from split_file import split_file_into_chunks
from encryption import encrypt_chunk
from sendRequest import save_all_chunks_locally
from sendRequest import create_torrent
import os

# def create_metadata_file(peer_directory, file_name, chunk_files):
#     metadata = {
#         "fileName": os.path.basename(file_name),
#         "total_chunks": len(chunk_files),
#         "chunks": chunk_files  # List of all chunk files (including encrypted and zipped)
#     }
#     metadata_file = f"{peer_directory}_metadata.json"
#     with open(metadata_file, 'w') as f:
#         json.dump(metadata, f, indent=4)  # Write metadata as JSON with indentation
#     print(f"Metadata file created: {metadata_file}")
#     return metadata_file

def ensure_base_directory(base_path="C:/Peers/Files"):
    # Check if the directory exists, if not, create it
    if not os.path.exists(base_path):  # If the directory doesn't exist
        os.makedirs(base_path)  # Create the directory at this path
        print(f"Directory created: {base_path}")
    else:
        print(f"Directory already exists: {base_path}")
    return base_path  

if __name__ == "__main__":
    # Request the user to enter the file path to split
    file_path = input("Please enter the file path to split: ")
    file_name = file_path.split("\\")[-1].split(".")[0].replace("_", " ")
    print(file_name)
    
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
    else:
        print(f"File path is: {file_path}")
        peer_directory = ensure_base_directory()
        encryption_key = os.urandom(32)
        chunk_files = split_file_into_chunks(
            file_path, 
            chunk_size=20 * 1024 * 1024, 
            peer_directory=peer_directory, 
            encryption_key=encryption_key
        )
        save_directory = os.path.join(peer_directory, "chunks")
        metadata_file = os.path.join(save_directory, "metadata.json")
        save_all_chunks_locally(file_path, save_directory, metadata_file)
        create_torrent(file_path, metadata_file, save_directory)
        print(f"Process complete. Torrent file and metadata created in {save_directory}.")