from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoVendido import TrabalhoVendidoVelho, TrabalhoVendido
from modelos.personagem import Personagem
from modelos.logger import MeuLogger
from constantes import (
    CHAVE_VENDAS, 
    CHAVE_ID, 
    CHAVE_DESCRICAO, 
    CHAVE_DATA_VENDA, 
    CHAVE_ID_TRABALHO, 
    CHAVE_QUANTIDADE, 
    CHAVE_VALOR, 
    CHAVE_ID_PERSONAGEM, 
    CHAVE_TRABALHOS, 
    CHAVE_REPOSITORIO_VENDAS, 
    STRING_PUT, 
    STRING_PATCH)
from requests.exceptions import HTTPError
from repositorio.stream import Stream
from firebase_admin.db import Event
from firebase_admin import db

class RepositorioVendas(Stream):
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_VENDAS, nomeLogger= CHAVE_REPOSITORIO_VENDAS)
        personagem = Personagem() if personagem is None else personagem
        self.__logger: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_VENDAS, arquivoLogger= f'{CHAVE_REPOSITORIO_VENDAS}.log')
        self.__erro: str= None
        self.__personagem: Personagem= personagem
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferencia: db.Reference= meuBanco.reference(CHAVE_VENDAS)
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
            dicionarioVenda: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if evento.data is None:
                if len(ids) > 2:
                    dicionario: dict= {CHAVE_ID: ids[2]}
                    dicionarioVenda[CHAVE_TRABALHOS]= dicionario
                    super().insereDadosModificados(dado= dicionarioVenda)
                    return
                dicionarioVenda[CHAVE_TRABALHOS]= None
                super().insereDadosModificados(dado= dicionarioVenda)
                return
            dicionario: dict = evento.data
            dicionario[CHAVE_ID] = ids[2]
            dicionarioVenda[CHAVE_TRABALHOS] = dicionario
            super().insereDadosModificados(dado= dicionarioVenda)

    def pegaTrabalhosVendidos(self) -> list[TrabalhoVendidoVelho] | None:
        listaVendas = []
        try:
            vendasEncontradas: dict= self.__minhaReferencia.child(self.__personagem.id).get()
            if vendasEncontradas is None:
                return listaVendas
            for chave, valor in vendasEncontradas.items():
                trabalhoVendido = TrabalhoVendidoVelho()
                trabalhoVendido.dicionarioParaObjeto(valor)
                listaVendas.append(trabalhoVendido)
            self.__logger.debug(menssagem= f'Trabalhos vendidos recuperados com sucesso!')
            return listaVendas
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao recuperar trabalhos vendidos: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao recuperar trabalhos vendidos: {e}')
        return None
    
    def insereTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__minhaReferencia.child(self.__personagem.id).child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_DESCRICAO: trabalho.descricao, CHAVE_DATA_VENDA: trabalho.dataVenda, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_QUANTIDADE: trabalho.quantidade, CHAVE_VALOR: trabalho.valor})
            self.__logger.debug(menssagem= f'Trabalho ({self.__personagem.id.ljust(36)} | {trabalho}) inserido com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao inserir trabalho vendido: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao inserir trabalho vendido: {e}')
        return False

    def modificaTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__minhaReferencia.child(self.__personagem.id).child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_DESCRICAO: trabalho.descricao, CHAVE_DATA_VENDA: trabalho.dataVenda, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_QUANTIDADE: trabalho.quantidade, CHAVE_VALOR: trabalho.valor})
            self.__logger.debug(menssagem= f'Trabalho ({self.__personagem.id.ljust(36)} | {trabalho}) modificado com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao modificar trabalho vendido: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao modificar trabalho vendido: {e}')
        return False
        
    def removeTrabalhoVendido(self, trabalho: TrabalhoVendido) -> bool:
        try:
            self.__minhaReferencia.child(self.__personagem.id).child(trabalho.id).delete()
            self.__logger.debug(menssagem= f'Trabalho ({self.__personagem.id.ljust(36)} | {trabalho}) removido com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao remover trabalho vendido: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao remover trabalho vendido: {e}')
        return False
    
    @property
    def abreStream(self) -> bool:
        if super().abreStream:
           return True 
        self.__erro = super().pegaErro
        return False

    @property
    def pegaErro(self):
        return self.__erro