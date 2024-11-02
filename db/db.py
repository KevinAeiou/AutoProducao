import sqlite3

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
        except AttributeError:
            pass

    def pegaErros(self):
        return self.__erroConexao
    
    def pegaFabrica(self):
        return self.__fabrica

    def criaTabelas(self):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS trabalhos(id VARCHAR(30) PRIMARY KEY NOT NULL, nome TEXT NOT NULL, nomeProducao TEXT NOT NULL, experiencia INTEGER NOT NULL, nivel INTEGER NOT NULL, profissao TEXT NOT NULL, raridade TEXT NOT NULL, trabalhoNecessario TEXT NOT NULL); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS personagens(id VARCHAR(30) PRIMARY KEY NOT NULL, nome TEXT NOT NULL, email TEXT NOT NULL, senha TEXT NOT NULL, espacoProducao INTEGER NOT NULL, estado TINYINT NOT NULL, uso TINYINT NOT NULL, autoProducao TINYINT NOT NULL); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS profissoes(id VARCHAR(30) PRIMARY KEY NOT NULL, idPersonagem VARCHAR(30) NOT NULL, nome TEXT NOT NULL, experiencia INTEGER NOT NULL, prioridade TINYINT NOT NULL); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS vendas(id VARCHAR(30) PRIMARY KEY NOT NULL, nomeProduto TEXT NOT NULL, dataVenda VARCHAR(12) NOT NULL, nomePersonagem VARCHAR(30) NOT NULL, quantidadeProduto INTEGER NOT NULL, trabalhoId VARCHAR(30) NOT NULL, valorProduto INTEGER NOT NULL); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS Lista_desejo(id VARCHAR(30) PRIMARY KEY NOT NULL, idTrabalho VARCHAR(30) NOT NULL, idPersonagem VARCHAR(30) NOT NULL, nome TEXT NOT NULL, nomeProducao TEXT NOT NULL, experiencia INTEGER NOT NULL, nivel INTEGER NOT NULL, profissao VARCHAR(30) NOT NULL, raridade VARCHAR(10) NOT NULL, trabalhoNecessario TEXT NOT NULL, recorrencia TINYINT NOT NULL, tipoLicenca TEXT NOT NULL, estado INTEGER NOT NULL); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS Lista_estoque(id VARCHAR(30) PRIMARY KEY NOT NULL, idPersonagem VARCHAR(30) NOT NULL, idTrabalho VARCHAR(30) NOT NULL, nome VARCHAR(30) NOT NULL, profissao VARCHAR(30) NOT NULL, nivel INTEGER NOT NULL, quantidade INTEGER NOT NULL, raridade VARCHAR(10) NOT NULL); """)

        except AttributeError:
            print(f'Faça a conexão do banco antes de criar as tabelas.')

    def excluiTabelaVendas(self):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""DROP TABLE vendas""")
        except AttributeError:
            print(f'Faça a conexão do banco antes de alternar o uso.')