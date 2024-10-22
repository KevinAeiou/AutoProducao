from constantes import *
from modelos.trabalhoEstoque import TrabalhoEstoque
from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO

class RepositorioEstoque:
    def __init__(self, personagem):
        self._meuBanco = FirebaseDatabase().pegaDataBase()
        self._personagem = personagem
        self.__erro = None

    def pegaTodosTrabalhosEstoque(self):
        listaEstoque = []
        try:
            todosTrabalhosEstoque = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_ESTOQUE).get()
            if todosTrabalhosEstoque.pyres != None:
                for trabalhoEstoqueEncontrado in todosTrabalhosEstoque.each():
                    if CHAVE_PROFISSAO in trabalhoEstoqueEncontrado.val():
                        profissao = trabalhoEstoqueEncontrado.val()[CHAVE_PROFISSAO]
                    else:
                        profissao = ''
                    trabalhoEstoque = TrabalhoEstoque(
                        trabalhoEstoqueEncontrado.key(),
                        trabalhoEstoqueEncontrado.val()[CHAVE_NOME],
                        profissao,
                        trabalhoEstoqueEncontrado.val()[CHAVE_NIVEL],
                        trabalhoEstoqueEncontrado.val()[CHAVE_QUANTIDADE],
                        trabalhoEstoqueEncontrado.val()[CHAVE_RARIDADE],
                        trabalhoEstoqueEncontrado.val()[CHAVE_TRABALHO_ID])
                    listaEstoque.append(trabalhoEstoque)
        except:
            print(f'Erro')
        return listaEstoque
    
    def insereTrabalhoEstoque(self, trabalho):
        try:
            self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_ESTOQUE).child(trabalho.pegaId()).set(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaTrabalhoEstoque(self, trabalho):
        try:
            self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_ESTOQUE).child(trabalho.pegaId()).update(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeTrabalho(self, trabalho):
        try:
            self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_ESTOQUE).child(trabalho.pegaId()).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    
    def pegaErro(self):
        return self.__erro