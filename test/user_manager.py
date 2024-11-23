# managers/user_manager.py
import os
import json
import re
from cryptography.fernet import Fernet


class UserManager:
    def __init__(self, user_dir):
        self.user_dir = user_dir  # Directory to store user JSON files
        os.makedirs(self.user_dir, exist_ok=True)  # Create the directory if it doesn't exist
        self.key = self._get_or_generate_key()
        self.cipher = Fernet(self.key)

    def _get_or_generate_key(self):
        key_file = "secret.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def _encrypt_password(self, password):
        """Encrypt the password."""
        return self.cipher.encrypt(password.encode()).decode()

    def _decrypt_password(self, encrypted_password):
        """Decrypt the password."""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
    #maybe get rid of this
    def _sanitize_username(self, username):
        """Sanitize the username to create a safe filename."""
        return re.sub(r'[^a-zA-Z0-9_-]', '_', username)

    def _get_user_file_path(self, username):
        """Get the file path for the user's JSON file."""
        sanitized_username = self._sanitize_username(username)
        return os.path.join(self.user_dir, f"{sanitized_username}.json")

    def user_exists(self, username):
        """Check if a user exists."""
        return os.path.exists(self._get_user_file_path(username))

    def read_user(self, username):
        """Read a user's data from their JSON file."""
        file_path = self._get_user_file_path(username)
        if not os.path.exists(file_path):
            return None  # User does not exist

        with open(file_path, "r") as file:
            data = json.load(file)
            # Decrypt the password before returning
            data['password'] = self._decrypt_password(data['password'])
            return data

    def save_user(self, username, password):
        """Save a new user to their own JSON file."""
        if self.user_exists(username):
            raise ValueError("User already exists.")

        encrypted_password = self._encrypt_password(password)
        user_data = {
            "username": username,
            "password": encrypted_password,
            "AOO": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1},
            "VOO": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1},
            "AAI": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1, "Atrial Sensitivity": 2.5, "ARP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12},
            "VVI": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1, "Ventricular Sensitivity": 2.5, "VRP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12},
            "AOOR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            "VOOR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            "AAIR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Atrial Amplitude": 3.5, "Atrial Pulse Width": 1, "Atrial Sensitivity": 2.5, "ARP": 250, "PVARP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            "VVIR": {"Lower Rate Limit": 60, "Upper Rate Limit": 120, "Max Sensor Rate": 175, "Ventricular Amplitude": 3.5, "Ventricular Pulse Width": 1, "Ventricular Sensitivity": 2.5, "VRP": 250, "Hysteresis": 3.0, "Rate Smoothing": 12, "Activity Threshold": 2.5, "Reaction Time": 10, "Response Factor": 8, "Recovery Time": 2},
            # You can add more user-specific data here
        }

        file_path = self._get_user_file_path(username)
        with open(file_path, "w") as file:
            json.dump(user_data, file, indent=4)

    def update_user_data(self, username, data):      
        file_path = self._get_user_file_path(username)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def delete_user(self, username):
        """Delete a user's JSON file."""
        file_path = self._get_user_file_path(username)
        if os.path.exists(file_path):
            os.remove(file_path)

    def read_all_users(self):
        """Read all users' data."""
        users = {}
        for filename in os.listdir(self.user_dir):
            if filename.endswith(".json"):
                username = filename[:-5]  # Remove '.json' extension
                user_data = self.read_user(username)
                if user_data:
                    users[username] = user_data['password']
        return users
