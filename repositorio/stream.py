from modelos.logger import MeuLogger
from repositorio.firebaseDatabase import FirebaseDatabase
from time import time

class Stream:
    def __init__(self, chave: str, nomeLogger: str):
        self.__meuBanco= FirebaseDatabase().pegaMeuBanco()
        self.__erro: str = None
        self.__chave: str= chave
        self.__dadosModificados: list= []
        self.__logger: MeuLogger= MeuLogger(nome= nomeLogger)

    @property
    def estaPronto(self) -> bool:
        '''
            Função que verifica se a lista de dados modificados têm pelo menos um item.
            Returns:
                bool: Verdadeiro se pelo menos um dado foi modificado no servidor
        '''
        return len(self.__dadosModificados) != 0

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

    def abreStream(self) -> bool:
        '''
        Retorna o estado de inicialização da stream

        Returns:
            bool: Verdadeiro se a inicialização foi feita com sucesso
        '''
        try:
            self.__inicio= time()
            self.__logger.info(menssagem= f'Inicio da stream: {self.__inicio}')
            self.__meuBanco.child(self.__chave).stream(self.streamHandler)
            return True
        except Exception as e:
            self.__erro= str(e)
        return False
    
    def streamHandler(self, menssagem: dict):
        if menssagem['event'] in ('put', 'path'):
            if menssagem['path'] == '/':
                diferenca: int= time() - self.__inicio
                minutos: int= int(diferenca // 60)
                segundos: int= int(diferenca % 60)
                self.__logger.info(menssagem= f'Fim da stream: {minutos}:{segundos}min')

    def pegaErro(self) -> str:
        '''
        Retorna string com erro encontrado

        Returns:
            str: String com erro
        '''
        return self.__erro