import os
import requests


class NetworkWriter:
    def __init__(self, server_url="http://127.0.0.1:8000/log", local_save_dir=None):
        """
        server_url: כתובת השרת/מחשב שאתה שולח אליו את הלוגים
        local_save_dir: נתיב מקומי לשמירה של הלוגים גם על המחשב שמקבל את הנתונים
        """
        self.server_url = server_url
        self.local_save_dir = local_save_dir
        if self.local_save_dir:
            os.makedirs(self.local_save_dir, exist_ok=True)

    def write(self, encrypted_log_line: str):
        try:
            # שליחה לשרת
            requests.post(self.server_url, data={"log": encrypted_log_line})

            # שמירה מקומית אם מוגדר נתיב
            if self.local_save_dir:
                timestamp = encrypted_log_line[:5].replace(":", "-")
                filename = f"{timestamp}.txt"
                file_path = os.path.join(self.local_save_dir, filename)
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(f"{encrypted_log_line}\n")
        except Exception as e:
            print(f"⚠️ שגיאה ב־NetworkWriter: {e}")
