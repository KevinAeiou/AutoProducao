from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoVendido import TrabalhoVendido
from constantes import *

class RepositorioVendas:
    __meuBanco = None
    def __init__(self, personagem) -> None:
        self.__erro = None
        self.__personagem = personagem
        self.__meuBanco = FirebaseDatabase().pegaDataBase()

    def pegaTodasVendas(self):
        listaVendas = []
        try:
            todasVendas = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_VENDAS).get()
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
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereTrabalhoVendido(self, trabalhoVendido):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_VENDAS).child(trabalhoVendido.pegaId()).set(trabalhoVendido.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaVenda(self, venda):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_VENDAS).child(venda.pegaId()).update(venda.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
        
    def removeVenda(self, venda):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_VENDAS).child(venda.pegaId()).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
        
    def limpaListaVenda(self):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.pegaId()).child(CHAVE_LISTA_VENDAS).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro