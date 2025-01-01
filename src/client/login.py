import socket
import requests
import json

def get_ip():
    try:
        hostname = socket.gethostname() #מקבלת את הHOSTNAME של המחשב
        local_ip = socket.gethostbyname(hostname)#ממיר את שם המחשב (HOSTNAME) לכתובת IP של המחשב
        return local_ip
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return None


def send_peer_data_to_server(server_url, ip, port, password, email):
    payload = {
        "ip": ip,
        "port": port,
        "email": email,
        "password": password
    }
    try:
        response = requests.post(server_url, json=payload)
        if response.status_code == 200:
            token = response.json().get("token")
            print(f"Successfully logged in. Token: {token}")
            return token
        else:
            print(f"Failed to register peer. Server returned status code: {response.status_code}")
            print(f"Server response: {response.text}")
            return None
    except Exception as e:
        print(f"Error sending data to server: {e}")
        return None
    

def get_available_port():
    #צריך לבדוק שהפורט מתפנה אחרי שעושים יציאה מהמערכת
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #AF_INET=IPV4, SOCK_STREAM=TCP
        #נפתח סוקט זמני כמו נקודת תקשורת שמערכת ההפעלה תשתמש בו כדי להקצות פורט
        s.bind(('', 0))  # בוחרת פורט פנוי
        return s.getsockname()[1]  # לוקח את הפורט מתוך (פורט,כתובתIP)


def logout_peer(server_url, email):
    payload = {"email": email} 
    try:
        response = requests.post(f"{server_url}/logout", json=payload)
        if response.status_code == 200:
            print("Successfully logged out.")
            token = None  # איפוס ה-TOKEN
            print("Token has been cleared.")
        else:
            print(f"Failed to log out. Server returned status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending logout request to server: {e}")
        return None

if __name__ == "__main__":
    peer_ip = get_ip()
    peer_port = get_available_port()
    print(f"Assigned port: {peer_port}")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    token = send_peer_data_to_server(server_url, peer_ip, peer_port, password, email)
    if token:
        logout_choice = input("Do you want to logout? (yes/no): ")
        if logout_choice.lower() == "yes":
            logout_peer(server_url, email, token)
        else:
            print("Continuing session with token.")
    else:
        print("No token received, cannot logout.")