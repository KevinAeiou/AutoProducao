from constantes import *
from modelos.personagem import Personagem
from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO

from time import time

class RepositorioPersonagem:
    listaPersonagens = []
    def __init__(self):
        self.__erro = None
        self.__tempo = None
        self.__meuBanco = FirebaseDatabase().pegaDataBase()
        self.__dadosModificados: list[Personagem] = []

    def abreStream(self):
        try:
            self.__inicio = time()
            self.__streamPronta = False
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).stream(self.stream_handler,  stream_id='teste2')
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def streamPronta(self):
        return self.__streamPronta
    
    def pegaTempoFinal(self):
        return self.__tempo
    
    def pegaTempo(self):
        return time() - self.__inicio
    
    @property
    def estaPronto(self) -> bool:
        """
        Returns:
            bool: True if my stuff is ready for use
        """
        return len(self.__dadosModificados) != 0
    
    def pegaDadosModificados(self) -> list:
        '''
        Returns:
            list: Lista de personagens modificados
        '''
        return self.__dadosModificados
    
    def limpaLista(self):
        '''
        Limpa lista __dadosModificados
        '''
        self.__dadosModificados.clear()
    
    def stream_handler(self, message):
        print("Lista de personagens foi modificada...")
        if message["event"] in ("put", "patch"):
            if message["path"] == "/":
                self.__fim = time()
                self.__tempo = self.__fim - self.__inicio
                self.__streamPronta = True
                return
            personagem = Personagem()
            if message['data'] is None:
                # Algum personagem foi removido do servidor
                idPersonagemDeletado = message['path'].replace('/','').strip()
                personagem.setId(idPersonagemDeletado)
                self.__dadosModificados.append(personagem)
                return
            # Algum personagem foi modificado/inserido no servidor
            personagem.dicionarioParaObjeto(message['data'])
            self.__dadosModificados.append(personagem)
    
    def pegaTodosPersonagens(self):
        personagens = []
        try:
            todosPersonagens = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).get()
            if todosPersonagens.pyres != None:
                for personagemEncontrado in todosPersonagens.each():
                    personagem = Personagem()
                    personagem.dicionarioParaObjeto(personagemEncontrado.val())
                    personagem.id = personagemEncontrado.key()
                    personagens.append(personagem)
                return personagens
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def inserePersonagem(self, personagem):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.id).set(personagem.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaPersonagem(self, personagem):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.id).update(personagem.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removePersonagem(self, personagem):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.id).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro