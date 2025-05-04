from repositorio.firebaseDatabase import FirebaseDatabase
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from constantes import *
from requests.exceptions import HTTPError
from modelos.logger import MeuLogger
from repositorio.stream import Stream
from firebase_admin.db import Event
from firebase_admin import db

class RepositorioTrabalhoProducao(Stream):
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_PRODUCAO, nomeLogger= CHAVE_REPOSITORIO_TRABALHO_PRODUCAO)
        personagem = Personagem() if personagem is None else personagem
        self.__logger: MeuLogger= MeuLogger(nome= CHAVE_REPOSITORIO_TRABALHO_PRODUCAO, arquivo_logger= f'{CHAVE_REPOSITORIO_TRABALHO_PRODUCAO}.log')
        self.__erro: str = None
        self._personagem: Personagem= personagem
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferencia: db.Reference = meuBanco.reference(CHAVE_PRODUCAO)
        except Exception as e:
            self.__logger.error(mensagem= f'Erro: {e}')

    def streamHandler(self, evento: Event):
        super().streamHandler(evento= evento)
        if evento.event_type in (STRING_PUT, STRING_PATCH):
            if evento.path == '/':
                return
            self.__logger.debug(mensagem= evento.path)
            self.__logger.debug(mensagem= evento.data)
            ids: list[str]= evento.path.split('/')
            dicionarioTrabalho: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if evento.data is None:
                if len(ids) > 2:
                    dicionario: dict = {CHAVE_ID: ids[2]}
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
            pass

    def pegaTodosTrabalhosProducao(self) -> list[TrabalhoProducao] | None:
        '''
        Retorna uma lista de objetos do tipo TrabalhoProducao encontrados no servidor
        Returns:
            trabalhos (list[TrabalhoProducao]): Lista de trabalhos do tipo TrabalhoProducao
        Raises:
            None: Se algum erro for encontrado
        '''
        trabalhos: list[TrabalhoProducao]= []
        try:
            trabalhosEncontrados: dict= self.__minhaReferencia.child(self._personagem.id).get()
            if trabalhosEncontrados is None:
                return trabalhos
            for chave, valor in trabalhosEncontrados.items():
                trabalho: TrabalhoProducao= TrabalhoProducao()
                trabalho.dicionarioParaObjeto(valor)
                trabalhos.append(trabalho)
            trabalhos= sorted(trabalhos, key=lambda trabalhoProducao: trabalhoProducao.estado, reverse= True)
            self.__logger.debug(mensagem= f'Trabalhos para produção recuperados com sucesso!')
            return trabalhos
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro ao recuperar trabalhos para produção: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao recuperar trabalhos para produção: {e}')
        return None

    def pegaTrabalhosProducaoEstadoProduzirProduzindo(self) -> list[TrabalhoProducao] | None:
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            todosTrabalhosProducao: dict= self.__minhaReferencia.child(self._personagem.id).order_by_child(CHAVE_ESTADO).start_at(0).end_at(1).get()
            if todosTrabalhosProducao is None:
                return trabalhosProducao
            for chave, valor in todosTrabalhosProducao.items():
                trabalhoProducao: TrabalhoProducao = TrabalhoProducao()
                trabalhoProducao.dicionarioParaObjeto(valor)
                trabalhosProducao.append(trabalhoProducao)
            trabalhosProducao = sorted(trabalhosProducao, key=lambda trabalhoProducao: trabalhoProducao.estado, reverse=True)
            self.__logger.debug(mensagem= f'Trabalhos para produção com estados "Para produzir" e "Produzindo" recuperados com sucesso!')
            return trabalhosProducao
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro ao pegar trabalhos para produção com estados paraProduzir(0) e produzindo(1): {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao pegar trabalhos para produção com estados paraProduzir(0) e produzindo(1): {e.errno}')
        return None
    
    def removeTrabalhoProducao(self, trabalho: TrabalhoProducao) -> bool:
        try:
            self.__minhaReferencia.child(self._personagem.id).child(trabalho.id).delete()
            self.__logger.debug(mensagem= f'Trabalho ({self._personagem.id.ljust(36)} | {trabalho}) removido com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro remover trabalho para produção: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro remover trabalho para produção: {e}')
        return False
    
    def insereTrabalhoProducao(self, trabalho: TrabalhoProducao) -> bool:
        try:
            self.__minhaReferencia.child(self._personagem.id).child(trabalho.id).set({CHAVE_ID: trabalho.id, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_ESTADO: trabalho.estado, CHAVE_RECORRENCIA: trabalho.recorrencia, CHAVE_TIPO_LICENCA: trabalho.tipoLicenca})
            self.__logger.debug(mensagem= f'Trabalho ({self._personagem.id.ljust(36)} | {trabalho}) inserido com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro inserir trabalho para produção: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro inserir trabalho para produção: {e}')
        return False

    def modificaTrabalhoProducao(self, trabalho: TrabalhoProducao) -> bool:
        try:
            self.__minhaReferencia.child(self._personagem.id).child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_ESTADO: trabalho.estado, CHAVE_RECORRENCIA: trabalho.recorrencia, CHAVE_TIPO_LICENCA: trabalho.tipoLicenca})
            self.__logger.debug(mensagem= f'Trabalho ({trabalho}) modificado com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro modificar trabalho para produção: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro modificar trabalho para produção: {e}')
        return False

    @property
    def pegaErro(self):
        return self.__erro