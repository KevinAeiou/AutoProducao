import firebase_admin
from firebase_admin import credentials, db
from modelos.logger import MeuLogger
from typing import Optional, NoReturn
from repositorio.credenciais.firebaseCredenciais import CAMINHO_CERTIFICADO_FIREBASE

class FirebaseDatabase:
    '''
        Classe para gerenciamento da conexão com o Firebase Realtime Database.
    '''
    _instancia: Optional['FirebaseDatabase'] = None

    def __new__(cls):
        '''
            Implementa o padrão Singleton para garantr uma única instância.
        '''
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.__initialize()
        return cls._instancia
    
    def __initialize(self):
        '''
            Inicialização privada para o Singleton.
        '''
        self.__loggerFirebaseDatabase: MeuLogger= MeuLogger(nome= 'firebaseDatabase')
        self.__erro: Optional[Exception] = None
        self.__meuBanco: db= None
        self._initializeFirebase()

    def _initializeFirebase(self) -> NoReturn:
        '''
            Configura a conexão com o Firebase.
        '''
        try:
            cred= credentials.Certificate(CAMINHO_CERTIFICADO_FIREBASE)
            firebase_admin.initialize_app(credential= cred, options= {'databaseURL': 'https://bootwarspear-default-rtdb.firebaseio.com/'})
        except Exception as e:
            self.__loggerFirebaseDatabase.error(menssagem= f'Falha na inicialização do Firebase: {e}')
            self.__erro = e
            raise

    @property
    def banco(self) -> db:
        '''
            Propriedade que retorna a instância do banco de dados.
            Returns:
                firebase_admin.db.Reference: Instância do banco de dados.
            Raises:
                Exception: Se a conexão com o Firebase não estiver disponível.
        '''
        if self.__meuBanco is None:
            try:
                self.__meuBanco = db
                self.__loggerFirebaseDatabase.info(menssagem= f'Conexão com Firebase estabelecida com sucesso.')
                return self.__meuBanco
            except Exception as e:
                self.__loggerFirebaseDatabase.error(menssagem= f'Erro ao obter referência do banco: {e}')
                self.__erro = e
                raise
        return self.__meuBanco
    
    @property
    def pegaErro(self) -> Optional[Exception]:
        '''
            Retorna o último erro registrado.
        '''
        return self.__erro