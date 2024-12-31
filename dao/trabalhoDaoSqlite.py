__author__ = 'Kevin Amazonas'

from modelos.trabalho import Trabalho
from db.db import MeuBanco
from repositorio.repositorioTrabalho import RepositorioTrabalho
import logging

class TrabalhoDaoSqlite():
    logging.basicConfig(level = logging.INFO, filename = 'logs/aplicacao.log', encoding='utf-8', format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt = '%d/%m/%Y %I:%M:%S %p')
    def __init__(self):
        self.__conexao = None
        self.__erro = None
        self.__fabrica = None
        self.__logger = logging.getLogger('trabalhoDao')
        try:
            self.__meuBanco = MeuBanco()
            self.__conexao = self.__meuBanco.pegaConexao(1)
            self.__fabrica = self.__meuBanco.pegaFabrica()
            self.__meuBanco.criaTabelas()
            self.__repositorioTrabalho = RepositorioTrabalho()
        except Exception as e:
            self.__erro = str(e)

    def pegaTrabalhos(self):
        trabalhos = []
        sql = """
            SELECT *
            FROM trabalhos
            WHERE id IS NOT NULL AND nome IS NOT NULL AND nomeProducao IS NOT NULL AND experiencia IS NOT NULL AND nivel IS NOT NULL AND profissao IS NOT NULL AND raridade IS NOT NULL AND trabalhoNecessario IS NOT NULL;
            """
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql)
                for linha in cursor.fetchall():
                    trabalho = Trabalho()
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                    trabalhos.append(trabalho)
                trabalhos = sorted(trabalhos, key= lambda trabalho: (trabalho.profissao, trabalho.raridade, trabalho.nivel))
                self.__meuBanco.desconecta()
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def pegaTrabalhosComumProfissaoNivelEspecifico(self, trabalhoBuscado):
        trabalhos = []
        sql = """
            SELECT * 
            FROM trabalhos
            WHERE profissao = ? 
            AND raridade == ? 
            AND nivel == ?;
            """
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalhoBuscado.profissao, trabalhoBuscado.raridade, str(trabalhoBuscado.nivel)))
                for linha in cursor.fetchall():
                    trabalho = Trabalho()
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                    trabalhos.append(trabalho)
                trabalhos = sorted(trabalhos, key= lambda trabalho: trabalho.nome)
                self.__meuBanco.desconecta()
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def pegaTrabalhosPorProfissaoRaridade(self, trabalhoBuscado):
        trabalhos = []
        sql = """
            SELECT * 
            FROM trabalhos
            WHERE profissao = ? 
            AND raridade == ?;
            """
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalhoBuscado.profissao, trabalhoBuscado.raridade))
                for linha in cursor.fetchall():
                    trabalho = Trabalho()
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                    trabalhos.append(trabalho)
                trabalhos = sorted(trabalhos, key= lambda trabalho: trabalho.nome)
                self.__meuBanco.desconecta()
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhoEspecificoPorId(self, idBuscado):
        trabalho = Trabalho()
        sql = """
            SELECT * 
            FROM trabalhos
            WHERE id == ?;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [idBuscado])
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                self.__meuBanco.desconecta()
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhoEspecificoPorNomeProfissaoRaridade(self, trabalhoBuscado):
        trabalho = Trabalho()
        sql = """
            SELECT * 
            FROM trabalhos
            WHERE nome == ? AND profissao = ? AND raridade == ?;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalhoBuscado.nome, trabalhoBuscado.profissao, trabalhoBuscado.raridade))
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                self.__meuBanco.desconecta()
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhoPorNome(self, nomeTrabalho : str) -> Trabalho:
        trabalho = Trabalho()
        sql = """
            SELECT * 
            FROM trabalhos
            WHERE nome == ?
            LIMIT 1;"""
        try:
            if self.__fabrica == 1:
                cursor = self.__conexao.cursor()
                cursor.execute(sql, [nomeTrabalho])
                for linha in cursor.fetchall():
                    trabalho.id = linha[0]
                    trabalho.nome = linha[1]
                    trabalho.nomeProducao = linha[2]
                    trabalho.experiencia = linha[3]
                    trabalho.nivel = linha[4]
                    trabalho.profissao = linha[5]
                    trabalho.raridade = linha[6]
                    trabalho.trabalhoNecessario = linha[7]
                self.__meuBanco.desconecta()
                return trabalho            
        except Exception as e:
            self.__erro = str(e)
        return None
    
    def insereTrabalho(self, trabalho, modificaServidor = True):
        sql = """INSERT INTO trabalhos (id, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.id, trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalho.insereTrabalho(trabalho):
                    self.__logger.info(f'({trabalho}) inserido no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao inserir ({trabalho}) no servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalho(self, trabalho : Trabalho, modificaServidor = True) -> bool:
        sql = """
            UPDATE trabalhos SET nome = ?, nomeProducao = ?, experiencia = ?, nivel = ?, profissao = ?, raridade = ?, trabalhoNecessario = ?
            WHERE id = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario, trabalho.id))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalho.modificaTrabalho(trabalho):
                    self.__logger.info(f'({trabalho}) modificado no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao modificar ({trabalho}) no servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False

    def modificaTrabalhoPorNomeProfissaoRaridade(self, trabalho):
        sql = """
            UPDATE trabalhos SET id = ?, nome = ?, nomeProducao = ?, experiencia = ?, nivel = ?, profissao = ?, raridade = ?, trabalhoNecessario = ?
            WHERE nome = ? AND profissao = ? AND raridade = ?"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, (trabalho.id, trabalho.nome, trabalho.nomeProducao, trabalho.experiencia, trabalho.nivel, trabalho.profissao, trabalho.raridade, trabalho.trabalhoNecessario, trabalho.nome, trabalho.profissao, trabalho.raridade))
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
        
    def removeTrabalho(self, trabalho, modificaServidor = True):
        sql = """DELETE FROM trabalhos WHERE id == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(sql, [trabalho.id])
            self.__conexao.commit()
            self.__meuBanco.desconecta()
            if modificaServidor:
                if self.__repositorioTrabalho.removeTrabalho(trabalho):
                    self.__logger.info(f'({trabalho}) removido do servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao remover ({trabalho}) do servidor: {self.__repositorioTrabalho.pegaErro()}')
            return True
        except Exception as e:
            self.__erro = str(e)
        self.__meuBanco.desconecta()
        return False
    
    def pegaErro(self):
        return self.__erro