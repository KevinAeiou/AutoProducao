from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalho import Trabalho
from constantes import *
import time

class RepositorioTrabalho:
    def __init__(self) -> None:
        self.__erro = None
        self.__tempo = None
        self.__meuBanco = FirebaseDatabase().pegaDataBase()
        self.__dadosModificados: list[Trabalho] = []

    def abreStream(self):
        try:
            self.__inicio = time.time()
            self.__streamPronta = False
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).stream(self.stream_handler)
            return True
        except Exception as e:
            self.__erro = str(e)
            return False

    @property
    def estaPronto(self) -> bool:
        """
        Returns:
            bool: True if my stuff is ready for use
        """
        return len(self.__dadosModificados) != 0
    
    def pegaDadosModificados(self):
        return self.__dadosModificados
    
    def pegaTempoFinal(self):
        return self.__tempo
    
    def pegaTempo(self):
        return time.time() - self.__inicio
    
    def streamPronta(self):
        return self.__streamPronta
    
    def limpaLista(self):
        self.__dadosModificados.clear()
    
    def stream_handler(self, message):
        print("Lista de trabalhos foi modificada...")
        if message["event"] in ("put", "patch"):
            if message["path"] == "/":
                self.__fim = time.time()
                self.__tempo = self.__fim - self.__inicio
                self.__streamPronta = True
                return
            trabalho = Trabalho()
            if message['data'] is None:
                # Algum trabalho foi removido do servidor
                idTrabalhoDeletado = message['path'].replace('/','').strip()
                trabalho.setId(idTrabalhoDeletado)
                self.__dadosModificados.append(trabalho)
                return
            # Algum trabalho foi modificado/inserido no servidor
            trabalho.dicionarioParaObjeto(message['data'])
            self.__dadosModificados.append(trabalho)

    def pegaTodosTrabalhos(self):
        listaTrabalhos = []
        try:
            todosTrabalhos = self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).get()
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
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.pegaId()).set(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def modificaTrabalho(self, trabalho):
        try:
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.pegaId()).update(trabalho.__dict__)
            return True
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeTrabalho(self, trabalho):
        try:
            self.__meuBanco.child(CHAVE_LISTA_TRABALHOS).child(trabalho.pegaId()).remove()
            return True
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro