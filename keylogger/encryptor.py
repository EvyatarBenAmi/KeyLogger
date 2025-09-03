from cryptography.fernet import Fernet
import os

class Encryptor:
    KEY_FILE = "key.key"

    @staticmethod
    def load_key():
        """טוען את המפתח מקובץ, או יוצר חדש אם אין."""
        if not os.path.exists(Encryptor.KEY_FILE):
            key = Fernet.generate_key()
            with open(Encryptor.KEY_FILE, "wb") as f:
                f.write(key)
        else:
            with open(Encryptor.KEY_FILE, "rb") as f:
                key = f.read()
        return key

    @staticmethod
    def encrypt(text: str) -> str:
        key = Encryptor.load_key()
        f = Fernet(key)
        token = f.encrypt(text.encode())
        return token.decode()

    @staticmethod
    def decrypt(token: str) -> str:
        key = Encryptor.load_key()
        f = Fernet(key)
        try:
            text = f.decrypt(token.encode())
            return text.decode()
        except:
            # במקרה שהטקסט לא מוצפן
            return token
