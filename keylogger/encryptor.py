import base64

class Encryptor:
    @staticmethod
    def encrypt(text: str) -> str:
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decrypt(encrypted_text: str) -> str:
        return base64.b64decode(encrypted_text.encode("utf-8")).decode("utf-8")
