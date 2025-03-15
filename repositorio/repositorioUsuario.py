from pyrebase.pyrebase import Database
from repositorio.firebaseDatabase import FirebaseDatabase
from constantes import CHAVE_USUARIOS2, CHAVE_PERSONAGENS, CHAVE_REPOSITORIO_USUARIO
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from modelos.logger import MeuLogger

class RepositorioUsuario:
    def __init__(self):
        self.__logger: MeuLogger= MeuLogger(nome= CHAVE_REPOSITORIO_USUARIO)
        self.__erro: str= None
        self.__meuBanco: Database= FirebaseDatabase().pegaMeuBanco()

    def verificaIdPersonagem(self, id: str) -> bool:
        try:
            resultado = self.__meuBanco.child(CHAVE_USUARIOS2).child(CHAVE_ID_USUARIO).child(CHAVE_PERSONAGENS).child(id).get()
            return resultado.pyres  is not None
        except Exception as e:
            self.__erro= str(e)
            self.__logger.error(menssagem= f'Erro ao verificar se id de personagem ({id}) pertence ao usuario {CHAVE_ID_USUARIO}')
        return False
    
    def pegaErro(self):
        return self.__erro