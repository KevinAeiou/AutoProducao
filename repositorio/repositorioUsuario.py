from repositorio.firebaseDatabase import FirebaseDatabase
from constantes import CHAVE_USUARIOS2, CHAVE_PERSONAGENS, CHAVE_REPOSITORIO_USUARIO
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from modelos.logger import MeuLogger
from firebase_admin import db

class RepositorioUsuario:
    def __init__(self):
        self.__logger: MeuLogger= MeuLogger(nome= CHAVE_REPOSITORIO_USUARIO, arquivo_logger= f'{CHAVE_REPOSITORIO_USUARIO}.log')
        self.__erro: str= None
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferencia: db.Reference= meuBanco.reference(CHAVE_USUARIOS2).child(CHAVE_ID_USUARIO).child(CHAVE_PERSONAGENS)
        except Exception as e:
            self.__logger.error(mensagem= f'Erro: {e}')

    def verificaIdPersonagem(self, id: str) -> bool:
        '''
            Função que verifica se o "id" passado por parâmetro pertence ao usuário atual.
            Args:
                id (str): String que contêm o "id" do personagem a ser verificado.
            Returns:
                bool: Verdadeiro caso o "id" esteja na lista do usuário atual.
        '''
        try:
            resultado: dict= self.__minhaReferencia.child(id).get()
            pertence: bool= resultado is not None
            self.__logger.debug(mensagem= f'{id} pertence ao usuário {CHAVE_ID_USUARIO}: {pertence}')
            return pertence
        except Exception as e:
            self.__erro= str(e)
            self.__logger.error(mensagem= f'Erro ao verificar se id de personagem ({id}) pertence ao usuario {CHAVE_ID_USUARIO}')
        return False
    
    @property
    def pegaErro(self):
        return self.__erro