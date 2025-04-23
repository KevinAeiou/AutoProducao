from constantes import *
from modelos.trabalhoEstoque import TrabalhoEstoque
from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.stream import Stream
from modelos.personagem import Personagem
from requests.exceptions import HTTPError
from firebase_admin import db
from firebase_admin.db import Event
from modelos.logger import MeuLogger

class RepositorioEstoque(Stream):
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_ESTOQUE, nomeLogger= CHAVE_REPOSITORIO_ESTOQUE)
        personagem = Personagem() if personagem is None else personagem
        self.__logger: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_ESTOQUE, arquivoLogger= f'{CHAVE_REPOSITORIO_ESTOQUE}.log')
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        self.__personagem: Personagem= personagem
        self.__erro: str= None
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferencia: db.Reference = meuBanco.reference(CHAVE_ESTOQUE).child(self.__personagem.id)
        except Exception as e:
            self.__logger.error(menssagem= f'Erro: {e}')
        
    def streamHandler(self, evento: Event):
        super().streamHandler(evento= evento)
        if evento.event_type in (STRING_PUT, STRING_PATCH):
            if evento.path == '/':
                return
            self.__logger.debug(menssagem= evento.path)
            self.__logger.debug(menssagem= evento.data)
            ids: list[str]= evento.path.split('/')
            dicionarioTrabalho: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if evento.data is None:
                if len(ids) > 2:
                    dicionario: dict= {CHAVE_ID: ids[2]}
                    dicionarioTrabalho[CHAVE_TRABALHOS]= dicionario
                    super().insereDadosModificados(dado= dicionarioTrabalho)
                    return
                dicionarioTrabalho[CHAVE_TRABALHOS]= None
                super().insereDadosModificados(dado= dicionarioTrabalho)
                return
            dicionario: dict = evento.data
            dicionario[CHAVE_ID] = ids[2]
            dicionarioTrabalho[CHAVE_TRABALHOS]= dicionario
            super().insereDadosModificados(dado= dicionarioTrabalho)

    def pegaTodosTrabalhosEstoque(self) -> list[TrabalhoEstoque] | None:
        listaEstoque: list[TrabalhoEstoque]= []
        try:
            trabalhosEstoqueEncontrados: dict= self.__minhaReferencia.get()
            if trabalhosEstoqueEncontrados is None:
                return listaEstoque
            for chave, valor in trabalhosEstoqueEncontrados.items():
                trabalhoEstoque: TrabalhoEstoque= TrabalhoEstoque()
                trabalhoEstoque.dicionarioParaObjeto(valor)
                listaEstoque.append(trabalhoEstoque)
            self.__logger.debug(menssagem= f'Estoque recuperado com sucesso!')
            return listaEstoque
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao recuperar trabalhos no estoque: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao recuperar trabalhos no estoque: {e}')
        return None
        
    def insereTrabalhoEstoque(self, trabalho: TrabalhoEstoque):
        try:
            resultado: dict= self.__minhaReferencia.get()
            if resultado is not None:
                for chave, valor in resultado.items():
                    if valor[CHAVE_ID_TRABALHO] == trabalho.idTrabalho:
                        trabalho.id = chave
                        break
            self.__minhaReferencia.child(trabalho.id).set({CHAVE_ID: trabalho.id, CHAVE_QUANTIDADE: trabalho.quantidade, CHAVE_ID_TRABALHO: trabalho.idTrabalho})
            self.__logger.debug(menssagem= f'Trabalho ({self.__personagem.id.ljust(36)} | {trabalho}) inserido com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao inserir trabalho no estoque: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao inserir trabalho no estoque: {e}')
        return False

    def modificaTrabalhoEstoque(self, trabalho: TrabalhoEstoque) -> bool:
        try:
            self.__minhaReferencia.child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_QUANTIDADE: trabalho.quantidade})
            self.__logger.debug(menssagem= f'Trabalho ({self.__personagem.id.ljust(36)} | {trabalho}) modificado com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao modificar trabalho no estoque: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao modificar trabalho no estoque: {e}')
        return False
    
    def removeTrabalho(self, trabalho: TrabalhoEstoque) -> bool:
        try:
            self.__minhaReferencia.child(trabalho.id).delete()
            self.__logger.debug(menssagem= f'Trabalho ({trabalho}) removido com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao remover trabalho no estoque: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao remover trabalho no estoque: {e}')
        return False

    @property
    def pegaErro(self):
        return self.__erro