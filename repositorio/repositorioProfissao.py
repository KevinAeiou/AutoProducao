from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.profissao import Profissao
from constantes import *

class RepositorioProfissao:
    listaProfissoes = []
    def __init__(self, personagem) -> None:
        self._meuBanco = FirebaseDatabase()._dataBase
        self._personagem = personagem

    def pegaTodasProfissoes(self):
        todasProfissoes = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_PROFISSAO).get()
        if todasProfissoes.pyres != None:
            for profissaoEncontrado in todasProfissoes.each():
                profisao = Profissao(
                    profissaoEncontrado.key(),
                    profissaoEncontrado.val()[CHAVE_NOME],
                    profissaoEncontrado.val()[CHAVE_EXPERIENCIA],
                    profissaoEncontrado.val()[CHAVE_PRIORIDADE])
                self.listaProfissoes.append(profisao)
            self.listaProfissoes = sorted(self.listaProfissoes, key = lambda profissao: profissao.pegaExperiencia(), reverse = True)
        return self.listaProfissoes
    
    def modificaProfissao(self, profissao):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_PROFISSAO).child(profissao.pegaId()).update(profissao.__dict__)
    
    def mostraListaProfissoes(self):
        for profissao in self.listaProfissoes:
            print(profissao)