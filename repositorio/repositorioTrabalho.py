from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalho import Trabalho
from constantes import *

class RepositorioTrabalho:
    def __init__(self) -> None:
        self.__erro = None
        self._meuBanco = FirebaseDatabase()._dataBase

    def pegaTodosTrabalhos(self):
        listaTrabalhos = []
        try:
            todosTrabalhos = self._meuBanco.child(CHAVE_LISTA_TRABALHOS).get()
            for trabalhoEncontrado in todosTrabalhos.each():
                if CHAVE_EXPERIENCIA in trabalhoEncontrado.val():
                    if not CHAVE_TRABALHO_NECESSARIO in trabalhoEncontrado.val():
                        trataNecessario = ''
                    else:
                        trataNecessario = trabalhoEncontrado.val()[CHAVE_TRABALHO_NECESSARIO]
                    trabalho = Trabalho(
                        trabalhoEncontrado.key(),
                        trabalhoEncontrado.val()[CHAVE_NOME],
                        trabalhoEncontrado.val()[CHAVE_NOME_PRODUCAO],
                        trabalhoEncontrado.val()[CHAVE_EXPERIENCIA],
                        trabalhoEncontrado.val()[CHAVE_NIVEL],
                        trabalhoEncontrado.val()[CHAVE_PROFISSAO],
                        trabalhoEncontrado.val()[CHAVE_RARIDADE],
                        trataNecessario)
                    listaTrabalhos.append(trabalho)
        except:
            print(f'Erro')
        return listaTrabalhos
    
    def insereTrabalho(self, trabalho):
        try:
            self._meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.pegaId()).set(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaTrabalho(self, trabalho):
        try:
            self._meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.pegaId()).update(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeTrabalho(self, trabalho):
        try:
            self._meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.pegaId()).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro