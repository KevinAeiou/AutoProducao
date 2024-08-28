from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalho import Trabalho
from constantes import *

class RepositorioTrabalho:
    def __init__(self) -> None:
        self._meuBanco = FirebaseDatabase()._dataBase

    def pegaTodosTrabalhos(self):
        listaTrabalhos = []
        todosTrabalhos = self._meuBanco.child(CHAVE_LISTA_TRABALHOS).get()
        for trabalhoEncontrado in todosTrabalhos.each():
            if CHAVE_EXPERIENCIA in trabalhoEncontrado.val():
                trabalho = Trabalho(
                    trabalhoEncontrado.key(),
                    trabalhoEncontrado.val()[CHAVE_NOME],
                    trabalhoEncontrado.val()[CHAVE_NOME_PRODUCAO],
                    trabalhoEncontrado.val()[CHAVE_EXPERIENCIA],
                    trabalhoEncontrado.val()[CHAVE_NIVEL],
                    trabalhoEncontrado.val()[CHAVE_PROFISSAO],
                    trabalhoEncontrado.val()[CHAVE_RARIDADE]
                )
                listaTrabalhos.append(trabalho)
        return listaTrabalhos