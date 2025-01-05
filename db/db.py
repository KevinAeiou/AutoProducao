import sqlite3
from constantes import *

class MeuBanco:
    def __init__(self):
        self.__SQLITE = 1
        self.__fabrica = None
        self.__erroConexao = None
        self.conexao =  None

    def pegaConexao(self, banco):
        self.__fabrica = banco
        if banco == self.__SQLITE:
            nomeConexao = 'autoProducao.db'
            try:
                self.conexao = sqlite3.connect(nomeConexao)
            except Exception as e:
                self.__erroConexao = str(e)
        return self.conexao

    def desconecta(self):
        try:
            self.conexao.close()
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
            cursor = self.conexao.cursor()
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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS profissoes(
                id VARCHAR(30) PRIMARY KEY NOT NULL, 
                idPersonagem VARCHAR(30) NOT NULL, 
                nome TEXT NOT NULL, 
                experiencia INTEGER NOT NULL, 
                prioridade TINYINT NOT NULL);
                """)

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
            self.__erroConexao = str(e)

    def removeTabela(self, tabela: str) -> bool:
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""DROP TABLE {tabela}""")
            return True
        except Exception as e:
            self.__erroConexao = str(e)
        return False