from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from modelos.trabalhoVendido import TrabalhoVendidoVelho, TrabalhoVendido
from constantes import CHAVE_USUARIOS, CHAVE_LISTA_PERSONAGEM, CHAVE_LISTA_VENDAS

class RepositorioVendas:
    __meuBanco = None
    def __init__(self, personagem) -> None:
        self.__erro = None
        self.__personagem = personagem
        self.__meuBanco = FirebaseDatabase().pegaDataBase()

    def pegaTrabalhosVendidos(self) -> list[TrabalhoVendidoVelho] | None:
        listaVendas = []
        try:
            todasVendas = self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_VENDAS).get()
            if todasVendas.pyres == None:
                return listaVendas
            for vendaEncontrada in todasVendas.each():
                trabalhoVendido = TrabalhoVendidoVelho()
                trabalhoVendido.dicionarioParaObjeto(vendaEncontrada.val())
                trabalhoVendido.id = vendaEncontrada.key()
                listaVendas.append(trabalhoVendido)
            return listaVendas
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_VENDAS).child(trabalho.id).set(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_VENDAS).child(trabalho.id).update(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
        
    def removeTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_VENDAS).child(trabalho.id).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
        
    def limpaListaVenda(self):
        try:
            self.__meuBanco.child(CHAVE_USUARIOS).child(CHAVE_ID_USUARIO).child(CHAVE_LISTA_PERSONAGEM).child(self.__personagem.id).child(CHAVE_LISTA_VENDAS).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro