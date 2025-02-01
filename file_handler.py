import os
import base64
import socket
import zipfile
import hashlib
import requests
import bencodepy
import mimetypes

from fastapi import HTTPException
from threading import Lock, Thread
from encryption_utils import decrypt_data_with_private_key
from flask_socketio import emit
from app_init import socketio

download_progress = 0
    
def get_file_type(file_path):
    # Identifies the file type based on the extension
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type.split('/')[1]
    return 'unknown'  # If the file type can't be identified   

def create_torrent(file_path, metadata, chunk_hashes, torrents_directory, tracker_url):
    """
    Create a .torrent file based on the chunks of a file.

    Args:
        file_path (str): Path to the original file.
        chunk_files (list): List of paths to the zipped chunk files.
        torrents_directory (str): Directory to save the .torrent file.
        tracker_url (str): URL of the tracker to include in the torrent metadata.
    """
    
    torrent_info = {
        'announce': tracker_url,
        'info': {
            'name': metadata["name"],
            'type': metadata["type"],
            'pieces': b''.join(chunk_hashes),  # Concatenate all SHA-1 hashes
            'total_chunks': metadata["total_chunks"],
        }
    }

    torrent_file = os.path.join(torrents_directory, f"{os.path.basename(file_path)}.torrent")
    with open(torrent_file, 'wb') as f:
        f.write(bencodepy.encode(torrent_info))

    print(f"Torrent file created at {torrent_file}")
    return torrent_file



def split_file_into_chunks(file_path, chunk_size, chunks_directory):
    """
    Split a file into chunks and zip each chunk individually.

    Args:
        file_path (str): Path to the input file.
        chunk_size (int): Size of each chunk in bytes (default is 20MB).
        chunks_directory (str): Directory to store the zipped chunks.

    Returns:
        int: Total number of chunks created.
    """
    os.makedirs(chunks_directory, exist_ok=True)
    chunk_number = 0
    chunk_files = []
    chunk_hashes = []
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            # Define chunk filename
            chunk_filename = os.path.join(chunks_directory, f"{os.path.basename(file_path)}_chunk_{chunk_number}")

            # Save the chunk to a file
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
                
            # Compute hash for the chunk
            chunk_hash = hashlib.sha1(chunk).digest()
            chunk_hashes.append(chunk_hash)

            # Create a separate ZIP file for each chunk
            zip_filename = f"{chunk_filename}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(chunk_filename, os.path.basename(chunk_filename))
                print(f"Chunk created and zipped: {zip_filename}")

            # Delete the original chunk after zipping
            os.remove(chunk_filename)
            chunk_files.append(zip_filename)
            chunk_number += 1

        print(f"All chunks have been zipped individually.")
    return chunk_number, chunk_hashes




def check_file_exists(server_url, file_name, file_type, token):
    """
    Check if the file already exists on the tracker.
    
    Args:
        server_url (str): Tracker URL.
        file_name (str): Name of the file.
        file_type (str): Type/extension of the file.
    
    Returns:
        bool: True if the file exists, False otherwise.
    """
    payload = {"name": file_name, "type": file_type}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{server_url}/file/check_file", json=payload, headers=headers)
        if response.status_code == 200:
            return
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="File already exist!") 
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            raise HTTPException(status_code=response.status_code, detail="Unexpected error from tracker.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def add_file_to_tracker(server_url, file_name, file_type, total_chunks, token):
    """
    Send file metadata to the tracker to register a new file.
    
    Args:
        server_url (str): Tracker URL.
        file_name (str): Name of the file.
        file_type (str): Type/extension of the file.
        total_chunks (int): Total number of chunks.
        token (str): JWT token for authentication.
    
    Returns:
        bool: True if the file was added successfully, False otherwise.
    """
    payload = {"name": file_name, "type": file_type, "total_chunks": total_chunks}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{server_url}/file/add_file", json=payload, headers=headers)
        if response.status_code == 200:
            print("File added successfully.")
            return True
        else:
            print(f"Failed to add file. Status code: {response.status_code}")
            print(f"Server response: {response.text}")
            return False
    except Exception as e:
        print(f"Error adding file to tracker: {e}")
        return False

def handle_file_upload(file_path, server_url, token, chunks_directory, torrents_directory):
    """
        Handles the process of uploading a file:
        - Checks if the file exists on the tracker.
        - Splits the file into chunks.
        - Uploads file metadata to the tracker.
        - Creates a .torrent file for the uploaded file.

        Args:
            file_path (str): Path to the file to upload.
            server_url (str): URL of the tracker server.
            save_directory (str): Directory to save the generated .torrent file.
    """
    file_name = os.path.basename(file_path)
    file_type = file_name.split('.')[-1]
    
    # Step 1: Check if the file exists on the tracker
    check_file_exists(server_url, file_name, file_type, token)

    # Step 2: Split the file into chunks
    total_chunks, chunk_hashes = split_file_into_chunks(file_path, 20 * 1024 * 1024, chunks_directory)

    # Step 3: Send file metadata to the tracker
    if add_file_to_tracker(server_url, file_name, file_type, total_chunks, token):
        print("File metadata uploaded to the tracker successfully.")
        
        # Step 4: Create a .torrent file
        metadata = {
            "name": file_name,
            "type": file_type,
            "total_chunks": total_chunks
        }
        create_torrent(file_path, metadata, chunk_hashes, torrents_directory, server_url)
        print(f"Torrent file created and saved in {torrents_directory}.")
    else:
        print("File upload failed.")

def verify_final_file(file_path, pieces):
    """
    Verify the final merged file's integrity by comparing its SHA-1 hash with the provided pieces.
    
    Args:
        file_path (str): Path to the merged file.
        pieces (bytes): Concatenated SHA-1 hashes from the .torrent file.
    
    Returns:
        bool: True if the final file's hash matches, False otherwise.
    """
    sha1 = hashlib.sha1()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    
    return sha1.digest() == pieces

def is_busy(server_url, email, is_busy, token):
    payload = {
        "email": email,
        "is_busy": is_busy,
    }
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{server_url}/peer/update_status", json=payload, headers=headers)
        return response  # Return the server's response directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def download_chunks_from_peers(chunk_peers, file_name, save_dir, private_key, public_key, server_url, token):
    """
    Downloads all chunks from peers using a limited number of threads.

    Args:
        chunk_peers (list): List of chunk dictionaries with 'chunk' and 'peers' keys.
        file_name (str): Name of the file to download.
        save_dir (str): Directory to save the downloaded chunks.

    Returns:
        None
    """
    global download_progress
    download_progress = 0
    chunk_lock = Lock()  # To ensure threads don't access the same chunk simultaneously
    progress_lock = Lock()
    total_download = 0
    next_chunk_index = 0  # Tracks the next chunk to download
    total_chunks = len(chunk_peers)
    stack = []
    def download_from_peer(peer, peer_index):
        nonlocal next_chunk_index
        nonlocal total_download
        while True:
            with chunk_lock:
                if next_chunk_index >= total_chunks and not stack:
                    # No more chunks to download
                    break
                elif  next_chunk_index < total_chunks:
                    chunk_data = chunk_peers[next_chunk_index]
                    next_chunk_index += 1
                else:
                    chunk_number = stack.pop()
                    chunk_data = chunk_peers[chunk_number]


            chunk_index = chunk_data["chunk"]
            chunk_name = f"{file_name}_chunk_{chunk_index}.zip"

            try:
                print(f"Thread {peer_index}: Connecting to {peer['ip']}:{peer['port']} to download chunk {chunk_index}")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((peer["ip"], peer["port"]))
                    
                    # Send request with public key
                    public_key_b64 = base64.b64encode(public_key).decode('utf-8')
                    client.sendall(f"GET {chunk_name} {public_key_b64}".encode())

                    # Read encrypted key size and data
                    encrypted_key_size = int.from_bytes(client.recv(4), "big")
                    encrypted_key = client.recv(encrypted_key_size)
                    
                    # Receive the chunk data
                    encrypted_data  = b""
                    while True:
                        data = client.recv(1024)
                        if not data:
                            break
                        encrypted_data  += data
                # Decrypt AES key using RSA private key
                decrypted_chunk = decrypt_data_with_private_key(private_key, encrypted_key, encrypted_data)

                # Save the downloaded chunk
                chunk_path = os.path.join(save_dir, chunk_name)
                with open(chunk_path, "wb") as f:
                    f.write(decrypted_chunk)
                with progress_lock:
                    total_download += 1
                    download_progress = (total_download / total_chunks) * 100
                    print(f"download_progress: *************{download_progress}")
                    socketio.emit('download_progress', {'progress': download_progress, 'name': file_name})
                print(f"Thread {peer_index}: Finished downloading chunk {chunk_index} from {peer['ip']}:{peer['port']}")
            except Exception as e:
                is_busy(server_url, peer["email"], False, token)
                with chunk_lock:
                    stack.append(chunk_index)
                print(f"Thread {peer_index}: Error downloading chunk {chunk_index} from {peer['ip']}:{peer['port']} - {e}")
                break
        is_busy(server_url, peer["email"], False, token)

    # Get the list of unique peers
    unique_peers = {f"{peer['ip']}:{peer['port']}": peer for chunk in chunk_peers for peer in chunk["peers"]}.values()

    # Limit the number of threads to 5
    max_threads = min(5, len(unique_peers))
    limited_peers = list(unique_peers)[:max_threads]
    print(f"limited_peers: {limited_peers} ")
    if not limited_peers:
        print("No peers are available for downloading chunks.")
        return False
    
    # Create and start threads
    threads = []
    for i, peer in enumerate(limited_peers):
        thread = Thread(target=download_from_peer, args=(peer, i))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All chunks have been downloaded.")
    return True



def merge_chunks_to_file(output_file_path, file_name, total_chunks, peer_directory):
    """
    Merge the split chunks back into a single file after extracting them from ZIPs.

    Args:
        output_file_path (str): Path to save the merged output file.
        file_name (str): Base name of the original file (used for chunk names).
        total_chunks (int): Total number of chunks to merge.
        peer_directory (str): Directory where the zipped chunks are stored.

    Returns:
        None
    """
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'wb') as output_file:
        for i in range(total_chunks):
            # Define the path to the ZIP file for the current chunk
            zip_filename = os.path.join(peer_directory, f"{file_name}_chunk_{i}.zip")
            
            if not os.path.exists(zip_filename):
                print(f"Chunk {i} not found: {zip_filename}")
                continue

            with zipfile.ZipFile(zip_filename, 'r') as zipf:
                # Assume each ZIP contains a single file and extract it
                extracted_files = zipf.namelist()
                if len(extracted_files) != 1:
                    raise ValueError(f"Unexpected files in ZIP: {zip_filename}")
                
                chunk_filename_in_zip = extracted_files[0]

                # Extract the chunk to a temporary directory
                zipf.extract(chunk_filename_in_zip, peer_directory)
                extracted_chunk_path = os.path.join(peer_directory, chunk_filename_in_zip)
                
                # Read and append the chunk's content to the output file
                with open(extracted_chunk_path, 'rb') as chunk_file:
                    output_file.write(chunk_file.read())

                # Delete the extracted chunk after merging
                os.remove(extracted_chunk_path)
                print(f"Chunk {i} merged successfully from {zip_filename}")

    print(f"Merged file created: {output_file_path}")

