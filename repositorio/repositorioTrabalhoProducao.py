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
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).remove()
        except:
            print(f'Erro')

    def pegaTodosTrabalhosProducao(self):
        trabalhosProducao = []
        try:
            todosTrabalhosProducao = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).get()
            if todosTrabalhosProducao.pyres != None:
                for trabalhoProducaoEncontrado in todosTrabalhosProducao.each():
                    if CHAVE_TRABALHO_NECESSARIO in trabalhoProducaoEncontrado.val():
                        trabalhoNecessario = trabalhoProducaoEncontrado.val()[CHAVE_TRABALHO_NECESSARIO]
                    else:
                        trabalhoNecessario = ''
                    if CHAVE_TRABALHO_ID in trabalhoProducaoEncontrado.val():
                        trabalhoId = trabalhoProducaoEncontrado.val()[CHAVE_TRABALHO_ID]
                    else:
                        trabalhoId = ''
                    if  CHAVE_NOME_PRODUCAO in trabalhoProducaoEncontrado.val():
                        trabalhoProducao = TrabalhoProducao(trabalhoProducaoEncontrado.key(), trabalhoId, trabalhoProducaoEncontrado.val()[CHAVE_NOME], trabalhoProducaoEncontrado.val()[CHAVE_NOME_PRODUCAO], trabalhoProducaoEncontrado.val()[CHAVE_EXPERIENCIA], trabalhoProducaoEncontrado.val()[CHAVE_NIVEL], trabalhoProducaoEncontrado.val()[CHAVE_PROFISSAO], trabalhoProducaoEncontrado.val()[CHAVE_RARIDADE], trabalhoNecessario, trabalhoProducaoEncontrado.val()[CHAVE_RECORRENCIA], trabalhoProducaoEncontrado.val()[CHAVE_TIPO_LICENCA], trabalhoProducaoEncontrado.val()[CHAVE_ESTADO])
                        trabalhosProducao.append(trabalhoProducao)
            trabalhosProducao = sorted(trabalhosProducao, key=lambda trabalhoProducao: trabalhoProducao.pegaEstado(), reverse=True)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        return None

    
    def removeTrabalhoProducao(self, trabalhoProducao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.pegaId()).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def insereTrabalhoProducao(self, trabalhoProducao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.pegaId()).set(trabalhoProducao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaTrabalhoProducao(self, trabalhoProducao):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self._personagem.pegaId()).child(CHAVE_LISTA_TRABALHOS_PRODUCAO).child(trabalhoProducao.pegaId()).update(trabalhoProducao.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro