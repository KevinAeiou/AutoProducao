from constantes import *
from modelos.personagem import Personagem
from repositorio.firebaseDatabase import FirebaseDatabase

class RepositorioPersonagem:
    listaPersonagens = []
    def __init__(self):
        self._meuBanco = FirebaseDatabase()._dataBase
        self.listaPersonagens = self.pegaTodosPersonagens()
    
    def pegaTodosPersonagens(self):
        listaPersonagens = []
        try:
            todosPersonagens = self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).get()
            if todosPersonagens.pyres != None:
                for personagemEncontrado in todosPersonagens.each():
                    personagem = Personagem(
                        personagemEncontrado.key(),
                        personagemEncontrado.val()[CHAVE_NOME],
                        personagemEncontrado.val()[CHAVE_EMAIL],
                        personagemEncontrado.val()[CHAVE_SENHA],
                        personagemEncontrado.val()[CHAVE_ESPACO_PRODUCAO],
                        personagemEncontrado.val()[CHAVE_ESTADO],
                        personagemEncontrado.val()[CHAVE_USO])
                    listaPersonagens.append(personagem)
        except:
            print(f'Erro')
        return listaPersonagens
    
    def modificaPersonagem(self, personagem):
        try:
            self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.pegaId()).update(personagem.__dict__)
        except:
            print(f'Erro')

    def alternaUso(self, personagem):
        personagem.alternaUso()
        self.modificaPersonagem(personagem)

    def alternaEstado(self, personagem):
        personagem.alternaEstado()
        self.modificaPersonagem(personagem)