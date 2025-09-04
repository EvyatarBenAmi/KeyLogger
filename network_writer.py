import requests
import json
from datetime import datetime

class NetworkWriter:
    def __init__(self, server_url="http://127.0.0.1:8000/log", computer_name="PC1"):
        self.server_url = server_url
        self.computer_name = computer_name

    def write(self, encrypted_log_line: str):
        try:
            payload = {
                "computer": self.computer_name,
                "log": encrypted_log_line,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            headers = {"Content-Type": "application/json"}
            requests.post(self.server_url, data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(f"⚠️ שגיאה בשליחה לשרת: {e}")
