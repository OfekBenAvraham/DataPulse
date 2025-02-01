from Crypto.PublicKey import RSA

from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES, PKCS1_OAEP

from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16  # AES block size

def encrypt_data_with_public_key(public_key_pem, data):
    # Generate a random AES key
    aes_key = get_random_bytes(32)  # 256-bit AES key
    
    # Encrypt the data with AES
    iv = get_random_bytes(BLOCK_SIZE)
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    encrypted_data = iv + aes_cipher.encrypt(pad(data, BLOCK_SIZE))
    
    # Encrypt the AES key with the RSA public key
    public_key = RSA.import_key(public_key_pem)
    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_key = rsa_cipher.encrypt(aes_key)
    
    # Return the encrypted key and encrypted data
    return encrypted_key, encrypted_data

def decrypt_data_with_private_key(private_key_pem, encrypted_key, encrypted_data):
    """
    Decrypts the encrypted data using the private RSA key and AES decryption.

    Args:
        private_key_pem (bytes): The private RSA key in PEM format.
        encrypted_key (bytes): The AES key encrypted with RSA.
        encrypted_data (bytes): The data encrypted with AES.

    Returns:
        bytes: The decrypted data.
    """
    # Decrypt the AES key using the RSA private key
    private_key = RSA.import_key(private_key_pem)
    rsa_cipher = PKCS1_OAEP.new(private_key)
    aes_key = rsa_cipher.decrypt(encrypted_key)
    
    # Extract the IV from the beginning of the encrypted data
    iv = encrypted_data[:BLOCK_SIZE]
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    
    # Decrypt the data and remove padding
    decrypted_data = unpad(aes_cipher.decrypt(encrypted_data[BLOCK_SIZE:]), BLOCK_SIZE)
    return decrypted_data