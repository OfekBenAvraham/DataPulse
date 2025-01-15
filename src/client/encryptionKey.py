import json

def save_encryption_key_to_config(encryption_key, config_file_path='config.json'):
    """Save the encryption key to a config file."""
    key_hex = encryption_key.hex()
    config_data = {
        'encryption_key': key_hex
    }
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file)

    print(f"Encryption key saved to config file: {config_file_path}")


def load_encryption_key_from_config(config_file_path='config.json'):
    """Load the encryption key from the config file."""
    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)
        encryption_key = bytes.fromhex(config_data['encryption_key'])
    return encryption_key