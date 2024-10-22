from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from modelos.profissao import Profissao
from constantes import *

class RepositorioProfissao:
    listaProfissoes = []
    def __init__(self, personagem) -> None:
        self.__erro = None
        self.__meuBanco = FirebaseDatabase().pegaDataBase()
        self.__personagem = personagem

    def pegaTodasProfissoes(self):
        profissoes = []
        try:
            todasProfissoes = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_PROFISSAO).get()
            if todasProfissoes.pyres != None:
                for profissaoEncontrado in todasProfissoes.each():
                    profissao = Profissao()
                    profissao.dicionarioParaObjeto(profissaoEncontrado.val())
                    profissao.id = profissaoEncontrado.key()
                    profissao.idPersonagem = self.__personagem.id
                    profissoes.append(profissao)
                profissoes = sorted(profissoes, key = lambda profissao: profissao.experiencia, reverse = True)
                return profissoes
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereProfissao(self, profissao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_PROFISSAO).child(profissao.id).set(profissao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaProfissao(self, profissao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_PROFISSAO).child(profissao.id).update(profissao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeProfissao(self, profissao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_PROFISSAO).child(profissao.id).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def limpaProfissoes(self):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_PROFISSAO).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro