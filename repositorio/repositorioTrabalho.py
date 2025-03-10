from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalho import Trabalho
from constantes import *
from time import time
from modelos.logger import MeuLogger
from repositorio.stream import Stream

class RepositorioTrabalho(Stream):
    def __init__(self) -> None:
        super().__init__(chave= CHAVE_LISTA_TRABALHOS, nomeLogger= CHAVE_REPOSITORIO_TRABALHO)
        self.__logger: MeuLogger= MeuLogger(nome= CHAVE_REPOSITORIO_TRABALHO)
        self.__erro: str= None
        self.__meuBanco = FirebaseDatabase().pegaMeuBanco()
    
    def streamHandler(self, message: dict):
        super().streamHandler(menssagem= message)
        if message["event"] in ("put", "patch"):
            if message["path"] == "/":
                return
            trabalho: Trabalho= Trabalho()
            if message['data'] is None:
                # Algum trabalho foi removido do servidor
                caminho: str= message['path']
                idTrabalhoDeletado: str= caminho.replace('/','').strip()
                trabalho.id = idTrabalhoDeletado
                super().insereDadosModificados(dado= trabalho)
                return
            # Algum trabalho foi modificado/inserido no servidor
            trabalho.dicionarioParaObjeto(message['data'])
            super().insereDadosModificados(dado= trabalho)

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
    
    def removeTrabalho(self, trabalho: Trabalho) -> bool:
        try:
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.id).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro