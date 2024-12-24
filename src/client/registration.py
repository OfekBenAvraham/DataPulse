import requests
import json

def register_user(server_url, username, password, email):
    payload = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{server_url}/register", json=payload)
        if response.status_code == 200:
            print(f"Registration successful: {response.json()}")
        elif response.status_code == 400:
            print("Registration failed. The username or email might already exist.")
        else:
            print(f"Failed to register. Server returned status code: {response.status_code}")
            print(f"Server response: {response.text}")
    except Exception as e:
        print(f"Error communicating with server: {e}")

if __name__ == "__main__":
    print("Welcome to the registration system!")
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    register_user(server_url, username, password, email)
