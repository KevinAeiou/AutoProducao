import sqlite3
import uuid
from modelos.personagem import Personagem
from modelos.profissao import Profissao
from modelos.trabalho import Trabalho
from modelos.trabalhoProducao import TrabalhoProducao
from modelos.trabalhoVendido import TrabalhoVendido
from modelos.trabalhoEstoque import TrabalhoEstoque

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

    def insereTrabalho(self, trabalho):
        try:
            cursor = self.conexao.cursor()
            try:
                cursor.execute("""
                    INSERT INTO trabalhos (id, nome, nomeProducao, experiencia, nivel, profissao, raridade, trabalhoNecessario)
                    VALUES (?,?,?,?,?,?,?,?)
                    """, (trabalho.pegaId(), trabalho.pegaNome(), trabalho.pegaNomeProducao(), trabalho.pegaExperiencia(), trabalho.pegaNivel(), trabalho.pegaProfissao(), trabalho.pegaRaridade(), trabalho.pegaTrabalhoNecessario()))
                self.conexao.commit()
            except sqlite3.IntegrityError:
                print(f'O id {trabalho.pegaId()} já existe!')
            except sqlite3.OperationalError:
                print(f'O banco está trancado.')
        except AttributeError:
            print(f'Faça a conexão do banco antes de inserir novo trabalho.')

    def insereProfissoes(self, personagem):
        listaProfissoes = [Profissao('1', 'Arma de longo alcance', 0, False), Profissao('2','Armas corpo a corpo',0,False), Profissao('3','Armadura de tecido',0,False), Profissao('4','Armadura leve',0,False), Profissao('5','Armadura pesada',0,False), Profissao('6','Anéis',0,False), Profissao('7','Amuletos',0,False), Profissao('8','Capotes',0,False), Profissao('9','Braceletes',0,False)]
        # try:
        cursor = self.conexao.cursor()
        for profissao in listaProfissoes:
            profissao.setId(profissao.pegaId() + str(uuid.uuid4()))
            prioridade = 1 if profissao.pegaPrioridade() else 0
            try:
                cursor.execute("""
                    INSERT INTO profissoes (id, idPersonagem, nome, experiencia, prioridade) VALUES (?,?,?,?,?)
                    """, (profissao.pegaId(), personagem.pegaId(), profissao.pegaNome(), profissao.pegaExperiencia(), prioridade))
                self.conexao.commit()
                print(f'Profissão ({profissao}) inserida com sucesso!')
            except sqlite3.IntegrityError:
                print(f'O id {personagem.pegaId()} já existe!')
        # except AttributeError:
        #     print(f'Faça a conexão do banco antes de inserir nova profissão.')

    def insereVenda(self, venda):
        try:
            cursor = self.conexao.cursor()
            try:
                cursor.execute("""
                    INSERT INTO vendas (id, nomeProduto, dataVenda, nomePersonagem, quantidadeProduto, trabalhoId, valorProduto) VALUES (?,?,?,?,?,?,?)
                    """, (venda.pegaId(), venda.pegaNomeProduto(), venda.pegaDataVenda(), venda.pegaNomePersonagem(), venda.pegaQuantidadeProduto(), venda.pegaTrabalhoId(), venda.pegaValorProduto()))
                self.conexao.commit()
            except sqlite3.IntegrityError:
                print(f'O id {venda.pegaId()} já existe!')
        except AttributeError:
            print(f'Faça a conexão do banco antes de inserir nova venda.')

    def pegaTodasVendas(self, personagem):
        todasVendas = []
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""SELECT * FROM vendas WHERE nomePersonagem = {personagem.pegaId()};""")
            for linha in cursor.fetchall():
                todasVendas.append(TrabalhoVendido(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]))
        except AttributeError:
            print(f'Faça a conexão do banco antes de pegar as vendas.')
        return todasVendas

    def pegaTodosTrabalhosEstoque(self, personagem):
        todosTrabahlosEstoque = []
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""SELECT * FROM Lista_estoque WHERE idPersonagem = {personagem.pegaId()};""")
            for linha in cursor.fetchall():
                todosTrabahlosEstoque.append(TrabalhoEstoque(linha[0], linha[3], linha[4], linha[5], linha[6], linha[7], linha[2]))
        except AttributeError:
            print(f'Faça a conexão do banco antes de pegar os trabalhos em estoque.')
        return todosTrabahlosEstoque

    def modificaProfissao(self, profissao):
        prioridade = 1 if profissao.pegaPrioridade() else 0
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                UPDATE profissoes SET nome = ?, experiencia = ?, prioridade = ?
                WHERE id == ?""", (profissao.pegaNome(), profissao.pegaExperiencia(), prioridade, profissao.pegaId()))
            self.conexao.commit()
            print(f'Profissão ({profissao.pegaNome()}) modificada com sucesso!')
        except AttributeError:
            print(f'Faça a conexão do banco antes de modificar a profissão.')

    def modificaTrabalhoEstoque(self, trabalhoEstoque):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                UPDATE Lista_estoque SET nome = ?, profissao = ?, nivel = ?, quantidade = ?, raridade = ?
                WHERE id == ?""", (trabalhoEstoque.pegaNome(), trabalhoEstoque.pegaProfissao(), trabalhoEstoque.pegaNivel(), trabalhoEstoque.pegaQuantidade(), trabalhoEstoque.pegaRaridade, trabalhoEstoque.pegaId()))
            self.conexao.commit()
            print(f'Trabalho em estoque ({trabalhoEstoque.pegaNome()}) modificado com sucesso!')
        except AttributeError:
            print(f'Faça a conexão do banco antes de modificar o trabalho em estoque.')

    def modificaTrabalhoProducao(self, trabalhoProducao):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                UPDATE Lista_desejo SET nome = ?, profissao = ?, nivel = ?, quantidade = ?, raridade = ?
                WHERE id == ?""", (trabalhoProducao.pegaNome(), trabalhoProducao.pegaProfissao(), trabalhoProducao.pegaNivel(), trabalhoProducao.pegaQuantidade(), trabalhoProducao.pegaRaridade, trabalhoProducao.pegaId()))
            self.conexao.commit()
            print(f'Trabalho em estoque ({trabalhoProducao.pegaNome()}) modificado com sucesso!')
        except AttributeError:
            print(f'Faça a conexão do banco antes de modificar o trabalho em produção.')

    def excluiTabelaVendas(self):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""DROP TABLE vendas""")
        except AttributeError:
            print(f'Faça a conexão do banco antes de alternar o uso.')