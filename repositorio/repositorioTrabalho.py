from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalho import Trabalho
from constantes import *
from time import time
from modelos.logger import MeuLogger
from repositorio.stream import Stream
from firebase_admin import db
from firebase_admin.db import Event

class RepositorioTrabalho(Stream):
    def __init__(self) -> None:
        super().__init__(chave= CHAVE_LISTA_TRABALHOS, nomeLogger= CHAVE_REPOSITORIO_TRABALHO)
        self.__logger: MeuLogger= MeuLogger(nome= CHAVE_REPOSITORIO_TRABALHO, arquivo_logger= f'{CHAVE_REPOSITORIO_TRABALHO}.log')
        self.__erro: str= None
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferenciaTrabalhos: db.Reference= meuBanco.reference(CHAVE_LISTA_TRABALHOS)
            self.__minhaReferenciaEstoque: db.Reference= meuBanco.reference(CHAVE_ESTOQUE)
            self.__minhaReferenciaProducao: db.Reference= meuBanco.reference(CHAVE_PRODUCAO)
            self.__minhaReferenciaVendas: db.Reference= meuBanco.reference(CHAVE_VENDAS)
        except Exception as e:
            self.__logger.error(mensagem= f'Erro: {e}')
            self.__erro = e
    
    def streamHandler(self, evento: Event):
        super().streamHandler(evento= evento)
        if evento.event_type in (STRING_PUT, STRING_PATCH):
            if evento.path == "/":
                return
            self.__logger.debug(mensagem= evento.path)
            self.__logger.debug(mensagem= evento.data)
            caminho: str= evento.path
            idTrabalho: str= caminho.replace('/','').strip()
            dicionarioTrabalho: dict= {CHAVE_ID: idTrabalho}
            if evento.data is None:
                # Algum trabalho foi removido do servidor
                super().insereDadosModificados(dado= dicionarioTrabalho)
                return
            # Algum trabalho foi modificado/inserido no servidor
            dicionarioTrabalho = evento.data
            dicionarioTrabalho[CHAVE_ID] = idTrabalho
            super().insereDadosModificados(dado= dicionarioTrabalho)

    def pegaTodosTrabalhos(self):
        trabalhos: list[Trabalho] = []
        try:
            todosTrabalhos: dict= self.__minhaReferenciaTrabalhos.get()
            for chave, valor in todosTrabalhos.items():
                trabalho = Trabalho()
                trabalho.dicionarioParaObjeto(valor)
                trabalho.id = chave
                trabalhos.append(trabalho)
            self.__logger.debug(mensagem= f'Trabalhos recuperados com sucesso!')
            return trabalhos
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao pegar trabalhos: {e}')
        return None
    
    def insereTrabalho(self, trabalho: Trabalho):
        try:
            self.__minhaReferenciaTrabalhos.child(trabalho.id).set(trabalho.__dict__)
            self.__logger.debug(mensagem= f'Trabalho ({trabalho}) inserido com sucesso!')
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao inserir trabalho: {e}')
        return False
    
    def modificaTrabalho(self, trabalho: Trabalho):
        try:
            self.__minhaReferenciaTrabalhos.child(trabalho.id).update(trabalho.__dict__)
            self.__logger.debug(mensagem= f'Trabalho ({trabalho}) modificado com sucesso!')
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao modificar trabalho: {e}')
        return False
    
    def removeTrabalho(self, trabalho: Trabalho) -> bool:
        try:
            self.__minhaReferenciaTrabalhos.child(trabalho.id).delete()
            self.__logger.debug(mensagem= f'Trabalho ({trabalho}) removido com sucesso!')
            todasVendas: dict = self.__minhaReferenciaVendas.get()
            if todasVendas is not None:
                for idPersonagem in todasVendas:
                    for idVenda in todasVendas[idPersonagem]:
                        if todasVendas[idPersonagem][idVenda][CHAVE_ID_TRABALHO] == trabalho.id:
                            self.__minhaReferenciaVendas.child(idPersonagem).child(idVenda).delete()
                            self.__logger.debug(mensagem= f'Referência de ({trabalho}) removido da lista de vendas com sucesso!')
            estoques: dict = self.__minhaReferenciaEstoque.get()
            if estoques is not None:
                for idPersonagem in estoques:
                    for idEstoque in estoques[idPersonagem]:
                        if estoques[idPersonagem][idEstoque][CHAVE_ID_TRABALHO] == trabalho.id:
                            self.__minhaReferenciaEstoque.child(idPersonagem).child(idEstoque).delete()
                            self.__logger.debug(mensagem= f'Referência de ({trabalho}) removido da lista de estoque com sucesso!')
            producoes: dict = self.__minhaReferenciaProducao.get()
            if producoes is not None:
                for idPersonagem in producoes:
                    for idProducao in producoes[idPersonagem]:
                        if producoes[idPersonagem][idProducao][CHAVE_ID_TRABALHO] == trabalho.id:
                            self.__minhaReferenciaProducao.child(idPersonagem).child(idProducao).delete()
                            self.__logger.debug(mensagem= f'Referência de ({trabalho}) removido da lista de produções com sucesso!')
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao remover trabalho: {e}')
        return False

    @property
    def pegaErro(self):
        return self.__erro