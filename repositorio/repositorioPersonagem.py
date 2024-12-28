from constantes import *
import logging
from modelos.personagem import Personagem
from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO

from time import time

class RepositorioPersonagem:
    def __init__(self):
        logging.basicConfig(level = logging.debug, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__logger = logging.getLogger('repositorioPersonagem')
        self.__erro = None
        self.__meuBanco = FirebaseDatabase().pegaDataBase()
        self.__dadosModificados: list[dict] = []

    def abreStream(self):
        try:
            self.__inicio = time()
            self.__logger.info(f'Tempo de inicio da stream: {self.__inicio}')
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).stream(self.stream_handler,  stream_id='teste2')
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
        if message["event"] in ("put", "patch"):
            if message["path"] == "/":
                self.__logger.info(f'Tempo final da stream pronta: {time() - self.__inicio}')
                return
            listaChaves = message["path"].split("/")
            idPersonagemModificado = listaChaves[1]
            chavePersonagemModificado = None
            novoPersonagem = None
            if len(listaChaves) == 2:
                novoPersonagem = message['data']
            else:
                chavePersonagemModificado = listaChaves[2]
            self.__logger.info(f'Menssagem: ({message})')
            idTrabalhoProducaoModificado = None
            if chavePersonagemModificado == 'Lista_desejo' or chavePersonagemModificado == 'Lista_estoque' or chavePersonagemModificado == 'Lista_profissoes' or chavePersonagemModificado == 'Lista_vendas':
                idTrabalhoProducaoModificado = listaChaves[3]
            dicionarioPersonagemModificado = {'id' : idPersonagemModificado, 'idTrabalhoProducao' : idTrabalhoProducaoModificado,chavePersonagemModificado : message['data'], 'novoPersonagem' : novoPersonagem}
            self.__dadosModificados.append(dicionarioPersonagemModificado)
    
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