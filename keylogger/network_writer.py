import requests
from encryptor import Encryptor

class NetworkWriter:
    def __init__(self, server_url="http://127.0.0.1:8000/log"):
        self.server_url = server_url

    def write(self, encrypted_log_line: str):
        try:
            decrypted_log = Encryptor.decrypt(encrypted_log_line)
            requests.post(self.server_url, data={"log": decrypted_log})
        except Exception as e:
            print(f"⚠️ שגיאה בשליחה לשרת: {e}")
