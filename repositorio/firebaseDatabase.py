import pyrebase
from repositorio.credenciais.firebaseCredenciais import config

class FirebaseDatabase:
    def __init__(self):
        self._dataBase = pyrebase.initialize_app(config).database()
        