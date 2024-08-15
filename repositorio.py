import pyrebase
from constantes import *
from modelos.personagem import Personagem

config = {
    'apiKey': "AIzaSyCrQz9bYczFvF5S-HNlha48hXD7Mmiq6R8",
    'authDomain': "bootwarspear.firebaseapp.com",
    'databaseURL': "https://bootwarspear-default-rtdb.firebaseio.com",
    'projectId': "bootwarspear",
    'storageBucket': "bootwarspear.appspot.com",
    'messagingSenderId': "882438857395",
    'appId': "1:882438857395:web:1d0b926a94d0aacca086c6"}
firebase = pyrebase.initialize_app(config)

meuBanco = firebase.database()

def pegaTodosPersonagens():
    listaPersonagens = []
    todosPersonagens = meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).get()
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