from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoProducao import TrabalhoProducao
from constantes import *

class RepositorioTrabalhoProducao:
    def __init__(self, personagem) -> None:
        self._meuBanco = FirebaseDatabase()._dataBase
        self._personagem = personagem

    def limpaListaProducao(self):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).remove()

    def pegaTodosTrabalhosProducao(self):
        listaTrabalhosProducao = []
        todosTrabalhosProducao = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).get()
        if todosTrabalhosProducao.pyres != None:
            for trabalhoProducaoEncontrado in todosTrabalhosProducao.each():
                if CHAVE_TRABALHO_ID in trabalhoProducaoEncontrado.val():
                    trabalhoProducao = TrabalhoProducao(
                        trabalhoProducaoEncontrado.key(),
                        trabalhoProducaoEncontrado.val()[CHAVE_NOME],
                        trabalhoProducaoEncontrado.val()[CHAVE_NOME_PRODUCAO],
                        trabalhoProducaoEncontrado.val()[CHAVE_ESTADO],
                        trabalhoProducaoEncontrado.val()[CHAVE_EXPERIENCIA],
                        trabalhoProducaoEncontrado.val()[CHAVE_NIVEL],
                        trabalhoProducaoEncontrado.val()[CHAVE_PROFISSAO],
                        trabalhoProducaoEncontrado.val()[CHAVE_RARIDADE],
                        trabalhoProducaoEncontrado.val()[CHAVE_RECORRENCIA],
                        trabalhoProducaoEncontrado.val()[CHAVE_TIPO_LICENCA],
                        trabalhoProducaoEncontrado.val()[CHAVE_TRABALHO_ID])
                    listaTrabalhosProducao.append(trabalhoProducao)
        return listaTrabalhosProducao
    
    def removeTrabalhoProducao(self, trabalhoProducao):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.pegaId()).remove()
    
    def adicionaTrabalhoProducao(self, trabalhoProducao):
        resultado = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).push(trabalhoProducao.__dict__)
        trabalhoProducao.setId(resultado['name'])
        return self.modificaTrabalhoProducao(trabalhoProducao)

    def modificaTrabalhoProducao(self, trabalhoProducao):
        trabalhoProducao = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.pegaId()).update(trabalhoProducao.__dict__)
        return TrabalhoProducao(trabalhoProducao[CHAVE_ID], trabalhoProducao[CHAVE_NOME], trabalhoProducao[CHAVE_NOME_PRODUCAO], trabalhoProducao[CHAVE_ESTADO], trabalhoProducao[CHAVE_EXPERIENCIA], trabalhoProducao[CHAVE_NIVEL], trabalhoProducao[CHAVE_PROFISSAO], trabalhoProducao[CHAVE_RARIDADE], trabalhoProducao[CHAVE_RECORRENCIA], trabalhoProducao[CHAVE_TIPO_LICENCA], trabalhoProducao[CHAVE_TRABALHO_ID])