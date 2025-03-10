from constantes import *
from modelos.trabalhoEstoque import TrabalhoEstoque
from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.stream import Stream
from modelos.personagem import Personagem
from requests.exceptions import HTTPError

class RepositorioEstoque(Stream):
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_ESTOQUE, nomeLogger= 'repositorioEstoque')
        self.__meuBanco = FirebaseDatabase().pegaMeuBanco()
        self.__personagem: Personagem= personagem
        self.__erro: str= None
        
    def streamHandler(self, menssagem: dict):
        super().streamHandler(menssagem= menssagem)
        if menssagem['event'] in ('put', 'path'):
            if menssagem['path'] == '/':
                return
            ids: list[str]= menssagem['path'].split('/')
            trabalho: TrabalhoEstoque= TrabalhoEstoque()
            dicionarioTrabalho: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if menssagem['data'] is None:
                if len(ids) > 2:
                    trabalho.id= ids[2]
                    dicionarioTrabalho[CHAVE_TRABALHOS]= trabalho
                    super().insereDadosModificados(dado= dicionarioTrabalho)
                return
            trabalho.dicionarioParaObjeto(dicionario= menssagem['data'])
            dicionarioTrabalho[CHAVE_TRABALHOS]= trabalho
            super().insereDadosModificados(dado= dicionarioTrabalho)

    def pegaTodosTrabalhosEstoque(self) -> list[TrabalhoEstoque] | None:
        listaEstoque: list[TrabalhoEstoque]= []
        try:
            trabalhosEstoqueEncontrados = self.__meuBanco.child(CHAVE_ESTOQUE).child(self.__personagem.id).get()
            if trabalhosEstoqueEncontrados.pyres == None:
                return listaEstoque
            for trabalhoEstoqueEncontrado in trabalhosEstoqueEncontrados.each():
                trabalhoEstoque: TrabalhoEstoque= TrabalhoEstoque()
                trabalhoEstoque.dicionarioParaObjeto(trabalhoEstoqueEncontrado.val())
                listaEstoque.append(trabalhoEstoque)
            return listaEstoque
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return None
        
    def insereTrabalhoEstoque(self, trabalho: TrabalhoEstoque):
        try:
            resultado= self.__meuBanco.child(CHAVE_ESTOQUE).child(self.__personagem.id).get()
            if resultado.pyres != None:
                for trabalhoEncontrado in resultado.each():
                    print(type(trabalhoEncontrado))
                    if trabalhoEncontrado.val()[CHAVE_ID_TRABALHO] == trabalho.idTrabalho:
                        trabalho.id= trabalhoEncontrado.key()
                        break
            self.__meuBanco.child(CHAVE_ESTOQUE).child(self.__personagem.id).child(trabalho.id).set({CHAVE_ID: trabalho.id, CHAVE_QUANTIDADE: trabalho.quantidade, CHAVE_ID_TRABALHO: trabalho.idTrabalho})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaTrabalhoEstoque(self, trabalho: TrabalhoEstoque) -> bool:
        try:
            self.__meuBanco.child(CHAVE_ESTOQUE).child(self.__personagem.id).child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_QUANTIDADE: trabalho.quantidade})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def removeTrabalho(self, trabalho: TrabalhoEstoque) -> bool:
        try:
            self.__meuBanco.child(CHAVE_ESTOQUE).child(self.__personagem.id).child(trabalho.id).remove()
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro