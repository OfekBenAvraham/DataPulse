import os
import socket
import base64

from flask import Flask
from encryption_utils import encrypt_data_with_public_key


app = Flask(__name__)

def start_peer_server(port, chunk_dir):
    """
    Start the peer socket server to handle chunk requests and perform key exchange.
    
    Args:
        port (int): The port for the server to listen on.
        chunk_dir (str): The directory where chunks are stored.
        private_key (ECC.EccKey): The private key for key exchange.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(1) 
    
    while True:
        conn, addr = server.accept() 
        handle_client(conn, addr, chunk_dir) 

def handle_client(conn, addr, chunk_dir):
    """
    Handle incoming client requests for file chunks with key exchange and encryption.

    Args:
        conn (socket.socket): The client connection.
        addr (tuple): The address of the client.
        chunk_dir (str): The directory where chunks are stored.
        private_key (ECC.EccKey): The private key for key exchange.
    """
    try:
        request = conn.recv(1024).decode()

        if request.startswith("GET"):
            chunk_name = request.split()[1]
            key_b64  = request.split()[2]
            public_key = base64.b64decode(key_b64.encode('utf-8'))
            chunk_path = os.path.join(chunk_dir, chunk_name)
            with open(chunk_path, 'rb') as f:
                chunk_data = f.read()
                encrypted_key, encrypted_chunk = encrypt_data_with_public_key(public_key, chunk_data)
            conn.sendall(len(encrypted_key).to_bytes(4, 'big') + encrypted_key)
            conn.sendall(encrypted_chunk)
            print(f"Sent encrypted key and chunk {chunk_name}")
        else:
            conn.sendall(b"ERROR: Invalid request")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()