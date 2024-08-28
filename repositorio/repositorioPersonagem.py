from constantes import *
from modelos.personagem import Personagem
from repositorio.firebaseDatabase import FirebaseDatabase

class RepositorioPersonagem:
    def __init__(self):
        self._meuBanco = FirebaseDatabase()._dataBase
    
    def pegaTodosPersonagens(self):
        listaPersonagens = []
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
        return listaPersonagens
    
    def modificaPersonagem(self, personagem):
        self._meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(personagem.pegaId()).update(personagem)