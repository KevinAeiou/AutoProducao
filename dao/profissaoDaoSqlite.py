__author__ = 'Kevin Amazonas'

from modelos.profissao import Profissao
from db.db import MeuBanco
from uuid import uuid4
import logging
from repositorio.repositorioProfissao import RepositorioProfissao
from constantes import CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES

class ProfissaoDaoSqlite:
    logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
    logger = logging.getLogger('repositorioProfissao')
    def __init__(self, personagem = None):
        self.__conexao = None
        self.__erro = None
        self.__personagem = personagem
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__meuBanco.criaTabelas()
            self.__repositorioProfissao = RepositorioProfissao(personagem)
        except Exception as e:
            self.__erro = str(e)

    def pegaProfissaoPorId(self, profissao):
        sql = f"""
            SELECT * FROM profissoes
            WHERE id == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [profissao.id])
            for linha in cursor.fetchall():
                prioridade = True if linha[4] == 1 else False
                profissao = Profissao()
                profissao.id = linha[0]
                profissao.idPersonagem = linha[1]
                profissao.nome = linha[2]
                profissao.experiencia = linha[3]
                profissao.prioridade = prioridade
            self.__meuBanco.desconecta()
            return profissao
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return None
    
    def pegaProfissoes(self):
        profissoes = []
        sql = f"""
        SELECT * FROM profissoes 
        WHERE idPersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
            for linha in cursor.fetchall():
                prioridade = True if linha[4] == 1 else False
                profissao = Profissao()
                profissao.id = linha[0]
                profissao.idPersonagem = linha[1]
                profissao.nome = linha[2]
                profissao.experiencia = linha[3]
                profissao.prioridade = prioridade
                profissoes.append(profissao)
            profissoes = sorted(profissoes, key=lambda profissao:(profissao.experiencia), reverse=True)
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
    
    def modificaProfissao(self, profissao, modificaProfissao = False):
        prioridade = 1 if profissao.prioridade else 0
        sql = """
            UPDATE profissoes 
            SET nome = ?, experiencia = ?, prioridade = ?
            WHERE id = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (profissao.nome, profissao.experiencia, prioridade, profissao.id))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaProfissao:
                if self.__repositorioProfissao.modificaProfissao(profissao):
                    self.logger.info(f'{profissao} modificada no servidor com sucesso!')
                else:
                    self.logger.error(f'Erro ao modificar ({profissao}) no servidor: {self.__repositorioProfissao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def insereListaProfissoes(self):
        profissoes = [CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMA_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES]
        for nomeProfissao in profissoes:
            self.__conexao = self.__meuBanco.pegaConexao(1)
            profissao = Profissao()
            profissao.id = str(profissoes.index(nomeProfissao))+str(uuid4())
            profissao.nome = nomeProfissao
            profissao.idPersonagem = self.__personagem.id
            if self.insereProfissao(profissao, True):
                print(f'Profissão {nomeProfissao} inserida com sucesso!')
                continue
            print(f'Erro ao inserir profissão: {self.pegaErro()}')
            return False
        return True
    
    def insereProfissao(self, profissao, modificaServidor = False):
        prioridade = 1 if profissao.prioridade else 0
        sql = """
            INSERT INTO profissoes (id, idPersonagem, nome, experiencia, prioridade)
            VALUES (?, ?, ?, ?, ?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (profissao.id, self.__personagem.id, profissao.nome, profissao.experiencia, prioridade))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioProfissao.insereProfissao(profissao):
                    self.logger.info(f'{profissao} inserido no servidor com sucesso!')
                else:
                    self.logger.error(f'Erro ao inserir ({profissao}) no servidor: {self.__repositorioProfissao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def limpaListaProfissoes(self, modificaServidor = False):
        sql = """DELETE FROM profissoes WHERE idPersonagem == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [self.__personagem.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioProfissao.limpaProfissoes():
                    self.logger.info(f'Lista de profissões ({self.__personagem}) limpa no servidor com sucesso!')
                else:
                    self.logger.error(f'Erro ao limpar lista de profissões no servidor: {self.__repositorioProfissao.pegaErro()}')
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