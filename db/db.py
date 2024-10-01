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
                print(f'Banco conectado!')
                self.conexao = sqlite3.connect(nomeConexao)
            except Exception as e:
                self.__erroConexao = str(e)
        return self.conexao

    def desconecta(self):
        try:
            print(f'Banco desconectado!')
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
            cursor.execute(""" CREATE TABLE IF NOT EXISTS trabalhos(id VARCHAR(30) PRIMARY KEY, nome TEXT, nomeProducao TEXT, experiencia INTEGER, nivel INTEGER, profissao TEXT, raridade TEXT, trabalhoNecessario TEXT); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS personagens(id VARCHAR(30) PRIMARY KEY, nome TEXT, email TEXT, senha TEXT, espacoProducao INTEGER, estado TINYINT, uso TINYINT); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS profissoes(id VARCHAR(30) PRIMARY KEY, idPersonagem VARCHAR(30), nome TEXT, experiencia INTEGER, prioridade TINYINT); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS vendas(id VARCHAR(30) PRIMARY KEY, nomeProduto TEXT, dataVenda VARCHAR(12), nomePersonagem VARCHAR(30), quantidadeProduto INTEGER, trabalhoId VARCHAR(30), valorProduto INTEGER); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS Lista_desejo(id VARCHAR(30) PRIMARY KEY, idTrabalho VARCHAR(30), idPersonagem VARCHAR(30), nome TEXT, nomeProducao TEXT, experiencia INTEGER, nivel INTEGER, profissao VARCHAR(30), raridade VARCHAR(10), trabalhoNecessario TEXT, recorrencia TINYINT, tipoLicenca TEXT, estado INTEGER); """)

            cursor.execute(""" CREATE TABLE IF NOT EXISTS Lista_estoque(id VARCHAR(30) PRIMARY KEY, idPersonagem VARCHAR(30), idTrabalho VARCHAR(30), nome VARCHAR(30), profissao VARCHAR(30), nivel INTEGER, quantidade INTEGER, raridade VARCHAR(10)); """)

        except AttributeError:
            print(f'Faça a conexão do banco antes de criar as tabelas.')

    def excluiTabelaVendas(self):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""DROP TABLE vendas""")
        except AttributeError:
            print(f'Faça a conexão do banco antes de alternar o uso.')