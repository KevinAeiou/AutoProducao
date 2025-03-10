__author__ = 'Kevin Amazonas'

from modelos.trabalho import Trabalho
from db.db import MeuBanco
from repositorio.repositorioTrabalho import RepositorioTrabalho
import logging
from constantes import CHAVE_ID, CHAVE_PROFISSAO, CHAVE_NIVEL, CHAVE_TRABALHOS, CHAVE_RARIDADE

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

    def pegaTrabalhos(self) -> list[Trabalho]:
        trabalhos: list[Trabalho]= []
        sql = f"""
            SELECT *
            FROM {CHAVE_TRABALHOS};
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
    
    def pegaTrabalhosPorProfissaoRaridadeNivel(self, trabalhoBuscado: Trabalho) -> list[Trabalho] | None:
        trabalhos: list[Trabalho] = []
        sql = f"""
            SELECT * 
            FROM {CHAVE_TRABALHOS}
            WHERE {CHAVE_PROFISSAO} = ? 
            AND {CHAVE_RARIDADE} == ? 
            AND {CHAVE_NIVEL} == ?;
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
                trabalhos = sorted(trabalhos, key= lambda trabalho: (trabalho.nivel, trabalho.nome))
                self.__meuBanco.desconecta()
                return trabalhos            
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhoPorId(self, idBuscado: str) -> Trabalho | None:
        trabalho: Trabalho= Trabalho()
        sql = f"""
            SELECT * 
            FROM {CHAVE_TRABALHOS}
            WHERE {CHAVE_ID} == ?;"""
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
    
    def retornaListaIdsRecursosNecessarios(self, trabalho: Trabalho) -> list[str] | None:
        sql = f"""
            SELECT {CHAVE_ID} 
            FROM {CHAVE_TRABALHOS}
            WHERE {CHAVE_PROFISSAO} == ?
            AND {CHAVE_NIVEL} == ?;"""
        try:
            if self.__fabrica == 1:
                idsTrabalhos = []
                cursor = self.__conexao.cursor()
                cursor.execute(sql, (trabalho.profissao, trabalho.nivel))
                for linha in cursor.fetchall():
                    idsTrabalhos.append(linha[0])
                self.__meuBanco.desconecta()
                return idsTrabalhos            
        except Exception as e:
            self.__erro = str(e)
        return None

    def pegaTrabalhoPorNomeProfissaoRaridade(self, trabalhoBuscado):
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
                    self.__logger.info(f'({trabalho.id.ljust(36)} | {trabalho}) inserido no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao inserir ({trabalho.id.ljust(36)} | {trabalho}) no servidor: {self.__repositorioTrabalho.pegaErro()}')
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
                    self.__logger.info(f'({trabalho.id.ljust(36)} | {trabalho}) modificado no servidor com sucesso!')
                else:
                    self.__logger.error(f'Erro ao modificar ({trabalho.id.ljust(36)} | {trabalho}) no servidor: {self.__repositorioTrabalho.pegaErro()}')
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
        
    def removeTrabalho(self, trabalho: Trabalho, modificaServidor: bool= True) -> bool:
        sql = f"""
            DELETE FROM {CHAVE_TRABALHOS}
            WHERE {CHAVE_ID} == ?;"""
        try:
            cursor = self.__conexao.cursor()
            cursor.execute('BEGIN')
            cursor.execute(sql, [trabalho.id])
            if modificaServidor:
                if self.__repositorioTrabalho.removeTrabalho(trabalho= trabalho):
                    self.__logger.info(f'({trabalho.id.ljust(36)} | {trabalho}) removido do servidor com sucesso!')
                    self.__conexao.commit()
                    self.__meuBanco.desconecta()
                    return True
                self.__logger.error(f'Erro ao remover ({trabalho.id.ljust(36)} | {trabalho}) do servidor: {self.__repositorioTrabalho.pegaErro()}')
                self.__erro= self.__repositorioTrabalho.pegaErro()
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
    
    def pegaErro(self):
        return self.__erro