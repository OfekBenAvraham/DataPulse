# import os
# from split_file import split_file_into_chunks_with_encryption
# from sendRequest import save_all_chunks_locally
# import os
# import mimetypes
# import subprocess
    
# def ensure_base_directory(base_path="C:/Peers/Files"):
#     if not os.path.exists(base_path): 
#         os.makedirs(base_path) 
#         print(f"Directory created: {base_path}")
#     else:
#         print(f"Directory already exists: {base_path}")
#     return base_path  

# def get_file_type(file_path):
#     """Identifies the file type based on the extension."""
#     mime_type, encoding = mimetypes.guess_type(file_path)
#     if mime_type:
#         return mime_type.split('/')[1]
#     return 'unknown'

# if __name__ == "__main__":
#     file_path = input("Please enter the file path to split: ")
#     file_name = os.path.basename(file_path)
#     file_type = get_file_type(file_path)
#     print(f"File name: {file_name}, File type: {file_type}")
    
#     if not os.path.exists(file_path):
#         print(f"The file {file_path} does not exist.")
#     else:
#         # Check with the server if the file already exists
#         #להוריד מהערה אחרי שנעשה את הטרקאר
        
#         # if check_file_with_server(file_name, file_type):
#         #     print(f"The file '{file_name}' already exists on the server. Process stopped.")
#         # else:
#             print(f"File '{file_name}' does not exist on the server. Starting the process...")
#             peer_directory = ensure_base_directory()  
#             encryption_key = os.urandom(32)
#             chunk_files = split_file_into_chunks_with_encryption(
#                 file_path=file_path,  
#                 chunk_size=20 * 1024 * 1024,  
#                 peer_directory=peer_directory,  
#                 encryption_key=encryption_key  
#             )
#             save_directory = os.path.join(peer_directory, "chunks") 
#             metadata_file = os.path.join(save_directory, "metadata.json")
#             save_all_chunks_locally(file_path, save_directory, metadata_file)
#             print("Starting the chunk sender server (peerSendChunks)...")
#             subprocess.Popen(["python", "peerSendChunks.py"]) 
import os
import json
from split_file import split_file_into_chunks_with_encryption
from sendRequest import save_all_chunks_locally
import os
import mimetypes
import subprocess

# תיקיות
PEERS_BASE_DIR = "C:/Peers"
CHUNKS_DIR = os.path.join(PEERS_BASE_DIR, "chunks")  # תיקיית הצ'אנקים
FILES_DIR = os.path.join(PEERS_BASE_DIR, "files")    # תיקיית הקבצים המאוחדים

# פונקציה לוודא שהתיקיות קיימות
def ensure_directories_exist():
    os.makedirs(PEERS_BASE_DIR, exist_ok=True)  # יצירת תיקיית בסיס
    os.makedirs(CHUNKS_DIR, exist_ok=True)      # יצירת תיקיית chunks
    os.makedirs(FILES_DIR, exist_ok=True)       # יצירת תיקיית files
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
        ensure_directories_exist()  # לוודא שהתיקיות קיימות
        encryption_key = os.urandom(32)
        chunk_files = split_file_into_chunks_with_encryption(
            file_path=file_path,
            chunk_size=20 * 1024 * 1024,
            peer_directory=CHUNKS_DIR,  # שמירת הצ'אנקים בתיקיית chunks
            encryption_key=encryption_key
        )
        metadata_file = os.path.join(CHUNKS_DIR, "metadata.json")
        save_all_chunks_locally(file_path, CHUNKS_DIR, metadata_file)