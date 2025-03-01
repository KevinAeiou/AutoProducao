__author__ = 'Kevin Amazonas'

from modelos.profissao import Profissao
from modelos.personagem import Personagem
from db.db import MeuBanco
import logging
from repositorio.repositorioProfissao import RepositorioProfissao
from constantes import CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMAS_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES, CHAVE_ID

class ProfissaoDaoSqlite:
    logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
    logger = logging.getLogger('repositorioProfissao')
    def __init__(self, personagem = None):
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
    
    def modificaProfissao(self, profissao, modificaServidor = True):
        prioridade = 1 if profissao.prioridade else 0
        sql = """
            UPDATE profissoes 
            SET nome = ?, experiencia = ?, prioridade = ?
            WHERE id == ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (profissao.nome, profissao.experiencia, prioridade, profissao.id))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioProfissao.modificaProfissao(profissao):
                    self.logger.info(f'({profissao}) modificado no servidor com sucesso!')
                else:
                    self.logger.error(f'Erro ao modificar ({profissao}) no servidor: {self.__repositorioProfissao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def removeProfissao(self, profissao, modificaServidor = True):
        sql = """
            DELETE FROM profissoes
            WHERE id == ?;
            """
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [profissao.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioProfissao.removeProfissao(profissao):
                    self.logger.info(f'({profissao}) removido do servidor com sucesso!')
                else:
                    self.logger.error(f'Erro ao remover ({profissao}) do servidor: {self.__repositorioProfissao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def insereListaProfissoes(self):
        profissoes = [CHAVE_PROFISSAO_ARMA_DE_LONGO_ALCANCE, CHAVE_PROFISSAO_ARMAS_CORPO_A_CORPO, CHAVE_PROFISSAO_ARMADURA_DE_TECIDO, CHAVE_PROFISSAO_ARMADURA_LEVE, CHAVE_PROFISSAO_ARMADURA_PESADA, CHAVE_PROFISSAO_ANEIS, CHAVE_PROFISSAO_AMULETOS, CHAVE_PROFISSAO_CAPOTES, CHAVE_PROFISSAO_BRACELETES]
        for nomeProfissao in profissoes:
            self.__conexao = self.__meuBanco.pegaConexao(1)
            profissao = Profissao()
            profissao.nome = nomeProfissao
            profissao.idPersonagem = self.__personagem.id
            if self.insereProfissao(profissao):
                print(f'({nomeProfissao}) inserido no banco com sucesso!')
                continue
            print(f'Erro ao inserir profissão no banco: {self.pegaErro()}')
            return False
        return True
    
    def insereProfissao(self, profissao: Profissao, modificaServidor: bool = True) -> bool:
        prioridade: int = 1 if profissao.prioridade else 0
        sql = f"""
            INSERT INTO profissoes (id, idPersonagem, nome, experiencia, prioridade)
            VALUES (?, ?, ?, ?, ?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (profissao.id, self.__personagem.id, profissao.nome, profissao.experiencia, prioridade))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioProfissao.insereProfissao(profissao):
                    self.logger.info(f'({profissao}) inserido no servidor com sucesso!')
                else:
                    self.logger.error(f'Erro ao inserir ({profissao}) no servidor: {self.__repositorioProfissao.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
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