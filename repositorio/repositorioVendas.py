from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoVendido import TrabalhoVendido
from constantes import *

class RepositorioVendas:
    _meuBanco = None
    def __init__(self, personagem) -> None:
        self.personagem = personagem
        self._meuBanco = FirebaseDatabase()._dataBase

    def pegaTodosTrabalhoVendidos(self):
        listaVendas = []
        todasVendas = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.personagem.pegaId()).child(CHAVE_LISTA_VENDAS).get()
        if todasVendas.pyres != None:
            for vendaEncontrada in todasVendas.each():
                if CHAVE_TRABALHO_ID in vendaEncontrada.val():
                    trabalhoVendido = TrabalhoVendido(
                        vendaEncontrada.key(),
                        vendaEncontrada.val()[CHAVE_NOME_PRODUTO],
                        vendaEncontrada.val()[CHAVE_DATA_VENDA],
                        vendaEncontrada.val()[CHAVE_NOME_PERSONAGEM],
                        vendaEncontrada.val()[CHAVE_QUANTIDADE_PRODUTO],
                        vendaEncontrada.val()[CHAVE_TRABALHO_ID],
                        vendaEncontrada.val()[CHAVE_VALOR_PRODUTO]
                    )
                    listaVendas.append(trabalhoVendido)
        return listaVendas
    
    def adicionaNovaVenda(self, novaVenda):
        res = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.personagem.pegaId()).child(CHAVE_LISTA_VENDAS).push(novaVenda.__dict__)
        novaVenda.setId(res['name'])
        res = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.personagem.pegaId()).child(CHAVE_LISTA_VENDAS).child(novaVenda.pegaId()).update(novaVenda.__dict__)

    def removeVenda(self, venda):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.personagem.pegaId()).child(CHAVE_LISTA_VENDAS).child(venda.pegaId()).remove()

    def limpaListaVenda(self):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.personagem.pegaId()).child(CHAVE_LISTA_VENDAS).remove()