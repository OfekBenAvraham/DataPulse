import os
import signal
import threading
import time

from auth import register_user, login_peer, logout_peer
from app_init import app, socketio
from flask import Flask, Response, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

from key_exchange import generate_rsa_key_pair

from concurrent.futures import ThreadPoolExecutor

from file_handler import handle_file_upload, handle_file_download, get_files_summary, handle_file_download_from_select, download_progress


# Create a global ThreadPoolExecutor instance
executor = ThreadPoolExecutor()

@app.teardown_appcontext
def cleanup_resources(_):
    """
    Clean up resources (e.g., ThreadPoolExecutor) during Flask app shutdown.
    """
    print("Shutting down resources...")
    executor.shutdown(wait=True)
    print("Executor shut down.")
    
# Global variables for key management
private_key, public_key = generate_rsa_key_pair()

BASE_DIRECTORY_CHUNKS = os.path.join(os.getcwd(), "Peers", "Chunks")
BASE_DIRECTORY_Torrents = os.path.join(os.getcwd(), "Peers", "Torrents")

os.makedirs(BASE_DIRECTORY_CHUNKS, exist_ok=True)
os.makedirs(BASE_DIRECTORY_Torrents, exist_ok=True)

peer_server_port = None
peer_token = None
userEmail = None
server_url = 'http://127.0.0.1:8000'
FLASK_PORT = 8001
# Peer Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    token = login_peer(server_url, data['password'], data['email'], BASE_DIRECTORY_CHUNKS)
    if token:
        global userEmail
        global peer_token
        userEmail = data['email']
        peer_token = token
        return jsonify({"token": token})
    return jsonify("Login failed"), 401

# Peer Logout Endpoint
@app.route('/logout', methods=['POST'])
def logout():
    # data = request.json
    result = logout_peer(server_url, userEmail)
    if isinstance(result, str):
        # If `logout_peer` returns a string, assume success
        return jsonify({"message": result}), 200
    elif isinstance(result, Exception):
        # If an exception occurred, return an error response
        return jsonify({"error": str(result)}), 500
    else:
        # Handle unexpected cases
        return jsonify({"error": "Failed to logout"}), 400
    
# User Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response = register_user(server_url, data['email'], data['password'])

    if response.status_code == 200:
        print(f"Registration successful")
        return jsonify({"message": "Registration successful"}), 200
    elif response.status_code == 400:
        print("Registration failed. The username or email might already exist.")
        return jsonify({"error": "Registration failed. The username or email already exist"}), 400
    else:
        print("Unexpected error occurred.")
        return jsonify({"error": "Failed to register"}), 401


# File Upload Endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.json.get('file_path')
    handle_file_upload(file_path, server_url, peer_token, BASE_DIRECTORY_CHUNKS, BASE_DIRECTORY_Torrents)
    return jsonify("File uploaded successfully"), 200

# File Download Endpoint
@app.route('/download', methods=['POST'])
def download_file():
    torrent_path = request.json.get('torrent_path')
    handle_file_download(torrent_path, server_url, peer_token, BASE_DIRECTORY_CHUNKS, BASE_DIRECTORY_Torrents, private_key, public_key)
    return jsonify("File download completed"), 200

# File Download Endpoint
@app.route('/download_from_select', methods=['POST'])
def download_file_from_select():
    name = request.json.get('name')
    type = request.json.get('type')
    if peer_token == None:
        return jsonify({"error": "You must to login before downloading."}), 404
    handle_file_download_from_select(name, type, server_url, peer_token, BASE_DIRECTORY_CHUNKS, BASE_DIRECTORY_Torrents, private_key, public_key)
    return jsonify({"message": "File download completed"}), 200

@app.route('/get_progress', methods=['GET'])
def get_progress():
    return download_progress, 200

    
@app.route('/files_summary', methods=['GET'])
def files_summary():
    """
    Endpoint to fetch file summaries from the tracker and return them to the client.
    """
    response = get_files_summary(server_url)
    # Check if the tracker request was successful
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch files summary", "details": response.text}), response.status_code

    # Return the JSON response from the tracker
    return response.json(), 200

def graceful_shutdown(signal, frame):
    """
    Handle graceful shutdown of the server.
    """
    print("\nShutting down server...")
    os._exit(0)  # Forcefully terminate all threads

def start_flask_server():
    """
    Start the Flask API server.
    """
    print(f"Starting Flask server on port {FLASK_PORT}...")
    socketio.run(app, host="0.0.0.0", port=8001)

    app.run(app, host="0.0.0.0", port=FLASK_PORT)


@socketio.on('connect')
def on_connect():
    print('Client connected!')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected!')

    
def main():
    """
    Main function to initialize the system.
    """
    # Start Flask Server
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    start_flask_server()
    # flask_thread = threading.Thread(target=start_flask_server, daemon=False)
    # flask_thread.start()
    # print(f"Flask server started on port {FLASK_PORT}. Waiting for peer server requests...")
    
if __name__ == "__main__":
    main()
