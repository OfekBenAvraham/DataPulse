import socket
import requests
import threading

from peer_handler import start_peer_server

def get_ip():
    try:
        hostname = socket.gethostname() #מקבלת את הHOSTNAME של המחשב
        local_ip = socket.gethostbyname(hostname)#ממיר את שם המחשב (HOSTNAME) לכתובת IP של המחשב
        return local_ip
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return None

def get_available_port():
    #צריך לבדוק שהפורט מתפנה אחרי שעושים יציאה מהמערכת
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #AF_INET=IPV4, SOCK_STREAM=TCP
        #נפתח סוקט זמני כמו נקודת תקשורת שמערכת ההפעלה תשתמש בו כדי להקצות פורט
        s.bind(('', 0))  # בוחרת פורט פנוי
        return s.getsockname()[1]  # לוקח את הפורט מתוך (פורט,כתובתIP)

def login_peer(server_url, password, email, chunk_dir):
    """
    Handles peer login and starts a socket server after successful login.
    
    Args:
        server_url (str): The tracker server URL.
        password (str): The peer's password.
        email (str): The peer's email.
        chunk_dir (str): Directory where chunks are stored.
    
    Returns:
        str: Access token if login is successful, None otherwise.
    """
    peer_ip = get_ip()
    peer_port = get_available_port()
    
    payload = {
        "ip": peer_ip,
        "port": peer_port,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{server_url}/peer/login", json=payload)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"Successfully logged in. Token: {token}")
            peer_thread = threading.Thread(
                target=start_peer_server,
                args=(peer_port, chunk_dir),
                daemon=True  # Ensures thread stops when the main program exits
            )
            peer_thread.start()
            
            return token
        else:
            print(f"Failed to register peer. Server returned status code: {response.status_code}")
            print(f"Server response: {response.text}")
            return None
    except Exception as e:
        print(f"Error sending data to server: {e}")
        return None

    


def logout_peer(server_url, email):
    payload = {"email": email} 
    try:
        response = requests.post(f"{server_url}/peer/logout", json=payload)
        if response.status_code == 200:
            print("Successfully logged out.")
            return "Logout successful"
        else:
            print(f"Failed to log out. Server returned status code: {response.status_code}")
            return f"Logout failed with status code: {response.status_code}"
    except Exception as e:
        print(f"Error sending logout request to server: {e}")
        return e


        
def register_user(server_url, email, password):
    peer_ip = get_ip()
    peer_port = get_available_port()
    payload = {
        "ip": peer_ip,
        "port": peer_port,
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{server_url}/peer/register", json=payload)
        return response  # Return the server's response directly
    except requests.ConnectionError as e:
        print(f"Error: Unable to connect to the server. Details: {e}")
        return None
    except requests.Timeout as e:
        print(f"Error: The request timed out. Details: {e}")
        return None
    except requests.RequestException as e:
        print(f"An error occurred while making the request. Details: {e}")
        return None

