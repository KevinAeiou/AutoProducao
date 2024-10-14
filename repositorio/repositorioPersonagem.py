from constantes import *
from modelos.personagem import Personagem
from repositorio.firebaseDatabase import FirebaseDatabase

class RepositorioPersonagem:
    listaPersonagens = []
    def __init__(self):
        self.__erro = None
        self.__meuBanco = FirebaseDatabase()._dataBase
        self.listaPersonagens = self.pegaTodosPersonagens()
    
    def pegaTodosPersonagens(self):
        listaPersonagens = []
        try:
            todosPersonagens = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).get()
            if todosPersonagens.pyres != None:
                for personagemEncontrado in todosPersonagens.each():
                    if CHAVE_AUTO_PRODUCAO in personagemEncontrado.val():
                        personagem = Personagem(
                            personagemEncontrado.key(),
                            personagemEncontrado.val()[CHAVE_NOME],
                            personagemEncontrado.val()[CHAVE_EMAIL],
                            personagemEncontrado.val()[CHAVE_SENHA],
                            personagemEncontrado.val()[CHAVE_ESPACO_PRODUCAO],
                            personagemEncontrado.val()[CHAVE_ESTADO],
                            personagemEncontrado.val()[CHAVE_USO],
                            personagemEncontrado.val()[CHAVE_AUTO_PRODUCAO])
                    else:
                        if self.modificaPersonagem(personagem = Personagem(
                            personagemEncontrado.key(),
                            personagemEncontrado.val()[CHAVE_NOME],
                            personagemEncontrado.val()[CHAVE_EMAIL],
                            personagemEncontrado.val()[CHAVE_SENHA],
                            personagemEncontrado.val()[CHAVE_ESPACO_PRODUCAO],
                            personagemEncontrado.val()[CHAVE_ESTADO],
                            personagemEncontrado.val()[CHAVE_USO],
                            False)):
                            print(f'CHAVE autoProducao inserida com sucesso!')
                        else:
                            print(f'Erro ao inserir chave autoProducao: {self.pegaErro()}')
                    listaPersonagens.append(personagem)
        except Exception as e:
            self.__erro = str(e)
        return listaPersonagens
    
    def inserePersonagem(self, personagem):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.pegaId()).set(personagem.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaPersonagem(self, personagem):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.pegaId()).update(personagem.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removePersonagem(self, personagem):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.pegaId()).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro