from pyrebase.pyrebase import Database
import pyrebase
from modelos.logger import MeuLogger
from repositorio.credenciais.firebaseCredenciais import config

class FirebaseDatabase:
    def __init__(self):
        self.__loggerFirebaseDatabase = MeuLogger(nome= 'firebaseDatabase')
        self.__erro = None
        try:
            self.__dataBase: Database= pyrebase.initialize_app(config).database()
        except Exception as e:
            self.__loggerFirebaseDatabase.error(f'Erro ao inicializar: {e}')

    def pegaMeuBanco(self):
        return self.__dataBase
    
    def pegaErro(self):
        return self.__erro