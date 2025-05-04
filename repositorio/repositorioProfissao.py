from repositorio.firebaseDatabase import FirebaseDatabase
from repositorio.stream import Stream
from modelos.profissao import Profissao
from modelos.personagem import Personagem
from constantes import *
from requests.exceptions import HTTPError
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
        self.__logger: MeuLogger = MeuLogger(nome= CHAVE_REPOSITORIO_PROFISSAO, arquivo_logger = f'{CHAVE_REPOSITORIO_PROFISSAO}.log')
        try:
            meuBanco: db = firebaseDb.banco
            self.__minhaReferenciaProfissoes: db.Reference= meuBanco.reference(CHAVE_PROFISSOES).child(self.__personagem.id)
            self.__minhaReferenciaListaProfissoes: db.Reference= meuBanco.reference(CHAVE_LISTA_PROFISSAO)
        except Exception as e:
            self.__erro = e
            self.__logger.error(mensagem= f'Erro: {e}')

    def streamHandler(self, evento: Event):
        super().streamHandler(evento= evento)
        if evento.event_type in (STRING_PUT, STRING_PATCH):
            if evento.path == '/':
                return
            self.__logger.debug(mensagem= evento.path)
            self.__logger.debug(mensagem= evento.data)
            ids: list[str]= evento.path.split('/')
            dicionario: dict= {CHAVE_ID_PERSONAGEM: ids[1]}
            if evento.data is None:
                if len(ids) > 2:
                    dicionarioProfissao: dict = {CHAVE_ID: ids[2]}
                    dicionario[CHAVE_TRABALHOS]= dicionarioProfissao
                    super().insereDadosModificados(dado= dicionario)
                    return
                dicionario[CHAVE_TRABALHOS]= None
                super().insereDadosModificados(dado= dicionario)
                return
            dicionarioProfissao: dict = evento.data
            dicionarioProfissao[CHAVE_ID] = ids[2]
            dicionario[CHAVE_TRABALHOS]= dicionarioProfissao
            super().insereDadosModificados(dado= dicionario)

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
            self.__logger.debug(mensagem= f'Profissões recuperadas com sucesso!')
            return profissoes
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao recuperar profissões: {e}')
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
            self.__logger.debug(mensagem= f'Lista de profissões recuperadas com sucesso!')
            return profissoes
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao recuperar lista de profissões: {e}')
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
                self.__logger.debug(mensagem= f'Profissão ({profissao.id} | {profissao.nome}) inserida com sucesso na lista de profissões!')
            else:
                for chave, valor in profissoes.items():
                    if valor[CHAVE_NOME] == profissao.nome:
                        profissao.id= chave
                        break
                else:
                    self.__minhaReferenciaListaProfissoes.child(profissao.id).update({CHAVE_ID: profissao.id, CHAVE_NOME: profissao.nome})
            self.__minhaReferenciaProfissoes.child(profissao.id).set({CHAVE_ID: profissao.id, CHAVE_EXPERIENCIA: profissao.experiencia, CHAVE_PRIORIDADE: profissao.prioridade})
            self.__logger.debug(mensagem= f'Profissão ({profissao}) inserida com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro ao inserir profissão: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao inserir profissão: {e}')
        return False

    def modificaProfissao(self, profissao: Profissao) -> bool:
        profissao.idPersonagem = self.__personagem.id
        try:
            self.__minhaReferenciaProfissoes.child(profissao.id).update({CHAVE_EXPERIENCIA: profissao.experiencia, CHAVE_PRIORIDADE: profissao.prioridade})
            self.__minhaReferenciaListaProfissoes.child(profissao.id).update({CHAVE_NOME: profissao.nome})
            self.__logger.debug(mensagem= f'Profissão ({profissao}) modificada com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro ao modificar profissão: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao modificar profissão: {e}')
        return False
    
    def removeProfissao(self, profissao: Profissao) -> bool:
        profissao.idPersonagem = self.__personagem.id
        try:
            self.__minhaReferenciaProfissoes.child(profissao.id).delete()
            self.__logger.debug(mensagem= f'Profissão ({profissao}) removida com sucesso!')
            return True
        except HTTPError as e:
            self.__erro = str(e.errno)
            self.__logger.error(mensagem= f'Erro ao modificar profissão: {e.errno}')
        except Exception as e:
            self.__erro = str(e)
            self.__logger.error(mensagem= f'Erro ao modificar profissão: {e}')
        return False
    
    @property
    def pegaErro(self):
        return self.__erro