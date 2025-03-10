from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoVendido import TrabalhoVendidoVelho, TrabalhoVendido
from modelos.personagem import Personagem
from constantes import CHAVE_VENDAS, CHAVE_ID, CHAVE_DESCRICAO, CHAVE_DATA_VENDA, CHAVE_ID_TRABALHO, CHAVE_QUANTIDADE, CHAVE_VALOR, CHAVE_ID_PERSONAGEM, CHAVE_TRABALHOS, CHAVE_REPOSITORIO_VENDAS
from requests.exceptions import HTTPError
from repositorio.stream import Stream

class RepositorioVendas(Stream):
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_VENDAS, nomeLogger= CHAVE_REPOSITORIO_VENDAS)
        self.__erro: str= None
        self.__personagem: Personagem= personagem
        self.__meuBanco= FirebaseDatabase().pegaMeuBanco()

    def streamHandler(self, menssagem: dict):
        super().streamHandler(menssagem= menssagem)
        if menssagem['event'] in ('put', 'path'):
            if menssagem['path'] == '/':
                return
            ids: list[str]= menssagem['path'].split('/')
            trabalhoVendido: TrabalhoVendido= TrabalhoVendido()
            dicionarioVenda: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if menssagem['data'] is None:
                trabalhoVendido.id= ids[2]
                dicionarioVenda[CHAVE_TRABALHOS]= trabalhoVendido
                super().insereDadosModificados(dado= dicionarioVenda)
                return
            trabalhoVendido.dicionarioParaObjeto(dicionario= menssagem['data'])
            dicionarioVenda[CHAVE_TRABALHOS]= trabalhoVendido
            super().insereDadosModificados(dado= dicionarioVenda)

    def pegaTrabalhosVendidos(self) -> list[TrabalhoVendidoVelho] | None:
        listaVendas = []
        try:
            vendasEncontradas = self.__meuBanco.child(CHAVE_VENDAS).child(self.__personagem.id).get()
            if vendasEncontradas.pyres == None:
                return listaVendas
            for vendaEncontrada in vendasEncontradas.each():
                trabalhoVendido = TrabalhoVendidoVelho()
                trabalhoVendido.dicionarioParaObjeto(vendaEncontrada.val())
                trabalhoVendido.id = vendaEncontrada.key()
                listaVendas.append(trabalhoVendido)
            return listaVendas
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__meuBanco.child(CHAVE_VENDAS).child(self.__personagem.id).child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_DESCRICAO: trabalho.descricao, CHAVE_DATA_VENDA: trabalho.dataVenda, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_QUANTIDADE: trabalho.quantidade, CHAVE_VALOR: trabalho.valor})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__meuBanco.child(CHAVE_VENDAS).child(self.__personagem.id).child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_DESCRICAO: trabalho.descricao, CHAVE_DATA_VENDA: trabalho.dataVenda, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_QUANTIDADE: trabalho.quantidade, CHAVE_VALOR: trabalho.valor})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
        
    def removeTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__meuBanco.child(CHAVE_VENDAS).child(self.__personagem.id).child(trabalho.id).remove()
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
        
    def limpaListaVenda(self):
        try:
            self.__meuBanco.child(CHAVE_VENDAS).child(self.__personagem.id).remove()
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro