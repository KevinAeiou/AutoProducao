__author__ = 'Kevin Amazonas'

from modelos.profissao import Profissao
from modelos.personagem import Personagem
from db.db import MeuBanco
from modelos.logger import MeuLogger
from repositorio.repositorioProfissao import RepositorioProfissao
from constantes import CHAVE_ID, CHAVE_ID_PERSONAGEM, CHAVE_NOME, CHAVE_EXPERIENCIA, CHAVE_PRIORIDADE, LISTA_PROFISSOES, CHAVE_PROFISSOES

class ProfissaoPersonagemDaoSqlite:
    def __init__(self, banco: MeuBanco):
        self.__meuBanco: MeuBanco= banco
        self.__meuLogger: MeuLogger= MeuLogger(nome= 'profissaoDao')
        self.__conexao = None
        self.__erro = None

    def pegaProfissaoPorId(self, personagem: Personagem, id: str) -> Profissao | None:
        '''
            Função para buscar uma profissão específica no banco de dados local
            Args:
                personagem (Personagem): Objeto da classe Personagem que contêm o "id" do personagem atual
                id (str): String que contêm o "id" da profissão específica
            Returns:
                profissao (Profissao): Objeto da classe Profissao com os dados encontrados no banco
        '''
        try:
            self.__conexao = self.__meuBanco.pega_conexao()
            sql = f"""SELECT * FROM {CHAVE_PROFISSOES.lower()} WHERE {CHAVE_ID} == ? AND {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (id, personagem.id))
            profissao: Profissao= Profissao()
            for linha in cursor.fetchall():
                profissao.id = linha[0]
                profissao.idPersonagem = linha[1]
                profissao.nome = linha[2]
                profissao.experiencia = linha[3]
                profissao.prioridade = True if linha[4] == 1 else False
            return profissao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None

    def pegaNomeProfissaoPorId(self, id: str) -> str | None:
        '''
            Função para buscar o atributo "nome" de uma profissão específica no servidor
            Args:
                id (str): String que contêm o "id" da profissão específica
            Returns:
                nomeProfissao (str): String que contêm o dado encontrado no servidor
        '''
        try:
            repositorioProfissao: RepositorioProfissao= RepositorioProfissao()
            nomeProfissao: str= repositorioProfissao.pegaNomeProfissaoPorId(id= id)
            return nomeProfissao
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def pegaProfissoesPorIdPersonagem(self, personagem: Personagem) -> list[Profissao]:
        try:
            self.__conexao = self.__meuBanco.pega_conexao()
            profissoes: list[Profissao]= []
            sql = f"""SELECT * FROM {CHAVE_PROFISSOES.lower()} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [personagem.id])
            for linha in cursor.fetchall():
                prioridade = True if linha[4] == 1 else False
                profissao: Profissao = Profissao()
                profissao.id = linha[0]
                profissao.idPersonagem = linha[1]
                nome: str= '' if linha[2] is None else linha[2]
                profissao.nome = nome
                profissao.experiencia = linha[3]
                profissao.prioridade = prioridade
                profissoes.append(profissao)
            profissoes = sorted(profissoes, key=lambda profissao: profissao.nome)
            profissoes = sorted(profissoes, key=lambda profissao: profissao.experiencia, reverse=True)
            return profissoes
        except Exception as e:
            self.__erro = str(e)
        finally:
            self.__meuBanco.desconecta()
        return None
    
    def modificaProfissao(self, personagem: Personagem, profissao: Profissao, modificaServidor: bool = True):
        try:
            repositorioProfissao: RepositorioProfissao= RepositorioProfissao(personagem= personagem)
            self.__conexao = self.__meuBanco.pega_conexao()
            prioridade: int= 1 if profissao.prioridade else 0
            sql = f"""UPDATE {CHAVE_PROFISSOES.lower()} SET {CHAVE_EXPERIENCIA} = ?, {CHAVE_PRIORIDADE} = ? WHERE {CHAVE_ID} == ? AND {CHAVE_ID_PERSONAGEM} == ?"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (profissao.experiencia, prioridade, profissao.id, personagem.id))
            if modificaServidor:
                if repositorioProfissao.modificaProfissao(profissao= profissao):
                    self.__meuLogger.info(f'({profissao}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__meuLogger.error(f'Erro ao modificar ({profissao}) no servidor: {repositorioProfissao.pegaErro}')
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removeProfissao(self, personagem: Personagem, profissao: Profissao, modificaServidor: bool = True) -> bool:
        try:
            repositorioProfissao: RepositorioProfissao = RepositorioProfissao(personagem= personagem)
            self.__conexao = self.__meuBanco.pega_conexao()
            sql = f"""DELETE FROM {CHAVE_PROFISSOES.lower()} WHERE {CHAVE_ID} == ? AND {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (profissao.id, personagem.id))
            if modificaServidor:
                if repositorioProfissao.removeProfissao(profissao= profissao):
                    self.__meuLogger.info(f'({profissao}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__meuLogger.error(f'Erro ao remover ({profissao}) do servidor: {repositorioProfissao.pegaErro}')
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def removeProfissoesPorIdPersonagem(self, personagem: Personagem) -> bool:
        try:
            self.__conexao = self.__meuBanco.pega_conexao()
            sql = f"""DELETE FROM {CHAVE_PROFISSOES.lower()} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [personagem.id])
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def insere_lista_profissoes(self, personagem: Personagem):
        for nome_profissao in LISTA_PROFISSOES:
            self.__conexao = self.__meuBanco.pega_conexao()
            profissao = Profissao()
            profissao.nome = nome_profissao
            profissao.idPersonagem = personagem.id
            if self.insere_profissao(personagem= personagem, profissao= profissao):
                self.__meuLogger.info(f'({nome_profissao}) inserido no banco com sucesso!')
                continue
            self.__meuLogger.error(f'Erro ao inserir profissão no banco: {self.pegaErro}')
            return False
        return True
    
    def insere_profissao(self, personagem: Personagem, profissao: Profissao, modificaServidor: bool = True) -> bool:
        '''
            Função que insere um objeto do tipo Profissao no banco de dados
            Returns:
                bool: Verdadeiro caso inserido com sucesso
            Args:
                profissao (Profissao): Novo objeto para inserir no banco
                modificaServidor(bool): Valor boleano, verdadeiro por padrão, que indica se a nova profissão também deve ser inserida no servidor
        '''
        try:
            repositorioProfissao: RepositorioProfissao= RepositorioProfissao(personagem= personagem)
            self.__conexao = self.__meuBanco.pega_conexao()
            prioridade: int = 1 if profissao.prioridade else 0
            sql = f"""INSERT INTO {CHAVE_PROFISSOES.lower()} ({CHAVE_ID}, {CHAVE_ID_PERSONAGEM}, {CHAVE_NOME}, {CHAVE_EXPERIENCIA}, {CHAVE_PRIORIDADE}) VALUES (?, ?, ?, ?, ?);"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (profissao.id, personagem.id, profissao.nome, profissao.experiencia, prioridade))
            if modificaServidor:
                if repositorioProfissao.insereProfissao(profissao= profissao):
                    self.__meuLogger.info(f'({profissao}) inserido no servidor com sucesso!')
                    self.__conexao.commit()
                    return True
                self.__meuLogger.error(f'Erro ao inserir ({profissao}) no servidor: {repositorioProfissao.pegaErro}')
                self.__conexao.rollback()
                return False
            self.__conexao.commit()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def sincroniza_profissoes_por_id(self, personagem: Personagem):
        '''
            Função para sincronizar as profissões no servidor, de um personagem específico, com o banco de dados local
            Returns:
                bool: Verdadeiro caso a sincronização seja comcluída com sucesso
        '''
        self.__conexao = self.__meuBanco.pega_conexao()
        if self.__conexao is None:
            raise Exception("Falha ao conectar ao banco de dados")

        try:
            sql = f"""DELETE FROM {CHAVE_PROFISSOES.lower()} WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [personagem.id])
            repositorio_profissao: RepositorioProfissao= RepositorioProfissao(personagem= personagem)
            profissoes_servidor: list[Profissao] | None = repositorio_profissao.pega_profissoes_personagem()

            if profissoes_servidor is None:
                self.__meuLogger.error(f'Erro ao buscar profissões no servidor: {repositorio_profissao.pegaErro}')
                raise Exception(repositorio_profissao.pegaErro)
            
            for profissao in profissoes_servidor:
                prioridade: int = 1 if profissao.prioridade else 0
                sql = f"""
                    INSERT INTO {CHAVE_PROFISSOES.lower()} ({CHAVE_ID}, {CHAVE_ID_PERSONAGEM}, {CHAVE_NOME}, {CHAVE_EXPERIENCIA}, {CHAVE_PRIORIDADE})
                    VALUES (?, ?, ?, ?, ?)"""
                try:
                    cursor.execute(sql, (profissao.id, personagem.id, profissao.nome, profissao.experiencia, prioridade))
    
                except Exception as e:
                    raise e
    
            self.__conexao.commit()
            return True

        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()

        finally:
            self.__meuBanco.desconecta()

        return False

    @property
    def pegaErro(self):
        '''
            Propriedade que retorna o último erro registrado.
        '''
        return self.__erro