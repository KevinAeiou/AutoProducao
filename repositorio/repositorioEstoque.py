from constantes import *
from modelos.trabalhoEstoque import TrabalhoEstoque
from repositorio.firebaseDatabase import FirebaseDatabase

class RepositorioEstoque:
    def __init__(self, personagem):
        self._meuBanco = FirebaseDatabase()._dataBase
        self._personagem = personagem

    def pegaTodosTrabalhosEstoque(self):
        listaEstoque = []
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
        return listaEstoque
    
    def adicionaTrabalhoEstoque(self, trabalho):
        resultado = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_ESTOQUE).push(trabalho.__dict__)
        trabalho.setId(resultado['name'])
        self.modificaTrabalhoEstoque(trabalho)
    
    def modificaTrabalhoEstoque(self, trabalho):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_ESTOQUE).child(trabalho.pegaId()).update(trabalho.__dict__)