def handle_file_download(torrent_path, server_url, token, chunks_directory, torrents_directory, private_key, public_key):
    """
    Handles the process of downloading a file using a .torrent file.

    Args:
        torrent_path (str): Path to the .torrent file.
        server_url (str): URL of the tracker server.
        token (str): JWT token for authentication.
        chunks_directory (str): Directory to save chunks.
        torrents_directory (str): Directory to save the merged file.
        private_key (ECC.EccKey): Private key for key exchange.
        public_key (str): Public key for key exchange.
    """
    # Read the .torrent file
    with open(torrent_path, 'rb') as f:
        torrent_info = bencodepy.decode(f.read())

    # Convert byte strings to regular strings recursively
    def decode_dict(d):
        if isinstance(d, dict):
            return {k.decode('utf-8') if isinstance(k, bytes) else k: decode_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [decode_dict(i) for i in d]
        elif isinstance(d, bytes):
            try:
                return d.decode('utf-8')
            except UnicodeDecodeError:
                return d
        else:
            return d

    torrent_info = decode_dict(torrent_info)
    
    file_name = torrent_info['info']['name']
    file_type = torrent_info['info']['type']
    pieces = torrent_info['info']['pieces']  # Concatenated SHA-1 hashes
    total_chunks = torrent_info['info']['total_chunks']
    
    # Request peers from the tracker
    response = requests.post(
        f"{server_url}/file/get_peers",
        json={"name": file_name, "type": file_type},
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        print(f"Failed to get peers: {response.status_code} - {response.text}")
        return
    
    chunks_with_peers = response.json()["peers"]
    if not chunks_with_peers:
        print("No available peers for the requested file.")
        return
    
    print(f"Found {len(chunks_with_peers)} peers for download.")

    # Download chunks in parallel
    if not download_chunks_from_peers(chunks_with_peers, file_name, chunks_directory, private_key, public_key, server_url, token):
        print("Some chunks failed to download. Aborting.")
        return

    # Merge the downloaded chunks
    output_file_path = os.path.join(torrents_directory, f"{file_name}")
    merge_chunks_to_file(output_file_path, file_name, total_chunks, chunks_directory)
    chunks = [i for i in range(0, total_chunks)]
    payload = {"file_name": file_name, "type": file_type, "chunks": chunks}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{server_url}/file/update_chunks", json=payload, headers=headers)
        if response.status_code == 200:
            pass
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            raise HTTPException(status_code=response.status_code, detail="Unexpected error from tracker.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    # Verify the final merged file
    if verify_final_file(output_file_path, pieces):
        print(f"File download and merge completed successfully: {output_file_path}")
    else:
        print("Final file verification failed. The downloaded file may be corrupted.")


def handle_file_download_from_select(file_name, type, server_url, token, chunks_directory, torrents_directory, private_key, public_key):
    """
    Handles the process of downloading a file using a .torrent file.

    Args:
        torrent_path (str): Path to the .torrent file.
        server_url (str): URL of the tracker server.
        token (str): JWT token for authentication.
        chunks_directory (str): Directory to save chunks.
        torrents_directory (str): Directory to save the merged file.
        private_key (ECC.EccKey): Private key for key exchange.
        public_key (str): Public key for key exchange.
    """
    
    # Request file from the tracker
    response = requests.post(
        f"{server_url}/file/get_file",
        json={"name": file_name, "type": type},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code != 200:
        print(f"Failed to get file: {response.status_code} - {response.text}")
        return
    
    total_chunks = response.json()["total_chunks"]
    
    # Request peers from the tracker
    response = requests.post(
        f"{server_url}/file/get_peers",
        json={"name": file_name, "type": type},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code != 200:
        print(f"Failed to get peers: {response.status_code} - {response.text}")
        return
    
    chunks_with_peers = response.json()["peers"]
    if not chunks_with_peers:
        print("No available peers for the requested file.")
        return
    
    print(f"Found {len(chunks_with_peers)} peers for download.")

    # Download chunks in parallel
    if not download_chunks_from_peers(chunks_with_peers, file_name, chunks_directory, private_key, public_key, server_url, token):
        print("Some chunks failed to download. Aborting.")
        return

    # Merge the downloaded chunks
    output_file_path = os.path.join(torrents_directory, f"{file_name}")
    merge_chunks_to_file(output_file_path, file_name, total_chunks, chunks_directory)
    chunks = [i for i in range(0, total_chunks)]
    payload = {"file_name": file_name, "type": type, "chunks": chunks}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{server_url}/file/update_chunks", json=payload, headers=headers)
        if response.status_code == 200:
            pass
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            raise HTTPException(status_code=response.status_code, detail="Unexpected error from tracker.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    print(f"File download and merge completed successfully: {output_file_path}")


def get_files_summary(server_url):
    # Request peers from the tracker
    return requests.get(
        f"{server_url}/file/files_summary"
    )