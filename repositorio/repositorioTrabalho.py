from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalho import Trabalho
from constantes import *
from time import time
import logging

class RepositorioTrabalho:
    def __init__(self) -> None:
        logging.basicConfig(level = logging.debug, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__logger = logging.getLogger('repositorioTrabalho')
        self.__erro = None
        self.__meuBanco = FirebaseDatabase().pegaDataBase()
        self.__dadosModificados: list[Trabalho] = []

    def abreStream(self):
        try:
            self.__inicio = time()
            self.__logger.info(f'Tempo de inicio da stream: {self.__inicio}')
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).stream(self.stream_handler)
            return True
        except Exception as e:
            self.__erro = str(e)
            return False

    @property
    def estaPronto(self) -> bool:
        """
        Returns:
            bool: True if my stuff is ready for use
        """
        return len(self.__dadosModificados) != 0
    
    def pegaDadosModificados(self):
        return self.__dadosModificados
    
    def limpaLista(self):
        self.__dadosModificados.clear()
    
    def stream_handler(self, message):
        if message["event"] in ("put", "patch"):
            if message["path"] == "/":
                self.__logger.info(f'Tempo final da stream pronta: {time() - self.__inicio}')
                return
            trabalho = Trabalho()
            if message['data'] is None:
                # Algum trabalho foi removido do servidor
                idTrabalhoDeletado = message['path'].replace('/','').strip()
                trabalho.setId(idTrabalhoDeletado)
                self.__dadosModificados.append(trabalho)
                return
            # Algum trabalho foi modificado/inserido no servidor
            trabalho.dicionarioParaObjeto(message['data'])
            self.__dadosModificados.append(trabalho)

    def pegaTodosTrabalhos(self):
        trabalhos = []
        try:
            todosTrabalhos = self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).get()
            for trabalhoEncontrado in todosTrabalhos.each():
                trabalho = Trabalho()
                trabalho.dicionarioParaObjeto(trabalhoEncontrado.val())
                trabalho.id = trabalhoEncontrado.key()
                trabalhos.append(trabalho)
            return trabalhos
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereTrabalho(self, trabalho):
        try:
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.id).set(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaTrabalho(self, trabalho):
        try:
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.id).update(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeTrabalho(self, trabalho):
        try:
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.id).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro