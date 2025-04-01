from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.personagem import Personagem
from constantes import *
from requests.exceptions import HTTPError
from modelos.logger import MeuLogger
from repositorio.stream import Stream

class RepositorioTrabalhoProducao(Stream):
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_PRODUCAO, nomeLogger= CHAVE_REPOSITORIO_TRABALHO_PRODUCAO)
        self.__logger: MeuLogger= MeuLogger(nome= CHAVE_REPOSITORIO_TRABALHO_PRODUCAO)
        self.__erro: str = None
        self.__meuBanco= FirebaseDatabase().pegaMeuBanco()
        self._personagem: Personagem= personagem

    def streamHandler(self, menssagem: dict):
        super().streamHandler(menssagem= menssagem)
        if menssagem['event'] in ('put', 'path'):
            if menssagem['path'] == '/':
                return
            self.__logger.debug(menssagem= menssagem)
            ids: list[str]= menssagem['path'].split('/')
            trabalho: TrabalhoProducao= TrabalhoProducao()
            dicionarioTrabalho: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if menssagem['data'] is None:
                if len(ids) > 2:
                    trabalho.id= ids[2]
                    dicionarioTrabalho[CHAVE_TRABALHOS]= trabalho
                    super().insereDadosModificados(dado= dicionarioTrabalho)
                    return
                dicionarioTrabalho[CHAVE_TRABALHOS]= None
                super().insereDadosModificados(dado= dicionarioTrabalho)
                return
            trabalho.dicionarioParaObjeto(dicionario= menssagem['data'])
            dicionarioTrabalho[CHAVE_TRABALHOS]= trabalho
            super().insereDadosModificados(dado= dicionarioTrabalho)
            pass

    def limpaListaProducao(self):
        '''
        Método para limpar lista de trabalhos no servidor
        '''
        try:
            self.__meuBanco.child(CHAVE_PRODUCAO).child(self._personagem.id).remove()
        except Exception as e:
            self.__erro= str(e)

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
            trabalhosEncontrados= self.__meuBanco.child(CHAVE_PRODUCAO).child(self._personagem.id).get()
            if trabalhosEncontrados.pyres == None:
                return trabalhos
            for trabalhoEncontrado in trabalhosEncontrados.each():
                trabalho: TrabalhoProducao= TrabalhoProducao()
                trabalho.dicionarioParaObjeto(trabalhoEncontrado.val())
                trabalhos.append(trabalho)
            trabalhos= sorted(trabalhos, key=lambda trabalhoProducao: trabalhoProducao.estado, reverse= True)
            return trabalhos
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhosProducaoEstadoProduzirProduzindo(self) -> list[TrabalhoProducao] | None:
        try:
            trabalhosProducao: list[TrabalhoProducao]= []
            todosTrabalhosProducao = self.__meuBanco.child(CHAVE_PRODUCAO).child(self._personagem.id).order_by_child(CHAVE_ESTADO).start_at(0).end_at(1).get()
            if todosTrabalhosProducao.pyres is None:
                return trabalhosProducao
            for trabalhoProducaoEncontrado in todosTrabalhosProducao.each():
                trabalhoProducao: TrabalhoProducao = TrabalhoProducao()
                trabalhoProducao.dicionarioParaObjeto(trabalhoProducaoEncontrado.val())
                trabalhosProducao.append(trabalhoProducao)
            trabalhosProducao = sorted(trabalhosProducao, key=lambda trabalhoProducao: trabalhoProducao.estado, reverse=True)
            return trabalhosProducao
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def removeTrabalhoProducao(self, trabalhoProducao: TrabalhoProducao) -> bool:
        try:
            self.__meuBanco.child(CHAVE_PRODUCAO).child(self._personagem.id).child(trabalhoProducao.id).remove()
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False
    
    def insereTrabalhoProducao(self, trabalhoProducao: TrabalhoProducao) -> bool:
        try:
            self.__meuBanco.child(CHAVE_PRODUCAO).child(self._personagem.id).child(trabalhoProducao.id).set({CHAVE_ID: trabalhoProducao.id, CHAVE_ID_TRABALHO: trabalhoProducao.idTrabalho, CHAVE_ESTADO: trabalhoProducao.estado, CHAVE_RECORRENCIA: trabalhoProducao.recorrencia, CHAVE_TIPO_LICENCA: trabalhoProducao.tipoLicenca})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def modificaTrabalhoProducao(self, trabalho: TrabalhoProducao) -> bool:
        try:
            self.__meuBanco.child(CHAVE_PRODUCAO).child(self._personagem.id).child(trabalho.id).update({CHAVE_ID: trabalho.id, CHAVE_ID_TRABALHO: trabalho.idTrabalho, CHAVE_ESTADO: trabalho.estado, CHAVE_RECORRENCIA: trabalho.recorrencia, CHAVE_TIPO_LICENCA: trabalho.tipoLicenca})
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
        except Exception as e:
            self.__erro = str(e)
        return False

    def pegaErro(self):
        return self.__erro