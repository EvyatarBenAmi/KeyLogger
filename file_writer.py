import os
from encryptor import Encryptor

class FileWriter:
    def __init__(self, computer_name, base_path="logs", key="my-secret-key"):
        """
        אתחול המחלקה FileWriter
        :param computer_name: שם המחשב ממנו מגיעים הלוגים
        :param base_path: ספריית בסיס לשמירת הלוגים
        :param key: מפתח ההצפנה/פענוח
        """
        self.computer_name = computer_name
        self.base_path = base_path
        self.encryptor = Encryptor(key)

    def write(self, text, date, hour):
        """
        כותב טקסט לפייל לוג מתאים
        :param text: הטקסט המוצפן מהקליינט
        :param date: תאריך (YYYY-MM-DD)
        :param hour: שעה (HH)
        """
        # נתיב מלא: logs/<computer_name>/<date>/<hour>.txt
        dir_path = os.path.join(self.base_path, self.computer_name, date)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"{hour}.txt")

        # פענוח הטקסט לפני כתיבה
        decrypted = self.encryptor.decrypt(text)

        # כתיבה לקובץ
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(decrypted + "\n")
