__author__ = 'Kevin Amazonas'

from modelos.profissao import Profissao
from modelos.personagem import Personagem
from db.db import MeuBanco
from modelos.logger import MeuLogger
from repositorio.repositorioProfissao import RepositorioProfissao
from constantes import CHAVE_ID, CHAVE_ID_PERSONAGEM, CHAVE_NOME, CHAVE_EXPERIENCIA, CHAVE_PRIORIDADE, LISTA_PROFISSOES, CHAVE_PROFISSOES, CHAVE_LISTA_PROFISSAO

class ProfissaoDaoSqlite:
    def __init__(self, personagem = None):
        self.__meuLogger: MeuLogger= MeuLogger(nome= 'repositorioProfissao')
        self.__conexao = None
        self.__erro = None
        self.__personagem: Personagem = personagem
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
            self.__repositorioProfissao = RepositorioProfissao(personagem)
        except Exception as e:
            self.__erro = str(e)

    def pegaProfissaoPorId(self, id : str) -> Profissao | None:
        sql = f"""
            SELECT * 
            FROM profissoes
            WHERE {CHAVE_ID} == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [id])
            profissao = Profissao()
            for linha in cursor.fetchall():
                profissao.id = linha[0]
                profissao.idPersonagem = linha[1]
                profissao.nome = linha[2]
                profissao.experiencia = linha[3]
                profissao.prioridade = True if linha[4] == 1 else False
            self.__meuBanco.desconecta()
            return profissao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaProfissoesPorIdPersonagem(self) -> list[Profissao]:
        profissoes: list[Profissao]= []
        sql = f"""
            SELECT *
            FROM {CHAVE_PROFISSOES.lower()}
            WHERE {CHAVE_ID_PERSONAGEM} == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
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
            self.__meuBanco.desconecta()
            return profissoes
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaTodasProfissoes(self):
        profissoes = []
        sql = f"""
            SELECT * FROM profissoes;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            for linha in cursor.fetchall():
                prioridade = True if linha[4] == 1 else False
                profissao = Profissao()
                profissao.id = linha[0]
                profissao.idPersonagem = linha[1]
                profissao.nome = linha[2]
                profissao.experiencia = linha[3]
                profissao.prioridade = prioridade
                profissoes.append(profissao)
            profissoes = sorted(profissoes, key=lambda profissao:(profissao.idPersonagem, profissao.experiencia), reverse=True)
            self.__meuBanco.desconecta()
            return profissoes
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def modificaProfissao(self, profissao: Profissao, modificaServidor: bool = True):
        prioridade: int= 1 if profissao.prioridade else 0
        sql = f"""
            UPDATE {CHAVE_PROFISSOES.lower()} 
            SET {CHAVE_EXPERIENCIA} = ?, {CHAVE_PRIORIDADE} = ?
            WHERE {CHAVE_ID} == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (profissao.experiencia, prioridade, profissao.id))
            if modificaServidor:
                if self.__repositorioProfissao.modificaProfissao(profissao= profissao):
                    self.__meuLogger.info(f'({profissao}) modificado no servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__meuLogger.error(f'Erro ao modificar ({profissao}) no servidor: {self.__repositorioProfissao.pegaErro()}')
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
    
    def removeProfissao(self, profissao: Profissao, modificaServidor: bool = True) -> bool:
        sql = f"""
            DELETE FROM {CHAVE_PROFISSOES.lower()}
            WHERE {CHAVE_ID} == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [profissao.id])
            if modificaServidor:
                if self.__repositorioProfissao.removeProfissao(profissao= profissao):
                    self.__meuLogger.info(f'({profissao}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__meuLogger.error(f'Erro ao remover ({profissao}) do servidor: {self.__repositorioProfissao.pegaErro()}')
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__conexao.rollback()
        self.__meuBanco.desconecta()
        return False
    
    def insereListaProfissoes(self):
        for nomeProfissao in LISTA_PROFISSOES:
            self.__conexao = self.__meuBanco.pegaConexao(1)
            profissao = Profissao()
            profissao.nome = nomeProfissao
            profissao.idPersonagem = self.__personagem.id
            if self.insereProfissao(profissao= profissao):
                self.__meuLogger.info(f'({nomeProfissao}) inserido no banco com sucesso!')
                continue
            self.__meuLogger.error(f'Erro ao inserir profissão no banco: {self.pegaErro()}')
            return False
        return True
    
    def insereProfissao(self, profissao: Profissao, modificaServidor: bool = True) -> bool:
        prioridade: int = 1 if profissao.prioridade else 0
        sql = f"""
            INSERT INTO profissoes ({CHAVE_ID}, {CHAVE_ID_PERSONAGEM}, {CHAVE_NOME}, {CHAVE_EXPERIENCIA}, {CHAVE_PRIORIDADE})
            VALUES (?, ?, ?, ?, ?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, (profissao.id, self.__personagem.id, profissao.nome, profissao.experiencia, prioridade))
            if modificaServidor:
                if self.__repositorioProfissao.insereProfissao(profissao= profissao):
                    self.__meuLogger.info(f'({profissao}) inserido no servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__meuLogger.error(f'Erro ao inserir ({profissao}) no servidor: {self.__repositorioProfissao.pegaErro()}')
                self.__conexao.rollback()
                self.__meuBanco.desconecta()
                return False
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
            self.__conexao.rollback()
        finally:
            self.__meuBanco.desconecta()
        return False
    
    def limpaListaProfissoes(self, modificaServidor = True):
        sql = """DELETE FROM profissoes WHERE idPersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioProfissao.limpaProfissoes():
                    self.__meuLogger.info(f'Lista de profissões ({self.__personagem}) limpa no servidor com sucesso!')
                else:
                    self.__meuLogger.error(f'Erro ao limpar lista de profissões no servidor: {self.__repositorioProfissao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def deletaTabelaProfissoes(self):
        sql = """
            DROP TABLE profissoes;            
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql)
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def pegaErro(self):
        return self.__erro