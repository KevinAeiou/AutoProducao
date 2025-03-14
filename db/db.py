import sqlite3
from constantes import *
from modelos.logger import MeuLogger
import os

class MeuBanco:
    def __init__(self, banco:int= 1):
        self.__logger: MeuLogger= MeuLogger(nome= 'bancoDados')
        self.__nomeConexao = 'autoProducao.db'
        self.__SQLITE = 1
        self.__fabrica = None
        self.__erroConexao = None
        self.__conexao =  None
        self.__banco: int= banco

    def pegaConexao(self):
        self.__fabrica = self.__banco
        if self.__banco == self.__SQLITE:
            try:
                self.__conexao = sqlite3.connect(self.__nomeConexao)
            except Exception as e:
                self.__erroConexao = str(e)
        return self.__conexao

    def desconecta(self):
        try:
            self.__conexao.close()
            return True
        except Exception as e:
            self.__erroConexao = str(e)
        return False

    def pegaErro(self):
        return self.__erroConexao
    
    def pegaFabrica(self):
        return self.__fabrica

    def criaTabelas(self):
        try:
            cursor = self.__conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trabalhos(
                id VARCHAR(30) PRIMARY KEY NOT NULL, 
                nome TEXT NOT NULL, 
                nomeProducao TEXT NOT NULL, 
                experiencia INTEGER NOT NULL, 
                nivel INTEGER NOT NULL, 
                profissao TEXT NOT NULL, 
                raridade TEXT NOT NULL, 
                trabalhoNecessario TEXT NOT NULL);
                """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personagens(
                id VARCHAR(30) PRIMARY KEY NOT NULL, 
                nome TEXT NOT NULL, 
                email TEXT NOT NULL, 
                senha TEXT NOT NULL, 
                espacoProducao INTEGER NOT NULL, 
                estado TINYINT NOT NULL, 
                uso TINYINT NOT NULL, 
                autoProducao TINYINT NOT NULL);
                """)

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {CHAVE_PROFISSOES.lower()} (
                {CHAVE_ID} VARCHAR(30) NOT NULL, 
                {CHAVE_ID_PERSONAGEM} VARCHAR(30) NOT NULL, 
                {CHAVE_NOME} TEXT NOT NULL, 
                {CHAVE_EXPERIENCIA} INTEGER NOT NULL, 
                {CHAVE_PRIORIDADE} TINYINT NOT NULL,
                PRIMARY KEY ({CHAVE_ID}, {CHAVE_ID_PERSONAGEM})
                );""")

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {CHAVE_LISTA_VENDAS}(
                {CHAVE_ID} VARCHAR(30) PRIMARY KEY NOT NULL, 
                {CHAVE_DESCRICAO} TEXT NOT NULL, 
                {CHAVE_DATA_VENDA} VARCHAR(12) NOT NULL, 
                {CHAVE_ID_PERSONAGEM} VARCHAR(30) NOT NULL, 
                {CHAVE_QUANTIDADE} INTEGER NOT NULL, 
                {CHAVE_ID_TRABALHO} VARCHAR(30) NOT NULL, 
                {CHAVE_VALOR} INTEGER NOT NULL);
                """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Lista_desejo (
                id VARCHAR(30) PRIMARY KEY NOT NULL, 
                idTrabalho VARCHAR(30) NOT NULL, 
                idPersonagem VARCHAR(30) NOT NULL, 
                recorrencia TINYINT NOT NULL, 
                tipoLicenca TEXT NOT NULL, 
                estado INTEGER NOT NULL);
                """)

            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS Lista_estoque(
                id VARCHAR(30) PRIMARY KEY NOT NULL, 
                idPersonagem VARCHAR(30) NOT NULL, 
                idTrabalho VARCHAR(30) NOT NULL, 
                quantidade INTEGER NOT NULL);
                """)
        except Exception as e:
            self.__erroConexao= str(e)
            self.__logger.error(menssagem= f'Erro ao criar tabelas: {e}')

    def removeTabela(self, tabela: str) -> bool:
        try:
            cursor = self.__conexao.cursor()
            cursor.execute(f"""DROP TABLE {tabela}""")
            return True
        except Exception as e:
            self.__erroConexao = str(e)
        return False