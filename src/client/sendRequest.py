import os
import shutil
import hashlib
import json
import bencodepy
import mimetypes

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
    while True:
        chunk_filename = os.path.join(os.path.dirname(file_path), f"{base_name}_chunk_{chunk_number}.enc")
        if not os.path.exists(chunk_filename):
            break
        save_chunk_locally(chunk_filename, save_directory, metadata, chunk_number)
        chunk_number += 1
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to {metadata_file}")
    create_torrent(file_path, metadata, save_directory)

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

    # Prepare the torrent dictionary
    torrent_info = {
        'announce': tracker_url,
        'info': {
            'name': os.path.basename(file_path),
            'type': file_type,
            'pieces': b''.join([bytes.fromhex(chunk['hash']) for chunk in metadata]),  # concatenate all chunk hashes
            'files': [{'length': chunk['size'], 'path': [chunk['chunk_name']]} for chunk in metadata],  # Path of each chunk
            'total_chunks': int(round((sum([chunk['size'] for chunk in metadata]))/(20 * 1024 * 1024))),
        }
    }
    torrent_file = os.path.join(save_directory, f"{os.path.basename(file_path)}.torrent")
    with open(torrent_file, 'wb') as f:
        f.write(bencodepy.encode(torrent_info))
    print(f"Torrent file created at {torrent_file}")

# Example usage
file_path = r"C:\Users\rotem\Desktop\bittorent\movie\Charlie_and_the_chocolate_factory.avi"
save_directory = r"C:\Users\rotem\Desktop\bittorent\chunks"
metadata_file = os.path.join(save_directory, "metadata.json")

# Save chunks locally and generate the .torrent file
save_all_chunks_locally(file_path, save_directory, metadata_file)
