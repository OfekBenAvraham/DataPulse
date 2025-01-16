import os
from split_file import split_file_into_chunks_with_encryption
from sendRequest import save_all_chunks_locally
import os
import mimetypes

PEERS_BASE_DIR = "C:/Peers"
CHUNKS_DIR = os.path.join(PEERS_BASE_DIR, "chunks") 
FILES_DIR = os.path.join(PEERS_BASE_DIR, "files")  

def ensure_directories_exist():
    os.makedirs(PEERS_BASE_DIR, exist_ok=True) 
    os.makedirs(CHUNKS_DIR, exist_ok=True)   
    os.makedirs(FILES_DIR, exist_ok=True)    
    print(f"Directories ensured: {PEERS_BASE_DIR}, {CHUNKS_DIR}, {FILES_DIR}")

def get_file_type(file_path):
    """Identifies the file type based on the extension."""
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type.split('/')[1]
    return 'unknown'

if __name__ == "__main__":
    file_path = input("Please enter the file path to split: ")
    file_name = os.path.basename(file_path)
    file_type = get_file_type(file_path)
    print(f"File name: {file_name}, File type: {file_type}")
    
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
    else:
        print(f"File '{file_name}' does not exist on the server. Starting the process...")
        ensure_directories_exist() 
        encryption_key = os.urandom(32)
        chunk_files = split_file_into_chunks_with_encryption(
            file_path=file_path,
            chunk_size=20 * 1024 * 1024,
            peer_directory=CHUNKS_DIR, 
            encryption_key=encryption_key
        )
        metadata_file = os.path.join(CHUNKS_DIR, "metadata.json")
        save_all_chunks_locally(file_path, CHUNKS_DIR, metadata_file)
