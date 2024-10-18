from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoProducao import TrabalhoProducao
from constantes import *

class RepositorioTrabalhoProducao:
    def __init__(self, personagem) -> None:
        self.__erro = None
        self.__meuBanco = FirebaseDatabase().pegaDataBase()
        self._personagem = personagem

    def limpaListaProducao(self):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.id).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).remove()
        except:
            print(f'Erro')

    def pegaTodosTrabalhosProducao(self):
        trabalhosProducao = []
        try:
            todosTrabalhosProducao = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.id).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).get()
            if todosTrabalhosProducao.pyres != None:
                for trabalhoProducaoEncontrado in todosTrabalhosProducao.each():
                    trabalhoProducao = TrabalhoProducao()
                    trabalhoProducao.dicionarioParaObjeto(trabalhoProducaoEncontrado.val())
                    trabalhoProducao.id = trabalhoProducaoEncontrado.key()
                    trabalhosProducao.append(trabalhoProducao)
            trabalhosProducao = sorted(trabalhosProducao, key=lambda trabalhoProducao: trabalhoProducao.estado, reverse=True)

            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        return None

    
    def removeTrabalhoProducao(self, trabalhoProducao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.id).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.id).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def insereTrabalhoProducao(self, trabalhoProducao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.id).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.id).set(trabalhoProducao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaTrabalhoProducao(self, trabalhoProducao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.id).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.id).update(trabalhoProducao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro