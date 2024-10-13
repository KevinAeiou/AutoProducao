import pyrebase
from repositorio.credenciais.firebaseCredenciais import config

class FirebaseDatabase:
    def __init__(self):
        self.__dataBase = pyrebase.initialize_app(config).database()
        
    def pegaDataBase(self):
        return self.__dataBase