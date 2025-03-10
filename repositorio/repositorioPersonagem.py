from constantes import *
import logging
from modelos.personagem import Personagem
from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from requests.exceptions import HTTPError
from repositorio.stream import Stream

from time import time

class RepositorioPersonagem(Stream):
    def __init__(self):
        super().__init__(chave=CHAVE_PERSONAGENS, nomeLogger= 'repositorioPersonagem')
        logging.basicConfig(level = logging.debug, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
        self.__logger = logging.getLogger('repositorioPersonagem')
        self.__erro = None
        self.__meuBanco = FirebaseDatabase().pegaMeuBanco()
    
    def streamHandler(self, menssagem: dict):
        super().streamHandler(menssagem= menssagem)
        if menssagem["event"] in ("put", "patch"):
            if menssagem["path"] == "/":
                return
            personagem: Personagem= Personagem()
            if menssagem['data'] is None:
                caminho: str= menssagem['path']
                idPersonagemDeletado: str= caminho.replace('/', '').strip()
                personagem.id= idPersonagemDeletado
                super().insereDadosModificados(dado= personagem)
            personagem.dicionarioParaObjeto(dicionario= menssagem['data'])
            super().insereDadosModificados(dado= personagem)
    
    def pegaTodosPersonagens(self) -> list[Personagem] | None:
        personagens: list[Personagem]= []
        try:
            idPersonagensEncontrados = self.__meuBanco.child(CHAVE_USUARIOS2).child(CHAVE_ID_USUARIO).child(CHAVE_PERSONAGENS).get()
            if idPersonagensEncontrados.pyres == None:
                return personagens
            for idPersonagemEncontrado in idPersonagensEncontrados.each():
                idPersonagemEncontradoKey = idPersonagemEncontrado.key()
                resultadoPersonagem= self.__meuBanco.child(CHAVE_PERSONAGENS).order_by_key().equal_to(idPersonagemEncontradoKey).get()
                if len(resultadoPersonagem.pyres) == 0:
                    continue
                for personagemEncontrado in resultadoPersonagem:
                    personagem = Personagem()
                    personagem.dicionarioParaObjeto(personagemEncontrado.val())
                    break
                personagens.append(personagem)
            return personagens
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def inserePersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__meuBanco.child(CHAVE_USUARIOS2).child(CHAVE_ID_USUARIO).child(CHAVE_PERSONAGENS).update({personagem.id: True})
            self.__meuBanco.child(CHAVE_PERSONAGENS).child(personagem.id).set(personagem.__dict__)
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaPersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__meuBanco.child(CHAVE_PERSONAGENS).child(personagem.id).update(personagem.__dict__)
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removePersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__meuBanco.child(CHAVE_PERSONAGENS).child(personagem.id).remove()
            self.__meuBanco.child(CHAVE_USUARIOS2).child(CHAVE_ID_USUARIO).child(CHAVE_PERSONAGENS).child(personagem.id).remove()
            self.__meuBanco.child(CHAVE_PROFISSOES).child(personagem.id).remove()
            self.__meuBanco.child(CHAVE_PRODUCAO).child(personagem.id).remove()
            self.__meuBanco.child(CHAVE_ESTOQUE).child(personagem.id).remove()
            self.__meuBanco.child(CHAVE_VENDAS).child(personagem.id).remove()
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro