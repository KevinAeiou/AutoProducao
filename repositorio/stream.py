from modelos.logger import MeuLogger
from repositorio.firebaseDatabase import FirebaseDatabase
from time import time
from firebase_admin import db
from constantes import STRING_PUT, STRING_PATCH
from requests.exceptions import ConnectionError

class Stream:
    def __init__(self, chave: str, nomeLogger: str, arquivoLogger: str = None):
        self.__erro: str = None
        self.__streamPronta: bool= False
        self.__dadosModificados: list= []
        self.__logger: MeuLogger= MeuLogger(nome= nomeLogger, arquivoLogger= arquivoLogger)
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferencia: db.Reference= meuBanco.reference(chave)
        except Exception as e:
            self.__logger.error(menssagem= f'Erro: {e}')

    @property
    def estaPronto(self) -> bool:
        '''
            Função que verifica se a lista de dados modificados têm pelo menos um item.
            Returns:
                bool: Verdadeiro se pelo menos um dado foi modificado no servidor
        '''
        return len(self.__dadosModificados) != 0
    
    @property
    def streamPronta(self) -> bool:
        '''
            Função que verifca se a stream foi iniciada com sucesso.
            Returns:
                bool: Verdadeiro caso a stream tenha sida aberta.
        '''
        return self.__streamPronta

    def pegaDadosModificados(self) -> list:
        '''
        Retorna a lista de dados modificados no servidor

        Returns:
            list: Lista de dados modificados
        '''
        return self.__dadosModificados
    
    def insereDadosModificados(self, dado):
        '''
        Insere dado a lista __dadosModificados
        '''
        self.__dadosModificados.append(dado)
    
    @property
    def limpaLista(self):
        '''
        Limpa lista de dados modificados
        '''
        self.__dadosModificados.clear()

    @property
    def abreStream(self) -> bool:
        '''
        Retorna o estado de inicialização da stream

        Returns:
            bool: Verdadeiro se a inicialização foi feita com sucesso
        '''
        try:
            self.__inicio= time()
            self.__logger.debug(menssagem= f'Inicio da stream: {self.__inicio}')
            self.__minhaReferencia.listen(self.streamHandler)
            return True
        except ConnectionError as e:
            self.__erro= str(e.errno)
        except Exception as e:
            self.__erro= str(e)
        return False
    
    def streamHandler(self, evento: db.Event):
        if evento.event_type in (STRING_PUT, STRING_PATCH):
            if evento.path == '/':
                self.__streamPronta= True
                diferenca: int= time() - self.__inicio
                minutos: int= int(diferenca // 60)
                segundos: int= int(diferenca % 60)
                self.__logger.debug(menssagem= f'Fim da stream: {minutos}:{segundos}min')

    @property
    def pegaErro(self) -> str:
        '''
        Retorna string com erro encontrado

        Returns:
            str: String com erro
        '''
        return self.__erro