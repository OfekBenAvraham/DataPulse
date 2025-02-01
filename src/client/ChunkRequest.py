import os
import requests
from mergeChunks import merge_chunks

PEER_BASE_DIR = "C:\\Peer2" 
CHUNKS_DIR = os.path.join(PEER_BASE_DIR, "chunks") 
FILES_DIR = os.path.join(PEER_BASE_DIR, "files") 

PEERS = ["http://127.0.0.1:5001"]

def ensure_directories_exist():
    os.makedirs(PEER_BASE_DIR, exist_ok=True) 
    os.makedirs(CHUNKS_DIR, exist_ok=True)
    os.makedirs(FILES_DIR, exist_ok=True) 

def request_chunk(peer_ip, chunk_name):
    try:
        chunk_path = os.path.join(CHUNKS_DIR, f"{chunk_name}.zip")
        response = requests.get(f"{peer_ip}/get_chunk", params={"chunk_name": f"{chunk_name}.zip"})
        if response.status_code == 200:
            with open(chunk_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {chunk_name} from {peer_ip} to {chunk_path}")
            return chunk_path
    except Exception as e:
        print(f"Error downloading chunk {chunk_name}: {e}")
    return None


def download_chunks():
    chunks_to_download = [
        f"Merged_Charlie_and_the_chocolate_factory.avi_chunk_{i}" for i in range(35)
    ]
    downloaded_chunks = []
    for chunk_name in chunks_to_download:
        for peer_ip in PEERS:
            chunk_path = request_chunk(peer_ip, chunk_name)
            if chunk_path:
                downloaded_chunks.append(chunk_path)
                break 
    if len(downloaded_chunks) == len(chunks_to_download):
        print("All chunks downloaded successfully.")
    else:
        print("Error: Not all chunks were downloaded.")
    
    return downloaded_chunks


def main():
    ensure_directories_exist()
    print("Starting chunk processing...")
    downloaded_chunks = download_chunks()
    
    if len(downloaded_chunks) == 35:
        output_path = os.path.join(FILES_DIR, "Merged_Charlie_and_the_chocolate_factory.avi")
        if merge_chunks(output_path, "Merged_Charlie_and_the_chocolate_factory.avi", 35, CHUNKS_DIR): 
            print(f"Successfully merged and decrypted to {output_path}")
        else:
            print("Merging and decryption failed.")
    else:
        print("Not all chunks were downloaded. Merging skipped.")
    
if __name__ == "__main__":
    main()
