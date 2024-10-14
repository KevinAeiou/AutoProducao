from repositorio.firebaseDatabase import FirebaseDatabase
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
            todasProfissoes = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_PROFISSAO).get()
            if todasProfissoes.pyres != None:
                for profissaoEncontrado in todasProfissoes.each():
                    profisao = Profissao(
                        profissaoEncontrado.key(),
                        profissaoEncontrado.val()[CHAVE_NOME],
                        profissaoEncontrado.val()[CHAVE_EXPERIENCIA],
                        profissaoEncontrado.val()[CHAVE_PRIORIDADE])
                    profissoes.append(profisao)
                profissoes = sorted(profissoes, key = lambda profissao: profissao.pegaExperiencia(), reverse = True)
                return profissoes
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereProfissao(self, profissao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_PROFISSAO).child(profissao.pegaId()).set(profissao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaProfissao(self, profissao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_PROFISSAO).child(profissao.pegaId()).update(profissao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro