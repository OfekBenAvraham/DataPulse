import os
import shutil
import hashlib
import json
import bencodepy
import mimetypes
import requests

def check_file_with_server(file_name, file_type, tracker_url="http://yourserver.com/check_file"):
    """Check if the file already exists on the server."""
    payload = {"file_name": file_name, "type": file_type}
    try:
        response = requests.post(tracker_url, json=payload)
        server_response = response.json()
        return server_response.get("exist", False)
    except requests.RequestException as e:
        print(f"Error communicating with server: {e}")
        return False


def compute_hash(file_path):
    """Compute the SHA-1 hash of a file."""
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def save_chunk_locally(chunk_path, save_directory, metadata, chunk_index):
    """Save the chunk locally and update metadata."""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    destination_path = os.path.join(save_directory, os.path.basename(chunk_path))
    shutil.copy(chunk_path, destination_path)
    chunk_hash = compute_hash(destination_path)
    metadata.append({
        "chunk_index": chunk_index,
        "chunk_name": os.path.basename(chunk_path),
        "chunk_path": destination_path,
        "hash": chunk_hash,
        "size": os.path.getsize(destination_path),
    })

    print(f"Chunk {chunk_path} saved locally to {destination_path}")
def save_all_chunks_locally(file_path, save_directory, metadata_file):
    """Save all encrypted chunks locally and generate metadata."""
    chunk_number = 0
    base_name = os.path.basename(file_path)
    metadata = []
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"Chunks directory created: {save_directory}")
    
    while True:
        chunk_filename = os.path.join(save_directory, f"{base_name}_chunk_{chunk_number}.enc")
        if not os.path.exists(chunk_filename):
            break
        save_chunk_locally(chunk_filename, save_directory, metadata, chunk_number)
        chunk_number += 1
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to {metadata_file}")
    #create_torrent(file_path, metadata, save_directory)


def get_file_type(file_path):
    # Identifies the file type based on the extension
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type.split('/')[1]
    return 'unknown'  # If the file type can't be identified

def create_torrent(file_path, metadata, save_directory):
    # Create a .torrent file based on the metadata
    tracker_url = "http://trackeraddress.com/announce"
    file_type = get_file_type(file_path)
    torrent_info = {
        'announce': tracker_url,
        'info': {
            'name': os.path.basename(file_path),
            'type': file_type,
            'pieces': b''.join([bytes.fromhex(chunk['hash']) for chunk in metadata]),
            'files': [{'length': chunk['size'], 'path': [chunk['chunk_name']]} for chunk in metadata],
            'total_chunks': int(round((sum([chunk['size'] for chunk in metadata]))/(20 * 1024 * 1024))),
        }
    }
    torrent_file = os.path.join(save_directory, f"{os.path.basename(file_path)}.torrent")
    with open(torrent_file, 'wb') as f:
        f.write(bencodepy.encode(torrent_info))
    print(f"Torrent file created at {torrent_file}")
