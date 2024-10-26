import pyrebase
import logging
from repositorio.credenciais.firebaseCredenciais import config

class FirebaseDatabase:
    def __init__(self):
        logging.basicConfig(level = logging.debug, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__loggerFirebaseDatabase = logging.getLogger('firebaseDatabase')
        self.__erro = None
        try:
            self.__dataBase = pyrebase.initialize_app(config).database()
        except Exception as e:
            self.__loggerFirebaseDatabase.error(f'Erro ao inicializar: {e}')

    def pegaDataBase(self):
        return self.__dataBase
    
    def pegaErro(self):
        return self.__erro