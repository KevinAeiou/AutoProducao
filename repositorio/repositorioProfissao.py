from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.credenciais.firebaseCredenciais import CHAVE_ID_USUARIO
from repositorio.stream import Stream
from modelos.profissao import Profissao
from modelos.personagem import Personagem
from constantes import *
from requests.exceptions import HTTPError
from pyrebase import pyrebase
from pyrebase.pyrebase import PyreResponse
from firebase_admin import db
from firebase_admin.db import Event
from modelos.logger import MeuLogger

class RepositorioProfissao(Stream):
    listaProfissoes = []
    def __init__(self, personagem: Personagem= None):
        super().__init__(chave= CHAVE_PROFISSOES, nomeLogger= CHAVE_REPOSITORIO_PROFISSAO)
        personagem = Personagem() if personagem is None else personagem
        self.__erro: str= None
        firebaseDb: FirebaseDatabase = FirebaseDatabase()
        self.__personagem: Personagem= personagem
        self.__logger: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_PROFISSAO, arquivoLogger = f'{CHAVE_REPOSITORIO_PROFISSAO}.log')
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferenciaProfissoes: db.Reference= meuBanco.reference(CHAVE_PROFISSOES).child(self.__personagem.id)
            self.__minhaReferenciaListaProfissoes: db.Reference= meuBanco.reference(CHAVE_LISTA_PROFISSAO)
        except Exception as e:
            self.__erro = e
            self.__logger.error(menssagem= f'Erro: {e}')

    def streamHandler(self, evento: Event):
        super().streamHandler(evento= evento)
        if evento.event_type in (STRING_PUT, STRING_PATCH):
            if evento.path == '/':
                return
            self.__logger.debug(menssagem= evento.path)
            self.__logger.debug(menssagem= evento.data)
            ids: list[str]= evento.path.split('/')
            profissao: Profissao= Profissao()
            dicionarioProfissao: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if evento.data is None:
                if len(ids) > 2:
                    profissao.id= ids[2]
                    profissao.experiencia= None
                    dicionarioProfissao[CHAVE_TRABALHOS]= profissao
                    super().insereDadosModificados(dado= dicionarioProfissao)
                    return
                dicionarioProfissao[CHAVE_TRABALHOS]= None
                super().insereDadosModificados(dado= dicionarioProfissao)
                return
            profissao.dicionarioParaObjeto(dicionario= evento.data)
            dicionarioProfissao[CHAVE_TRABALHOS]= profissao
            super().insereDadosModificados(dado= dicionarioProfissao)

    def pegaProfissoesPersonagem(self) -> list[Profissao] | None:
        '''
            Função que retorna uma lista de objetos do tipo Profissao do servidor de um personagem específico
            Returns:
                profissoes (list[Profissao]): Lista de objetos Profissao.
        '''
        profissoes: list[Profissao]= []
        try:
            profissoesEncontradas: dict= self.__minhaReferenciaProfissoes.get()
            if profissoesEncontradas is None:
                return profissoes
            for chave, valor in profissoesEncontradas.items():
                profissao: Profissao= Profissao()
                profissao.dicionarioParaObjeto(valor)
                profissao.idPersonagem = self.__personagem.id
                profissao.nome= self.pegaNomeProfissaoPorId(id= profissao.id)
                profissoes.append(profissao)
            profissoes = sorted(profissoes, key = lambda profissao: profissao.nome)
            profissoes = sorted(profissoes, key = lambda profissao: profissao.experiencia, reverse = True)
            self.__logger.debug(menssagem= f'Profissões recuperadas com sucesso!')
            return profissoes
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao recuperar profissões: {e}')
        return None

    def pegaNomeProfissaoPorId(self, id: str) -> str:
        profissaoEncontrada: dict= self.__minhaReferenciaListaProfissoes.child(id).get()
        if profissaoEncontrada is None:
            raise Exception(f'({id}) não foi encontrado na lista de profissões!')
        return profissaoEncontrada[CHAVE_NOME]
    
    def pegaListaProfissoes(self) -> list[Profissao]:
        profissoes: list[Profissao] = []
        try:
            profissoesEncontradas: dict= self.__minhaReferenciaListaProfissoes.get()
            if profissoesEncontradas is None:
                return profissoes
            for chave, valor in profissoesEncontradas.items():
                profissao: Profissao= Profissao()
                profissao.dicionarioParaObjeto(valor)
                profissoes.append(profissao)
            self.__logger.debug(menssagem= f'Lista de profissões recuperadas com sucesso!')
            return profissoes
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao recuperar lista de profissões: {e}')
        return None
    
    def insereProfissao(self, profissao: Profissao) -> bool:
        '''
            Função para inserir um objeto da classe Profissao.
            Args:
                profissao (Profissao): Objeto da classe Profissao para ser inserida.
            Returns:
                bool: Verdadeiro caso profissão seja inserida com sucesso.
        '''
        profissao.idPersonagem = self.__personagem.id
        try:
            profissoes: dict= self.__minhaReferenciaListaProfissoes.get()
            if profissoes is None:
                self.__minhaReferenciaListaProfissoes.child(profissao.id).update({CHAVE_ID: profissao.id, CHAVE_NOME: profissao.nome})
                self.__logger.debug(menssagem= f'Profissão ({profissao.id} | {profissao.nome}) inserida com sucesso na lista de profissões!')
            else:
                for chave, valor in profissoes.items():
                    if valor[CHAVE_NOME] == profissao.nome:
                        profissao.id= chave
                        break
                else:
                    self.__minhaReferenciaListaProfissoes.child(profissao.id).update({CHAVE_ID: profissao.id, CHAVE_NOME: profissao.nome})
            self.__minhaReferenciaProfissoes.child(profissao.id).set({CHAVE_ID: profissao.id, CHAVE_EXPERIENCIA: profissao.experiencia, CHAVE_PRIORIDADE: profissao.prioridade})
            self.__logger.debug(menssagem= f'Profissão ({profissao}) inserida com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao inserir profissão: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao inserir profissão: {e}')
        return False

    def modificaProfissao(self, profissao: Profissao) -> bool:
        profissao.idPersonagem = self.__personagem.id
        try:
            self.__minhaReferenciaProfissoes.child(profissao.id).update({CHAVE_EXPERIENCIA: profissao.experiencia, CHAVE_PRIORIDADE: profissao.prioridade})
            self.__minhaReferenciaListaProfissoes.child(profissao.id).update({CHAVE_NOME: profissao.nome})
            self.__logger.debug(menssagem= f'Profissão ({profissao}) modificada com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao modificar profissão: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao modificar profissão: {e}')
        return False
    
    def removeProfissao(self, profissao: Profissao) -> bool:
        profissao.idPersonagem = self.__personagem.id
        try:
            self.__minhaReferenciaProfissoes.child(profissao.id).delete()
            self.__logger.debug(menssagem= f'Profissão ({profissao}) removida com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(menssagem= f'Erro ao modificar profissão: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(menssagem= f'Erro ao modificar profissão: {e}')
        return False
    
    @property
    def pegaErro(self):
        return self.__erro